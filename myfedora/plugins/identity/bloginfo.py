from myfedora.model import Blogs, DBSession

def get_metadata(username):
    h = 'http://planet.fedoraproject.org/images/heads/default.png'
    burl = None
    blog = DBSession.query(Blogs).filter(Blogs.user_name==username).first()
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
        print e