from lib.controllers.page_controller import read_pages_from_mongo
from lib.controllers import *
from     lib.helpers import *
from      lib.models import *
from             sys import exit

def display_category(category):
    this_category = Category.objects(title=category).first()
    if this_category is not None:
        print("-"*50)
        print("Category: {0}".format(this_category.title))
        print("Page ID: {0}".format(this_category.pageid))
        print("Parent Category: {0}".format(this_category.parent_title))
        print("Parent Page Id: {0}".format(this_category.parent_pageid))
        print("-"*50)
    else:
        print("Error: No Category {0}.".format(category))
        

def display_page(page):
    this_page = Page.objects(title=page).first()
    if this_page is not None: 
        print(this_page.title)
        print(this_page.text)
        for cat in this_page.category_tags:
            print(cat.category_pageid, cat.depth)
    else:
        print("Error: no page associated with {0}".format(page))
        
        
def display_query(query_id):
    if query_id == '': query_id = 0
    this_query = Query.objects(query_id=int(query_id)).first()
    if this_query is not None:
        print("-"*50)
        print("Category: {0}".format(this_query.category)) 
        print("Query Id: {0}".format(this_query.query_id))
        print("Query Type: {0}".format(this_query.query_type))
        if this_query.query_type == 'search':       
            print("Number of Matches: {0}".format(this_query.number_of_matches)) 
        print("Depth of Search: {0}".format(this_query.depth))             
        print("Page Count: {0}".format(this_query.page_count))  
        if this_query.query_type == 'download':           
            print("Subcategory Count: {0}".format(this_query.subcategory_count))       
        print("Status: {0}".format(this_query.status))            
        print("-"*50)
    else:
        print("Error: No Query {0}.".format(query_id))
    

def clear_database(verification):
    if verification == 'yes':
        Category.objects().delete()
        Page.objects().delete()
        Query.objects().delete()
    print("Database cleared.")

def index_categories():    
    categories = Category.objects()
    print("Category")
    print("-"*50)
    for cat in categories:
        print(cat.title)
    print("-"*50)
    
def index_pages(category, depth=1):
    category_pageid = mediawiki_get_category_pageid(category)
    try:
        assert(category_pageid is not -1)
    except AssertionError:
        print("Error: No Wikipedia Category: {0}".format(category))
        return [], [], []
        
    pages = read_pages_from_mongo(category_pageid)
    
    print("Page", " "*46,"Category","Depth")
    print("-"*66)
    for page in pages:
        print(page.title," "*(50-len(page.title)),category, page.reference_depths[int(category_pageid)])    
    print("-"*66)
    
def index_queries():
    queries = Query.objects()
    print("Queries   Type        Category")
    print("-"*50)
    for query in queries:
        print(str(query.query_id), "  ", query.query_type, " "*(10-len(query.query_type)), query.category)        
    print("-"*50)
    

def quit(verification):
    if verification == "yes":
        print("Thank you for using your notebook today.")
        exit(0)