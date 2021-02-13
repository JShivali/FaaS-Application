# FaaS-Application


# Design Details:
1. User interface:
I used react.js for the front-end of the project. The web page takes the url
of the book. The user can paste the url in the textbox or select a book from the drop
down.
2. Cache:
I have used the cloud Memorystore API (Redis) which is a low latency
in-memory service provided by Google. I used this for caching requests. The request url
is used as the key and value will be the url path to the graph stored in the bucket.
3. Backend:
The project has two cloud functions called fetch-data and plot-data. I have
used python 3.8 for implementing these functions. Both the functions are HTTP
triggered. The fetch-data function is used to get the data from the specified url and
create a list of lengths of sentences. I have used cloud memorystore(Redis) to share
data between functions (as it would be faster than conventional storage options like
buckets) The plot-data function uses the list of sentence lengths and plots the histogram.
This histogram is stored in google cloud storage bucket called plot-bucket. The url of the
plot is updated in the Memorystore for caching.

# WorkFlow
The front end sends the url of the book to the fetch-data function. The fetch-data checks the cache to see if the request is cached. If the request is not cached, the function reads the data from url, creates a list of sentence lengths. The function then writes to the cache (key- url and value- list of sentences lengths) and triggers the plot-data function. If the request is already cached, the function reads the url of the plot from the cache and returns directly to the UI, bypassing parsing and plotting of data.

The plot-data function reads data from the cache and creates a histogram using matplotlib and stores the plot in a bucket. The function then updates the cache with the publicly accessible url for thestored plot(in bucket) and returns it to the UI

# Cloud APIs used:
1. Cloud Functions
2. Cloud Storage
3. Cloud Memorystore(Redis) - caching
4. Firebase hosting

# GCloud logs:
Cloud function execution screenshots and other logs can be found in the  reports_and_logs subfolder 

