from mongoengine import DateTimeField, Document, IntField, StringField

class Query(Document):
    category          = StringField()
    number_of_matches = IntField()
    depth             = IntField()
    page_count        = IntField()
    subcategory_count = IntField()
    query_id          = IntField()
    query_type        = StringField()
    status            = StringField()