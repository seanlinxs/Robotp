import re
import pycouchdb
from urllib.parse import urlparse


def get_server(base_url):
    parsed_url = urlparse(base_url)

    if len(parsed_url.netloc) == 0:
        return (None, "Invalid url: {0}".format(mask_passwd(base_url)))
    
    try:
        server = pycouchdb.Server(base_url=base_url, verify=True)
        info = server.info()
        return (server, None)
    except Exception as e:
        return (None, "Connecting failed: {0} - {1}".format(mask_passwd(base_url), e))

def mask_passwd(url):
    p = re.compile(r":[^:]*@")
    return p.sub(":*****@", url)
