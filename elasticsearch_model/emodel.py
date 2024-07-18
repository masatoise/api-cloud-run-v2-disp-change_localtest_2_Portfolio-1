from elasticsearch8 import Elasticsearch

MSG = '''
    Elasticproccc  ==>> Errorr
'''

MSG_CON = '''
    ElasticCONNN  ==>> Errorr
'''

class ElasticConnectionSomthingError(Exception):
    def __init__(self, msg,*args: object) -> None:
        super().__init__(*args)
        self._msg = msg

    def __str__(self):
        return self._msg


class ElasticProcSomthingError(Exception):
    def __init__(self, msg,*args: object) -> None:
        super().__init__(*args)
        self._msg = msg

    def __str__(self):
        return self._msg

INDEX ="recomend_discogs_release_suggest"


class ElasticIndex():
    @staticmethod
    def recomend_discogs_release_suggest_index():
        return "recomend_discogs_release_suggest"
    
    @staticmethod
    def recomend_discogs_release_disp():
        return "recomend_discogs_release_disp"
    
    @staticmethod
    def display_artist_info():
        return "display_artist_info"
    
    @staticmethod
    def init_display_artist():
        return "init_display_artist"
    
    @staticmethod
    def en_wiki_elasticsearch():
        return "en_wiki_ela"
    

class QueryBuilder():
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def suggest_query_dict(_target=""):
        _target = _target
        return { 
                    #"size":0,
                    "query": { 
                        "bool": { 
                        "should": [ 
                            { 
                                "match": { 
                                    "artist_name_trance_remove_kakko.suggest": { 
                                    "query": _target 
                                    } 
                                } 
                            },
                            { 
                                "match": { 
                                    "artist_name_trance_remove_kakko.readingform": { 
                                    "query": _target,
                                    "operator": "and" 
                                    } 
                                } 
                            } 
                        ] 
                        } 
                    },
                    "aggs": { 
                        "keywords": { 
                            "terms": { 
                                "field": "artist_name_trance_remove_kakko",
                                "order": { 
                                "_count": "desc" 
                                },
                                "size":"10" 
                            } 
                        } 
                    } 
                }
    
    @staticmethod
    def suggest_query_dict_none_aggr(_target=""):
        _target = _target
        return { 
                    "query":{
                        "bool":{
                            "must":[
                                {
                                    "match": {
                                        "corpus": 1
                                    }
                                },
                                {
                                    "bool": {
                                        "should": [
                                            { 
                                                "match": { 
                                                    "artist_name_trance_remove_kakko.suggest": { 
                                                        "query": _target 
                                                    } 
                                                } 
                                            },
                                            { 
                                                "match": { 
                                                    "artist_name_trance_remove_kakko.readingform": { 
                                                        "query": _target,
                                                        "operator": "and" 
                                                    } 
                                                } 
                                            } 
                                        ] 
                                    }
                                }
                            ]
                        }
                    }
                } 
    
    @staticmethod
    def disp_artist_query_by_aritst_id(_discogs_origine_artist_id="",_artist_id=""):
        artist_id = _artist_id
        discogs_origine_artist_id = _discogs_origine_artist_id
        return{
                "query":{
                    "bool":{
                        "should":[
                            {"match":{"discogs_origine_artist_id":discogs_origine_artist_id}},
                            {"match":{"artist_id":artist_id}}
                        ],
                        "minimum_should_match" : 1
                    }
                }
            }
    
    @staticmethod
    def disp_artist_init_query_by_display_ids(init_disp_ids=[7, 4, 8, 9, 2, 0, 6, 3, 1, 5]):
        return {
            "query":{
                "terms":{
                    "init_disp_id":init_disp_ids
                }
            }
        }
    
    @staticmethod
    def disp_artist_detail_en_wiki(search_artsit_name,discogs_artsit_name):
        '''
        "Robert Hood"
        '''
        return {
            "query":{
                "bool":{
                    "must":[
                        {
                            "term":{
                                "searchTitle.keyword":search_artsit_name
                            }
                        },
                        {
                            "term":{
                                "title.keyword":discogs_artsit_name
                            }
                        },
                        {
                            "exists": {
                                "field": "text"
                            }
                        }
                    ]
                }
            }
        }


class ElasticSearchDataAccess():
    def __init__(self) -> None:
        self.elastic_host ="http://localhost:9200"
    def conn_ela(self):

        es =None
        try:
            es = Elasticsearch(self.elastic_host)
        except Exception as ecse:
            raise ElasticConnectionSomthingError(MSG_CON)
        return es
    
    def close_ela(self,es_obj):
        es_obj.close()

    def search_suggest(self,_q):
        es = self.conn_ela()

        result = {}
        try:
            result = es.search(index=INDEX, body=_q,size=10)
        except Exception as e:
            raise ElasticProcSomthingError(MSG)
        finally:
            self.close_ela(es)
        return result

    def search_exec(self,_q,index,size=10):
        es = self.conn_ela()

        result = {}
        try:
            result = es.search(index=index, body=_q,size=size)
        except Exception as e:
            raise ElasticProcSomthingError(MSG)
        finally:
            self.close_ela(es)
        return result

