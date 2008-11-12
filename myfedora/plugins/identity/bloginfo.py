from myfedora.model import Blogs, DBSession
import logging

log = logging.getLogger(__name__)

def get_metadata(username):
    h = 'http://planet.fedoraproject.org/images/heads/default.png'
    burl = None
    
    try:
        blog = DBSession.query(Blogs).filter(Blogs.user_name==username).first()
    except:
        blog = None
        
    if blog:
        hb = blog.hackergotchi_url
        if hb:
            h = hb
        burl = blog.blog_url
        
    return {'hackergotchi_url': h, 'blog_url': burl}

def add_metadata(identity):
    try:
        name = identity['person']['username']
        blog = get_metadata(name)
        
        identity['person'].update(blog)
        
    except Exception, e:
        log.warning(e)