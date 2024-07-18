from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from urllib.parse import urlunparse

import bs4

class YoutubeEMBStat():

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def getEmbUrlBase():
        return  "https://www.youtube.com/embed/"
    
    @staticmethod
    def getIframeWidth560():
        return "560"
    
    @staticmethod
    def getIframeHeight315():
        return "315"
    
    @staticmethod
    def getIframeTitle():
        return "Sample Recomend"
    
    @staticmethod
    def getIframeFrameborder():
        return "0"
    
    @staticmethod
    def getIframeAllow():
        return "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen *"


class YoutubeURLUtile():

    def __init__(self) -> None:
        pass

    @staticmethod
    def elminateYOutubeVideoID(youtubeURL):
        splited = youtubeURL.split("=")
        videoID = splited[1]
        return videoID
    
    @staticmethod
    def build_emb_url(videoID):
        emBase = YoutubeEMBStat.getEmbUrlBase()
        return emBase + videoID


def buildEmbIframeTag(youtube_emb_url):
    soup = bs4.BeautifulSoup('', 'html.parser')
    iframe_tag = soup.new_tag("iframe")
    iframe_tag["width"] = YoutubeEMBStat.getIframeWidth560()
    iframe_tag["height"] = YoutubeEMBStat.getIframeHeight315()
    iframe_tag["src"] = youtube_emb_url
    iframe_tag["title"] = YoutubeEMBStat.getIframeTitle()
    iframe_tag["frameborder"] = YoutubeEMBStat.getIframeFrameborder()
    iframe_tag["allow"] = YoutubeEMBStat.getIframeAllow()
    iframe_tag_str = iframe_tag.decode()
    return iframe_tag_str


class BingImageStat():
    def __init__(self) -> None:
        pass

    @staticmethod
    def getImageSize400():
        return "400"
    
    @staticmethod
    def getImageSize200():
        return "200"
    
    @staticmethod
    def getImageSize300():
        return "300"

    @staticmethod
    def getBingDomain():
        return "tse2.mm.bing.net"
    
    @staticmethod
    def getBingImagePath():
        return "/th"
    
    @staticmethod
    def getHttpsSchema():
        return "https"


def build_image_url(artistname,image_size):

    def __build_param(artistname,image_size):
        total = []
        a = "q=%s+spotify" % artistname
        total.append(a)
        b = "w=%s" % image_size
        total.append(b)
        c = "h=%s" % image_size
        total.append(c)
        d = "c=7&rs=1&p=0&dpr=1&pid=1.7&mkt=en-US&adlt=on"
        total.append(d)
        _ress = "&".join(total)
        #print(_ress)
        return _ress
    param_part = __build_param(artistname,image_size)
    schema = BingImageStat.getHttpsSchema()
    domain = BingImageStat.getBingDomain()
    path = BingImageStat.getBingImagePath()
    u = urlunparse((
        schema, 
        domain, 
        path, 
        None, 
        param_part, 
        None
    ))
    return u
    
def build_img_youtube_url_atag(youtube_url):
    _youtube_video_id =YoutubeURLUtile.elminateYOutubeVideoID(youtube_url)
    img_url = "https://img.youtube.com/vi/"+_youtube_video_id+"/mqdefault.jpg"
    emb_url = YoutubeURLUtile.build_emb_url(_youtube_video_id)
    _d={}
    _d["img_url"] = img_url
    _d["emb_url"] = emb_url
    return _d




class UnitilConst():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_NA():
        return "N/A"


class Neo4jResultHelper():
    def __init__(self) -> None:
        pass    
    @staticmethod
    def build_find_neighbor_disp(_result_neo4j_obj):
        _result_ =[]
        for _rec in _result_neo4j_obj:
            _record_d={}
            artsitname=  _rec.get("artsitname")
            if artsitname != None:
                _record_d["artsitname_ja"] = artsitname
            else:
                _record_d["artsitname_ja"] = UnitilConst.get_NA()
            
            ### da eliminate
            da = _rec.get("da")
            artist_name_kakko_none = da.get("artist_name_kakko_none")
            if artist_name_kakko_none != None:
                _record_d["artist_name_kakko_none_en"] = artist_name_kakko_none
                _image_str = build_image_url(artist_name_kakko_none,BingImageStat.getImageSize400())
                _record_d["artist_image_url"] = _image_str
            else:
                _record_d["artist_name_kakko_none_en"] = UnitilConst.get_NA()
                _record_d["artist_image_url"] = UnitilConst.get_NA()
            
            artistID = da.get("artistID")
            if artistID != None:
                _record_d["artistID"] = artistID
            else:
                _record_d["artistID"] = UnitilConst.get_NA()

            # URL COLL ekiminate
            url_coll = _rec.get("url_coll")
            _resli=[]
            for _indexx,_reinnn in enumerate(url_coll):
                if _indexx ==3: break
                _url_record={}
                artistUrlID = _reinnn.get("artistUrlID")
                url = _reinnn.get("url")
                _url_record["artistUrlID"]  =artistUrlID
                _url_record["url"]  =url
                _resli.append(_url_record)
            _record_d["artist_urls"] = _resli

            name_vari_coll = _rec.get("name_vari_coll")
            _res_name_li=[]
            for _indexx,_name_vari in enumerate(name_vari_coll):
                if _indexx ==3 :break
                #print(_name_vari)
                _name_record={}
                _name_record["artistNmaeVariationID"]  =_name_vari.get("artistNmaeVariationID")
                _name_record["nameVariation"]  =_name_vari.get("nameVariation")
                _res_name_li.append(_name_record)
            
            _record_d["artist_name_variation"] = _res_name_li
            
            alias_coll =  _rec.get("alias_coll")
            alias_li =[]
            for _indexx,_alias in enumerate(alias_coll):
                if _indexx ==3: break 
                _record_alias={}
                _record_alias["artistAliasID"] = _alias.get("artistAliasID")
                _record_alias["alias"] = _alias.get("alias")
                alias_li.append(_record_alias)
            _record_d["artist_alias"] = alias_li
            _result_.append(_record_d)
        return _result_
    
    @staticmethod
    def build_artist_detail_and_release_disp(_result_neo4j_obj):
        _result_ =[]
        for _rec in _result_neo4j_obj:
            _record_d={}
            
            ### da eliminate
            da = _rec.get("discigs_artist")
            artist_name_kakko_none = da.get("artist_name_kakko_none")
            if artist_name_kakko_none != None:
                _record_d["artist_name_kakko_none_en"] = artist_name_kakko_none
                _image_str = build_image_url(artist_name_kakko_none,BingImageStat.getImageSize400())
                _record_d["artist_image_url"] = _image_str
            else:
                _record_d["artist_name_kakko_none_en"] = UnitilConst.get_NA()
                _record_d["artist_image_url"] = UnitilConst.get_NA()
            
            artistID = da.get("artistID")
            if artistID != None:
                _record_d["artistID"] = artistID
            else:
                _record_d["artistID"] = UnitilConst.get_NA()

            artist_name_trance_remove_kakko_ja = da.get("artist_name_trance_remove_kakko")
            if artist_name_trance_remove_kakko_ja != None:
                _record_d["artist_name_trance_remove_kakko_ja"] = artist_name_trance_remove_kakko_ja
            else:
                _record_d["artist_name_trance_remove_kakko_ja"] = UnitilConst.get_NA()

            # URL COLL ekiminate
            url_coll = _rec.get("url_coll")
            _resli=[]
            for _reinnn in url_coll:
                _url_record={}
                artistUrlID = _reinnn.get("artistUrlID")
                url = _reinnn.get("url")
                _url_record["artistUrlID"]  =artistUrlID
                _url_record["url"]  =url
                _resli.append(_url_record)
            _record_d["artist_urls"] = _resli

            name_vari_coll = _rec.get("name_vari_coll")
            _res_name_li=[]
            for _name_vari in name_vari_coll:
                _name_record={}
                _name_record["artistNmaeVariationID"]  =_name_vari.get("artistNmaeVariationID")
                _name_record["nameVariation"]  =_name_vari.get("nameVariation")
                _res_name_li.append(_name_record)
            
            _record_d["artist_name_variation"] = _res_name_li
            
            alias_coll =  _rec.get("alias_coll")
            alias_li =[]
            for _alias in alias_coll:
                _record_alias={}
                _record_alias["artistAliasID"] = _alias.get("artistAliasID")
                _record_alias["alias"] = _alias.get("alias")
                alias_li.append(_record_alias)
            _record_d["artist_alias"] = alias_li
           
            artist_detail = _rec.get("artist_detail")
            content_en = artist_detail.get("content_en")
            if content_en != None:
                _record_d["content_en"] = content_en
            else:
                _record_d["content_en"] = UnitilConst.get_NA()
            
            discigs_relases = _rec.get("discigs_relases")
            _relsease_res =[]
            for _release in discigs_relases:
                _relsease_inner_rec ={}
                _relsease_inner_rec["discogs_artist_id"] = _release.get("artist_id")
                _relsease_inner_rec["discogs_releaseID"] = _release.get("releaseID")
                _relsease_inner_rec["discogs_release_tile"] = _release.get("release_tile")
                _relsease_inner_rec["artist_name_kakko_none_en"] = _release.get("artist_name_kakko_none")
                _relsease_inner_rec["artist_name_trance_remove_kakko_ja"] = _release.get("artist_name_trance_remove_kakko")
                youtube_url = _release.get("youtube_url")
                if youtube_url != None:
                    _yoyutube_img_url = build_img_youtube_url_atag(youtube_url)

                    _relsease_inner_rec["release_video_img_url"] = _yoyutube_img_url
                else:
                    _relsease_inner_rec["release_video_img_url"] = UnitilConst.get_NA()
                _relsease_res.append(_relsease_inner_rec)
            _record_d["releases"] = _relsease_res
            _result_.append(_record_d)
        
        return _result_
           
    @staticmethod
    def build_artist_from_keyword_disp(_result_neo4j_obj):
        
        _resutls=[]
        for _rec in _result_neo4j_obj:
            _record_d={}
        
            da = _rec.get("da")
            artist_name_kakko_none = da.get("artist_name_kakko_none")
            if artist_name_kakko_none != None:
                _record_d["artist_name_kakko_none_en"] = artist_name_kakko_none
                _image_str = build_image_url(artist_name_kakko_none,BingImageStat.getImageSize400())
                _record_d["artist_image_url"] = _image_str
            else:
                _record_d["artist_name_kakko_none_en"] = UnitilConst.get_NA()
                _record_d["artist_image_url"] = UnitilConst.get_NA()
            
            artistID = da.get("artistID")
            if artistID != None:
                _record_d["artistID"] = artistID
            else:
                _record_d["artistID"] = UnitilConst.get_NA()

            artist_name_trance_remove_kakko_ja = da.get("artist_name_trance_remove_kakko")
            if artist_name_trance_remove_kakko_ja != None:
                _record_d["artist_name_trance_remove_kakko_ja"] = artist_name_trance_remove_kakko_ja
            else:
                _record_d["artist_name_trance_remove_kakko_ja"] = UnitilConst.get_NA()
            # URL COLL ekiminate
            url_coll = _rec.get("url_coll")
            _resli=[]

            for _indexx ,_reinnn in enumerate(url_coll):
                if _indexx ==3:
                    if len(url_coll) >3:
                        _url_record={}        
                        _url_record["artistUrlID"]  ="artist_url_last"
                        _url_record["url"]  ="MORE............."
                        _resli.append(_url_record)
                    break
                _url_record={}
                artistUrlID = _reinnn.get("artistUrlID")
                url = _reinnn.get("url")
                _url_record["artistUrlID"]  =artistUrlID
                _url_record["url"]  =url
                _resli.append(_url_record)
            _record_d["artist_urls"] = _resli
            #name vari
            name_vari_coll = _rec.get("name_vari_coll")
            _res_name_li=[]
            for _indexx,_name_vari in enumerate(name_vari_coll):
                if _indexx ==3:
                    if len(name_vari_coll) >3:
                        _name_record={}
                        _name_record["artistNmaeVariationID"]  ="artist_Name_vari_last"
                        _name_record["nameVariation"]  ="MORE............."
                        _res_name_li.append(_name_record)
                    break
                #print(_name_vari)
                _name_record={}
                _name_record["artistNmaeVariationID"]  =_name_vari.get("artistNmaeVariationID")
                _name_record["nameVariation"]  =_name_vari.get("nameVariation")
                _res_name_li.append(_name_record)
            _record_d["artist_name_variation"] = _res_name_li
            #alias_coll
            alias_coll =  _rec.get("alias_coll")
            alias_li =[]
            for _indexx,_alias in enumerate(alias_coll):
                if _indexx ==3:
                    if len(alias_coll) >3:
                        _record_alias={}
                        _record_alias["artistAliasID"]  ="artist_Alias_last"
                        _record_alias["alias"]  ="MORE............."
                        alias_li.append(_record_alias)
                    break
                _record_alias={}
                _record_alias["artistAliasID"] = _alias.get("artistAliasID")
                _record_alias["alias"] = _alias.get("alias")
                alias_li.append(_record_alias)
            _record_d["artist_alias"] = alias_li
            _resutls.append(_record_d)

        return _resutls
    

class App():
    def __init__(self,uri, user, password) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    

    def find_neighbor(self,surface) -> list:
        result_neighbor=[]
        with self.driver.session() as session:
            try:
                result_neighbor = session.execute_read(self._find_neighbor, surface)
            except Exception as e:
                print(e)
                raise ServiceUnavailable()
            finally:
                self.close()
        return result_neighbor
    
    def get_artist_detail_and_releases(self,surface):
        result_artuist_detail=[]
        with self.driver.session() as session:
            try:
                result_artuist_detail = session.execute_read(self._get_artist_detail, surface)
            except Exception as e:
                print(e)
                raise ServiceUnavailable()
            finally:
                self.close()
        return result_artuist_detail
    
    def get_artist_main_disp(self,keyword_list):
        result_main_disp=[]
        with self.driver.session() as session:
            try:
                result_main_disp = session.execute_read(self._get_artist_main_disp, keyword_list)
            except Exception as e:
                print(e)
                raise ServiceUnavailable()
            finally:
                self.close()
        return result_main_disp
    
    

    @staticmethod
    def _find_neighbor(tx,surface):
        query =(
            '''
                MATCH (w:WORD_2_VEC_NODE)-[wr:WORD_2_VEC_REL*..2]-(ww:WORD_2_VEC_NODE)-[w2da:WORD_2_DISCOGS_ARIST]-(da:DISCOGS_ARTIST) WHERE w.surface=$surface
                WITH DISTINCT da.artist_name_trance_remove_kakko as discogs_artist
                WITH discogs_artist, rand() as r ORDER BY r DESC LIMIT 50
                UNWIND discogs_artist as discogsartistname
                CALL{
                    WITH discogsartistname
                    MATCH (da:DISCOGS_ARTIST)-[url:DISCOGS_ARTIST_URL_REL]-(url_res) WHERE da.artist_name_trance_remove_kakko = discogsartistname
                    WITH DISTINCT da.artist_name_trance_remove_kakko as discogsname1,collect(url_res) as url_coll
                    MATCH (da:DISCOGS_ARTIST)-[name_vari:DISCOGS_ARTIST_NAMEVARIATION_REL]-(name_vari_res) 
                    WHERE da.artist_name_trance_remove_kakko = discogsname1
                    WITH DISTINCT da.artist_name_trance_remove_kakko as discogsname2,da,url_coll, collect(name_vari_res) as name_vari_coll
                    MATCH (da:DISCOGS_ARTIST)-[alias_rel:DISCOGS_ARTIST_ALIAS_REL]-(alias)
                    WHERE da.artist_name_trance_remove_kakko = discogsname2
                    RETURN DISTINCT da.artist_name_trance_remove_kakko as artsitname , da,name_vari_coll,url_coll,collect(alias) as alias_coll 
                }
                RETURN  da.artist_name_trance_remove_kakko as artsitname,da,name_vari_coll,url_coll,alias_coll
            '''
        )
        try:
            result = tx.run(query, surface=surface)
        except Exception as e:
            raise ServiceUnavailable(e)

        res = Neo4jResultHelper.build_find_neighbor_disp(result)
        return res

    @staticmethod
    def _get_artist_detail(tx,surface):
        query =(
            '''
                MATCH (da:DISCOGS_ARTIST)-[url:DISCOGS_ARTIST_URL_REL]-(url_res) WHERE da.artist_name_trance_remove_kakko = $surface
                WITH DISTINCT da.artist_name_trance_remove_kakko as discogsname1,collect(url_res) as url_coll
                MATCH (da:DISCOGS_ARTIST)-[name_vari:DISCOGS_ARTIST_NAMEVARIATION_REL]-(name_vari_res) 
                WHERE da.artist_name_trance_remove_kakko = discogsname1
                WITH DISTINCT da.artist_name_trance_remove_kakko as discogsname2,da,url_coll, collect(name_vari_res) as name_vari_coll
                MATCH (da:DISCOGS_ARTIST)-[alias_rel:DISCOGS_ARTIST_ALIAS_REL]-(alias)
                WHERE da.artist_name_trance_remove_kakko = discogsname2
                WITH DISTINCT da.artist_name_trance_remove_kakko as artsitname , da,name_vari_coll,url_coll,collect(alias) as alias_coll
                MATCH (da:DISCOGS_ARTIST)-[detail_rel:DISCOGS_ARTIST_DETAIL_REL]-(artist_detail)
                WHERE da.artist_name_trance_remove_kakko = artsitname
                WITH artsitname,da,artist_detail,name_vari_coll,url_coll,alias_coll
                MATCH (da:DISCOGS_ARTIST)-[da2dr:DISCOGS_ARTIST_2_DISCOGS_RELSEASE]-(darr:DISCOGS_ARTIST_RELEASE) WHERE da.artist_name_trance_remove_kakko = artsitname
                WITH da as discigs_artist, darr as releases , rand() as r,artist_detail,name_vari_coll,url_coll,alias_coll
                ORDER BY r
                LIMIT 10
                RETURN discigs_artist,artist_detail,name_vari_coll,url_coll,alias_coll,collect(releases) as discigs_relases
            '''
        )
        result=None
        try:
             result = tx.run(query, surface=surface)
        except Exception as e:
            raise ServiceUnavailable(e)

        res = Neo4jResultHelper.build_artist_detail_and_release_disp(result)
        return res

    @staticmethod
    def _get_artist_main_disp(tx,keyword_list):
        result=None
        query =(
            '''
                MATCH (da:DISCOGS_ARTIST)-[sadtail:DISCOGS_ARTIST_DETAIL_REL]-(res) WHERE da.artist_name_trance_remove_kakko in $keyword_list
                WITH DISTINCT da.artist_name_trance_remove_kakko as target_artist_name
                UNWIND target_artist_name as artist_names
                CALL{
                    WITH artist_names
                    MATCH (da:DISCOGS_ARTIST)-[url:DISCOGS_ARTIST_URL_REL]-(url_res) WHERE da.artist_name_trance_remove_kakko = artist_names
                    WITH DISTINCT da.artist_name_trance_remove_kakko as discogsname1,collect(url_res) as url_coll
                    MATCH (da:DISCOGS_ARTIST)-[name_vari:DISCOGS_ARTIST_NAMEVARIATION_REL]-(name_vari_res) 
                    WHERE da.artist_name_trance_remove_kakko = discogsname1
                    WITH DISTINCT da.artist_name_trance_remove_kakko as discogsname2,da,url_coll, collect(name_vari_res) as name_vari_coll
                    MATCH (da:DISCOGS_ARTIST)-[alias_rel:DISCOGS_ARTIST_ALIAS_REL]-(alias)
                    WHERE da.artist_name_trance_remove_kakko = discogsname2
                    RETURN DISTINCT da.artist_name_trance_remove_kakko as artsitname , da,name_vari_coll,url_coll,collect(alias) as alias_coll 
                }
                RETURN  da.artist_name_trance_remove_kakko as artsitname,da,name_vari_coll,url_coll,alias_coll
            '''
        )
        try:
             result = tx.run(query, keyword_list=keyword_list)
        except Exception as e:
            raise ServiceUnavailable(e)

        res = Neo4jResultHelper.build_artist_from_keyword_disp(result)
        return res
        