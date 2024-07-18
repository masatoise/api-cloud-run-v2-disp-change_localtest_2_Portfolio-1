
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


from urllib.parse import urlunparse

class BingImageStat():
    def __init__(self) -> None:
        pass

    @staticmethod
    def getImageSize():
        return "200"

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
    


