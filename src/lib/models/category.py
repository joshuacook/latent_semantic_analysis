from mongoengine import Document, EmbeddedDocumentField, IntField, StringField

class Category(Document):
    pageid        = IntField()
    title         = StringField()
    parent_pageid = IntField()
    parent_title  = StringField() 