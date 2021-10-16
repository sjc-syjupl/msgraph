
from .src.client_base import Client_Base
from .src.users import Users
from .src.subscriptions import Subscriptions
from .src.mail import Mail
from .src.one_note import OneNote
from .src.calendar import Calendar
from .src.contacts import Contacts
from .src.files import Files


class Client(Users, Subscriptions, Mail, OneNote, Calendar, Contacts, Files, Client_Base):
    def __init__(self, client_id=None, client_secret=None, account_id=None, tenant=None, api_version='v1.0', account_type='common', office365=False, config=None):
        Client_Base.__init__(self, client_id, client_secret, account_id,
                             tenant, api_version, account_type, office365, config)
