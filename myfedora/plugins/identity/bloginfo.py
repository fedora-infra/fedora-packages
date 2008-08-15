from myfedora.model import Blogs, DBSession

def add_metadata(identity):
    try:
        name = identity['person']['username']
        blog = DBSession.query(Blogs).filter(Blogs.user_name==name).first()
        
        identity['person']['blog_url'] = blog.blog_url
        h = blog.hackergotchi_url
        if not h:
            h = 'http://planet.fedoraproject.org/images/heads/default.png'
        identity['person']['hackergotchi_url'] = h
    except Exception, e:
        print e