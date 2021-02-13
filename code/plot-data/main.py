import redis
import base64
from google.cloud import storage
import json
import os
import io
import math


def plot_data(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    import matplotlib.pyplot as plt
    
    request_json = request.get_json()
    client = storage.Client(project='cloud-map-reduce')
    bucket = client.bucket('plot-bucket')
    link = request_json['message']
    summFileName = link.split("/")[-1]
    blob = bucket.blob(summFileName + '.png')
    project_id = "cloud-map-reduce"

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        # Connect to redis  and get the intermediate data based on the url (key)
        redis_host = os.environ.get('REDISHOST', 'localhost')
        redis_port = int(os.environ.get('REDISPORT', 6379))
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
        redis_data = redis_client.get(link)
        string_data = redis_data.decode("latin-1")
        res = json.loads(string_data)

        # create bins for the plot and save it as a png in cloud storage bucket
        w = 25
        n = math.ceil((max(res) - min(res)) / w)
        print("n",n)
        plt.hist(res, bins=n,label="Sentence length distribution")
        xmin, xmax, ymin, ymax = plt.axis()
        plt.ylim(ymin,ymax)
        plt.xlim(xmin,xmax)
        plt.ylabel('number of sentences')
        plt.xlabel('sentence length')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.clf()
        plt.close()
        blob.upload_from_string(
            buf.getvalue(),
            content_type='image/png')
        blob.make_public()
        buf.close()

        #get the public url of the image uploaded to bucket and add to cache
        url = blob.public_url

        # update cache with the latest plot
        redis_client.set(link, url)

        return (url,200, headers)
    except Exception as e:
        return str(e)

