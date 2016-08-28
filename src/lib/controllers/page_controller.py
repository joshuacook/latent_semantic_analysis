from   nltk.stem import PorterStemmer
from          re import compile, escape, sub
from      string import digits, punctuation
from         sys import stdout
from lib.helpers import mediawiki_get_page_headings, mediawiki_get_page_text
from  lib.models import CategoryTag, Page
        
def parse_text(text):    
    regex = compile('[%s]' % escape(punctuation))
    text  = ''.join(char for char in text if char not in set(digits))
    text  = sub('\s+',' ', text)
    text  = regex.sub(' ', text)
    text  = text.split(' ')
    text  = [PorterStemmer().stem(word) for word in text]
    text  = ' '.join(text)

    return text
    
def parse_title(title):
    regex = compile('[%s]' % escape(punctuation))
    title  = regex.sub(' ', title)
    title = title.replace(' ','').lower()
    return title
       
def read_pages_from_mongo(category_pageid):
    pages = Page.objects()
    returned_pages = []
    for page in pages:
        if category_pageid in page.category_membership:
            returned_pages.append(page)  
    return returned_pages  

def write_page_to_mongo(page, category_tags):
    if Page.objects(pageid=page['pageid']).count() == 0:
        this_page               = Page(pageid=page['pageid'],title=page['title'])
        this_page.headings      = mediawiki_get_page_headings(this_page.title)
        this_page.text          = mediawiki_get_page_text(this_page.title, this_page.pageid)        
        this_page.save()
    
    this_page = Page.objects(pageid=page['pageid']).first()
    for category_tag in category_tags:
        if category_tag.category_pageid not in this_page.category_membership:
            Page.objects(pageid=page['pageid']).update_one(push__category_tags=category_tag)
        
    return this_page
