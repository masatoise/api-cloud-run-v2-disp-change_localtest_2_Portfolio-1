
class ElasticResultEmptyError(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg

MSG = '''
    Suggest Reslut ==>> None
'''

def __is_none(_targettt):
    if _targettt == None:
        return True
    else:
        return False


def get_elastic_suggest_result(_result_obj):
    hits = _result_obj.get("hits")
    if __is_none(hits):
        raise ElasticResultEmptyError(MSG)
    hitsss = hits.get("hits")
    if __is_none(hitsss):
        raise ElasticResultEmptyError(MSG)
    
    if not isinstance(hitsss,list):
        if len(hitsss) == 0:
           raise ElasticResultEmptyError(MSG)
    
    return hitsss


def get_elastic_artist_disp_result(_result_obj):
    
    def build_discogs_artsit_url(_aid=""):
        base = "https://www.discogs.com/ja/artist/"
        url = base + _aid
        return url
    
    hits = _result_obj.get("hits")
    if __is_none(hits):
        raise ElasticResultEmptyError(MSG)
    hitsss = hits.get("hits")
    if __is_none(hitsss):
        raise ElasticResultEmptyError(MSG)
    
    if not isinstance(hitsss,list):
        raise ElasticResultEmptyError(MSG)
    
    if len(hitsss) == 0:            
        raise ElasticResultEmptyError(MSG)
    
    _res_dict_tmp = hitsss[0]
    _artist_disp_dict = _res_dict_tmp.get("_source")
    discogs_origine_artist_id = _artist_disp_dict.get("discogs_origine_artist_id")
    discogs_artsit_url = build_discogs_artsit_url(_aid=discogs_origine_artist_id)
    _artist_disp_dict.update({"main_artist_url":discogs_artsit_url})
    if _artist_disp_dict == None:
        raise ElasticResultEmptyError(MSG)
    
    return _artist_disp_dict



def get_init_disp_artist_result(_result_obj):
    hits = _result_obj.get("hits")
    if __is_none(hits):
        raise ElasticResultEmptyError(MSG)
    hitsss = hits.get("hits")
    if __is_none(hitsss):
        raise ElasticResultEmptyError(MSG)
    _res=[]
    for _record in hitsss:
        #print(hitsss)
        _rexord_dict = _record.get("_source")
        if _rexord_dict == None:
            raise ElasticResultEmptyError(MSG)
        _res.append(_rexord_dict)
        #print()
        #print(_rexord_dict)
    return _res

    