from lib.controllers import *
from     lib.helpers import *
from      lib.models import *
from            time import time

def download_pages_by_category(category_title, depth):
    query = Query(query_type='download', depth=depth, category=category_title, number_of_matches=None, query_id=int(time()*10%100000))
    try: 
        depth         = int(depth)
    except ValueError:
        print("Error: You must provide a depth.")
        return [],[],[]
    category_pageid = mediawiki_get_category_pageid(category_title)
    try:
        assert(category_pageid is not -1)
    except AssertionError:    
        query.status = "Error: No Wikipedia Category: {0}".format(category_title)
        query.save()
        print(query.status)
        return [],[],[]
        
    write_category_to_mongo({'pageid':category_pageid,'title':category_title},None)
    
    print("Category", " "*32, "Page ID", " "*3, "Depth", " "*4, "Parents")    
    print("-"*76)
    print(category_title,' '*(40-len(category_title)),category_pageid,' '*(12-len(str(category_pageid))),depth)
    download_pages(category_title,category_pageid,depth)
    print("-"*76)
    
    pages = []
    subcategories = []
    category_tags = []   
    
    query.page_count        = len(read_pages_from_mongo(category_pageid))
    query.subcategory_count = len(Category.objects(parent_pageid=category_pageid))
    query.status            = "Success"
    query.save()   
        
    return pages, subcategories, category_tags
    
def download_pages(category_title,category_pageid,depth,parent_pageids=[]):        
    response       = mediawiki_get_pages_for_category(category_title)
    pages          = [page for page in response if page['ns'] == 0]
    subcategories  = [subcat for subcat in response if subcat['ns'] == 14] 
    
    try:
        parent_pageid = parent_pageids[-1]
    except IndexError:
        parent_pageid = None
    subparent_pageids = parent_pageids + [category_pageid]
    
    category_tags = []
    for i in range(len(subparent_pageids)):
        current_depth   = len(subparent_pageids) - i
        category_tags.append(CategoryTag(category_pageid=subparent_pageids[i], depth=current_depth))
        
    for page in pages:
        mongo_page = write_page_to_mongo(page,category_tags)
    for subcat in subcategories:
        mongo_subcategory = write_category_to_mongo(subcat,parent_pageid)  
    if depth > 1:
        for subcat in subcategories:
            print(subcat['title'],' '*(40-len(subcat['title'])),subcat['pageid'],' '*(12-len(str(subcat['pageid']))),depth-1," "*6, subparent_pageids)
            download_pages(subcat['title'],subcat['pageid'],depth-1,subparent_pageids)   
        
def search_pages_by_category(category, matches, search_term):
    query = Query(query_type='search', depth=None, category=category, number_of_matches=matches, query_id=int(time()*10%100000))
    category_pageid = mediawiki_get_category_pageid(category)
    try:
        assert(category_pageid is not -1)
    except AssertionError:
        print("Error: No Wikipedia Category: {0}".format(category))
        return [],[],[]
    
    pages              = read_pages_from_mongo(category_pageid)
    page_ids           = [page.pageid for page in pages]
    text_list          = [parse_text(page.text)   for page in pages]
    page_titles        = [page.title for page in pages]
    parsed_page_titles = [parse_title(page.title) for page in pages]
    parsed_search_term = parse_title(search_term)
    print("{0} pages in Category: {1}".format(len(page_titles), category))    
    matches            = min(int(matches),len(page_titles)-1)
    
    try:
        document_to_match_index = parsed_page_titles.index(parsed_search_term)
    except ValueError:
        document_to_match_index = len(page_titles)
        parsed_page_titles.append(parsed_search_term)
        text_list.append(search_term)\
    
    document_term_matrix     = prepare_document_term_matrix(text_list)
     
    latent_semantic_analysis = prepare_singular_value_decomposition(document_term_matrix)
    
    similarity_matrix        = prepare_similarity_matrix(latent_semantic_analysis)
    
    similar_page_indices  = identify_similar_pages(document_to_match_index, similarity_matrix)
    similar_pages = []
    for i in range(matches):
        pg_index = similar_page_indices[i+1]
        similar_pages.append((page_titles[pg_index],page_ids[pg_index]))
    
    print("Matching {0} pages to '{1}' in Category: {2}".format(matches, search_term, category))
    print("")
    print("Page Title                                          Page Id")
    for page in similar_pages:
        print(page[0]," "*(50-len(page[0])),page[1])
    query.status = "Success."
    query.save()
    
