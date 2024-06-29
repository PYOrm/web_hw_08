from mongoengine import Document, connect
from mongoengine.fields import StringField, EmailField, BooleanField
import configparser


class Contact(Document):
    meta = {'collection': 'contacts', "allow_inheritance": True}
    fullname = StringField()
    email = EmailField()
    msg_send = BooleanField(default=False)
    phone = StringField()
    address = StringField()
    sms_prefer = BooleanField(default=False)


def db_connection():
    config = configparser.ConfigParser()
    config.read('.env')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    # connect to cluster on AtlasDB with connection string

    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?\
retryWrites=true&w=majority&appName=Claster""", ssl=True)
