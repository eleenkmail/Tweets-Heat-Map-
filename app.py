from flask import Flask, render_template, request, jsonify
import json
import urllib.request
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

app=Flask(__name__,template_folder='templates')

def query(body):
    query_body =  {"query":{
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
            ]
        }}}

    response = es.search(
      index = 'tweets',
      body = query_body
        )

    hits = response["hits"]["hits"]
    return [float(response["hits"]["max_score"]), hits]



@app.route("/")
def home():
    return render_template('index.html' )


@app.route('/get', methods=['GET'])
def index2():

    body = {

        "text" : request.args.get("text"),
        "top_lat" : float(request.args.get("tlat")),
        "buttom_lat" :float(request.args.get("blat")),
        "left_lon" : float(request.args.get("llon")),
        "right_lon" : float(request.args.get("rlon")),
        "gte": request.args.get("gte"), 
        "lte": request.args.get("lte"),
    }

    

    response = query(body)


    dict = { }


    for doc in response[1]:
        dict[doc['_id']] = {'lat' : doc['_source']['location']['coordinates'][1],\
             'lng': doc['_source']['location']['coordinates'][0], 'score' : doc['_score']/ response[0]}

    return dict



if __name__ == '__main__':
    app.run(debug=True)
