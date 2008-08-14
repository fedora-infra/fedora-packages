from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from myfedora.model import metadata

import datetime
from sqlalchemy import ForeignKey

blog_table = Table('blogs', metadata,
    Column('user_name', Unicode(16), primary_key=True),
    Column('blog_url', Unicode(255)),
    Column('hackergotchi_url', Unicode(255)),
    Column('modified', TIMESTAMP, default=datetime.datetime.now())
)


# identity model
class Blogs(object):
    def __repr__(self):
        return '<Blog: user=%s url=%s hackergotchi=%s' % (self.user_name, 
                                                          self.blog_url,
                                                          self.hackergotchi_url)
    
mapper(Blogs, blog_table)