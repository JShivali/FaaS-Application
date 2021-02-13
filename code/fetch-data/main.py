import requests
from urllib.request import urlopen
import io
import sys
from google.cloud import storage
import matplotlib.pyplot as plt
import json
import os
import redis
import base64

def fetch_data(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    #convert  request data to json object (for sending  to the plot-data function as a parameter later)
    request_data = request.data
    json_string = request_data.decode('utf8').replace("'", '"')
    request_json = json.loads(json_string)

    # Connect to the  bucket
    client = storage.Client(project='cloud-map-reduce')
    bucket = client.bucket('plot-bucket')
    link = request_json['message']
    summFileName = link.split("/")[-1]
    blob = bucket.blob(summFileName + '.png')
    project_id = "cloud-map-reduce"

    # headers to avoid cross origin error.
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        #connect to redis
        redis_host = os.environ.get('REDISHOST', 'localhost')
        redis_port = int(os.environ.get('REDISPORT', 6379))
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

        #check in cache for cached requests, if not present fetch the data from url and create list of sentence lengths and save to KV store and hit the plot-data function.
        if redis_client.exists(link) == 0:
            f = urlopen(link)
            myfile = f.read()
            myfile = myfile.decode('latin-1')
            # fetch data and split according to  period and add length of the sentence to data list.
            data  = []
            sentences = myfile.split(".")
            for line in sentences:
                data.append(len(line))
            #json_data = json.dumps(data, default=serialize_sets)

            # Convert data  into json   and set the json object into  memorystore
            json_data = json.dumps(data)
            redis_client.set(link, json_data)
        
            # call the second cloud fucntion and pass the url (as a json object) in the parameters
            r = requests.post('https://us-central1-cloud-map-reduce.cloudfunctions.net/plot-data', json=request_json)
            
            return (redis_client.get(link), 200, headers)
        else:
            #If  reuqest is cached,  get the image from the url path found from cache and return to front end.
            url = redis_client.get(link)
            return (url, 200, headers)
    except Exception as e:
        return "exception" + str(e)
