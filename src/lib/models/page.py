from mongoengine import Document, EmbeddedDocument, \
    EmbeddedDocumentField, IntField, ListField, StringField
    
class CategoryTag(EmbeddedDocument):
    category_pageid = IntField()
    depth           = IntField()

class Page(Document):
    pageid          = IntField()
    title           = StringField()
    text            = StringField()
    headings        = ListField(StringField())
    category_tags   = ListField(EmbeddedDocumentField(CategoryTag))
    
    @property
    def category_membership(self):
        return [category_tag.category_pageid
                for category_tag in self.category_tags]
                
    @property
    def reference_depths(self):
        tags = {cat_tag.category_pageid:cat_tag.depth 
                for cat_tag in self.category_tags}
        return tags
        
        
