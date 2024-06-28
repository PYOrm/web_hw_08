from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField


class Contact(Document):
    meta = {'collection': 'contacts'}
    fullname = StringField()
    email = EmailField()
    msg_send = BooleanField(default=False)
    phone = StringField()
    address = StringField()
    sms_prefer = BooleanField(default=False)

