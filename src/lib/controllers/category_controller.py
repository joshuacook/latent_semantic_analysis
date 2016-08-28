from lib.helpers import *
from  lib.models import Category, Page

def write_category_to_mongo(category, parent_pageid):    
    category['title'] = category['title'].replace('Category:','')
    if Category.objects(pageid=category['pageid']).count() == 0:
        this_category           = Category(pageid=category['pageid'],title=category['title'])
        this_category.save()
        
    this_category   = Category.objects(pageid=category['pageid']).first()    

    if parent_pageid is not None:        
        parent_category             = Category.objects(pageid=parent_pageid).first()
        this_category.parent_pageid = parent_pageid
        this_category.parent_title  = parent_category.title
        this_category.save()
        
    return this_category
