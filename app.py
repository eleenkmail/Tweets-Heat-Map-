from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

# create client for elasticsearch 
es = Elasticsearch("http://localhost:9200")

app=Flask(__name__,template_folder='templates')


# query return documents from elasticsearch
def query(body):

    # body of the query
    query_body =  {
        'size' : 500,
        "query":{
        "bool": {
            "must": [
            {
                "match" : {
                "text":{
                "query":body['text'] 
            }}},
            {
            "range": {
            "date": {
            "time_zone": "+00:00",  
            "gte": body['gte'] , 
            "lte": body['lte']                  
        }}},
            
            {
            "geo_bounding_box": {
                "location": {
                
                "top_left": {
                    "lat": body['top_lat'],
                    "lon": body['left_lon']
                },
                "bottom_right": {
                    "lat": body['buttom_lat'],
                    "lon": body['right_lon']
                }
                }
            }
            }   
            ] }}}

    # search for query
    response = es.search(
      index = 'tweets',
      body = query_body)

    # max score to normalize all scores
    max_score = response["hits"]["max_score"]
    # all documents returned 
    hits = response["hits"]["hits"]

    # if there is no data returned then return empty dictionary
    if (max_score == None)  and (hits== []):
        return [None, None]

    # if there is data returned then return all documents and max score
    else: 
        return [float(response["hits"]["max_score"]), hits]




@app.route("/")
def home():
    return render_template('index.html' )



@app.route('/get', methods=['GET'])
def index():

    #data to search with
    body = {

        "text" : request.args.get("text"),
        "top_lat" : float(request.args.get("tlat")),
        "buttom_lat" :float(request.args.get("blat")),
        "left_lon" : float(request.args.get("llon")),
        "right_lon" : float(request.args.get("rlon")), 
        "gte": request.args.get("gte"),  # start date
        "lte": request.args.get("lte"),  # end date
    }

    
    # do the query function
    response = query(body)

    #if there is no data returned
    if response[0] == None:
        return {}

    # data be returned with shape {doc_id : { 'lat': value, 'lng': value, 'score': value}, {doc_id : {.....}}}
    dict = { }

    for doc in response[1]:
        dict[doc['_id']] = {'lat' : doc['_source']['location']['coordinates'][1],\
             'lng': doc['_source']['location']['coordinates'][0], 'score' : doc['_score']/ response[0]}

    return dict



if __name__ == '__main__':
    app.run(debug=True)
