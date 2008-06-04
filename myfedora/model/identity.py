from pylons import config
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from myfedora.model import metadata

import datetime
from sqlalchemy import ForeignKey
import md5
import sha

groups_table = Table('tg_group', metadata,
    Column('group_id', Integer, primary_key=True),
    Column('group_name', Unicode(16), unique=True),
    Column('display_name', Unicode(255)),
    Column('created', DateTime, default=datetime.datetime.now)
)

users_table = Table('tg_user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', Unicode(16), unique=True),
    Column('email_address', Unicode(255), unique=True),
    Column('display_name', Unicode(255)),
    Column('password', Unicode(40)),
    Column('created', DateTime, default=datetime.datetime.now)
)

permissions_table = Table('tg_permission', metadata,
    Column('permission_id', Integer, primary_key=True),
    Column('permission_name', Unicode(16), unique=True),
    Column('description', Unicode(255))
)

user_group_table = Table('tg_user_group', metadata,
    Column('user_id', Integer, ForeignKey('tg_user.user_id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

group_permission_table = Table('tg_group_permission', metadata,
    Column('group_id', Integer, ForeignKey('tg_group.group_id',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('permission_id', Integer, ForeignKey('tg_permission.permission_id',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# identity model
class Group(object):
    """An ultra-simple group definition.
    """
    def __repr__(self):
        return '<Group: name=%s>' % self.group_name

class User(object):
    """Reasonably basic User definition. Probably would want additional
    attributes.
    """
    def __repr__(self):
        return '<User: email="%s", display name="%s">' % (
                self.email_address, self.display_name)

    def permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms
    permissions = property(permissions)

    def by_email_address(klass, email):
        """A class method that can be used to search users
        based on their email addresses since it is unique.
        """
        session = DBSession()
        return session.query(klass).filter(klass.email_address==email).first()

    by_email_address = classmethod(by_email_address)

    def by_user_name(klass, username):
        """A class method that permits to search users
        based on their user_name attribute.
        """
        session = DBSession()
        return session.query(klass).filter(klass.user_name==username).first()

    by_user_name = classmethod(by_user_name)

    def _set_password(self, password):
        """encrypts password on the fly using the encryption
        algo defined in the configuration
        """
        algorithm = config.get('authorize.hashmethod', None)
        self._password = self.__encrypt_password(algorithm, password)

    def _get_password(self):
        """returns password
        """
        return self._password

    password = property(_get_password, _set_password)

    def __encrypt_password(self, algorithm, password):
        """Hash the given password with the specified algorithm. Valid values
        for algorithm are 'md5' and 'sha1'. All other algorithm values will
        be essentially a no-op."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')

        else:
            password_8bit = password

        if "md5" == algorithm:
            hashed_password = md5.new(password_8bit).hexdigest()

        elif "sha1" == algorithm:
            hashed_password = sha.new(password_8bit).hexdigest()

        # TODO: re-add the possibility to provide own hasing algo
        # here... just get the real config...

        #elif "custom" == algorithm:
        #    custom_encryption_path = turbogears.config.get(
        #        "identity.custom_encryption", None )
        #
        #    if custom_encryption_path:
        #        custom_encryption = turbogears.util.load_class(
        #            custom_encryption_path)

        #    if custom_encryption:
        #        hashed_password = custom_encryption(password_8bit)

        # make sure the hased password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        return hashed_password

    def validate_password(self, password):
        """Check the password against existing credentials.
        """
        algorithm = config.get('authorize.hashmethod', None)
        return self.password == self.__encrypt_password(algorithm, password)

class Permission(object):
    """A relationship that determines what each Group can do
    """
    pass


mapper(User, users_table,
        properties=dict(_password=users_table.c.password))

mapper(Group, groups_table,
        properties=dict(users=relation(User,
                secondary=user_group_table, backref='groups')))

mapper(Permission, permissions_table,
        properties=dict(groups=relation(Group,
                secondary=group_permission_table, backref='permissions')))
