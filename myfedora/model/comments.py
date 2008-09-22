from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from myfedora.model import metadata

import datetime
from sqlalchemy import ForeignKey

comments_table = Table('comments', metadata,
    Column('data_key', Unicode(255), primary_key = True),
    Column('user_name', Unicode(16)),
    Column('app_display_name', Unicode(128)),
    Column('comment', Unicode(255)),
    Column('comment_thread_url', Unicode(255)),
    Column('timestamp', TIMESTAMP, default=datetime.datetime.now())
)

class Comments(object):
    def __repr__(self):
        return '<Comment: At %s %s wrote "%s" on %s>' (str(self.timestamp),
                                                       self.user_name, 
                                                       self.comment,
                                                       self.app_display_name)
    
mapper(Comments, comments_table)