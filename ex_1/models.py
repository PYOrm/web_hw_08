from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField, DateField

class Author(Document):
    meta = {'collection': 'authors'}
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    meta = {'collection': "quotes"}
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()
