from flask import Flask,jsonify,request
from elasticsearch_model.emodel import QueryBuilder as qb, ElasticSearchDataAccess
from elasticsearch_model.emodel import ElasticConnectionSomthingError,ElasticProcSomthingError
from elasticsearch_model.helper_for_disp import ElasticResultEmptyError,get_elastic_suggest_result
from elasticsearch_model.helper_for_search import gen_random_int_no_dup,get_target_artist_list

from neo4j_model.nmodel import App

from werkzeug.exceptions import BadRequest,InternalServerError,Unauthorized,Forbidden,NotFound

from flask_cors import CORS

import os
import json


NEO4J_CREDENTIAL = os.environ.get("NEO4J_CREDENTIAL")
NEO4J_CREDENTIAL = json.loads(NEO4J_CREDENTIAL)
NEO4J_URI = NEO4J_CREDENTIAL.get("NEO4J_URI")
NEO4J_USER=NEO4J_CREDENTIAL.get("NEO4J_USER")
NEO4J_PASSWORD = NEO4J_CREDENTIAL.get("NEO4J_PASSWORD")


app = Flask(__name__)
CORS(app)

#########
#ERROR HAndling

app.errorhandler(NotFound)
def not_found(e):
    return "handling NotFound"

app.errorhandler(BadRequest)
def not_found(e):
    return "handling BadRequest"

app.errorhandler(Unauthorized)
def not_found(e):
    return "handling Unauthorized"

app.errorhandler(Forbidden)
def not_found(e):
    return "handling Forbidden"

app.errorhandler(InternalServerError)
def not_found(e):
    return "handling InternalServerError"

######
 
@app.route('/hello')
def hello():
    hello = "It is Work"
    return jsonify(hello)

@app.route('/suggest',methods=['post'])
def get_suggest():
    _get_param =  request.json
    _target_param = _get_param.get("suggest")
    if _target_param == None:
        print("PARAM NONEEEEE")
        raise BadRequest()
    elif _target_param =="":
        print("PARAM NONEEEEE")
        raise BadRequest()
        
    queryy = qb.suggest_query_dict_none_aggr(_target=_target_param)
    esda=ElasticSearchDataAccess()
    result_proc =None
    try:
        result_proc = esda.search_suggest(queryy)
    except ElasticConnectionSomthingError as ecse:
        raise InternalServerError()
    except ElasticProcSomthingError as epse:
        raise InternalServerError()

    result_li = None
    try:
        result_li = get_elastic_suggest_result(result_proc)
    except ElasticResultEmptyError as eree:
        raise InternalServerError()
    res_json_dict = {"result":result_li}
    return jsonify(res_json_dict)

@app.route('/nn_neighbor_artist',methods=['get'])
def get_neighbor_artist():
    _get_param = request.values.get("artist_name_trance_remove_kakko", "None")
    if _get_param ==None:
        raise BadRequest()
    
    neo4j_app = App(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    
    _nn_neighbor_artist_result =None
    try:

        _nn_neighbor_artist_result = neo4j_app.find_neighbor(_get_param)
    except Exception as e:
        raise InternalServerError()
    return jsonify({"nn_neighbor_artist_result":_nn_neighbor_artist_result})


@app.route('/maindisp',methods=['get'])
def get_init_disp_artist():
    _init_disp_ids = gen_random_int_no_dup()
    target_atists = get_target_artist_list(_init_disp_ids)
    neo4j_app = App(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    _main_disp_result =None
    try:
        _main_disp_result = neo4j_app.get_artist_main_disp(target_atists)
    except Exception as e:
        raise InternalServerError()
    res_main_disp = {}
    res_main_disp["result"]=_main_disp_result
    _res_jsonn = jsonify(res_main_disp)
    return _res_jsonn

@app.route('/get_artist_detail_with_releases',methods=['get'])
def get_artist_detail_with_releases():
    _get_param = request.values.get("artist_name_trance_remove_kakko", "None")
    if _get_param ==None:
        raise BadRequest()
    
    neo4j_app = App(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    
    _artist_detail_result =None
    try:
        
        _artist_detail_result = neo4j_app.get_artist_detail_and_releases(_get_param)
    except Exception as e:
        raise InternalServerError()
    _artist_detail_result = _artist_detail_result[0]
    _res_jsonn = jsonify(_artist_detail_result)
    return _res_jsonn
    
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3333)))