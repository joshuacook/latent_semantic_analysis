from             sys import argv 
from            yaml import load
from lib.controllers import download_pages_by_category

if len(argv) > 1:
    category = argv[1]    
    depth = 1 
    
    if category is not 'Machine Learning' and \
        category[-3:] == 'yml' or category[-4:] == 'yaml':

        category   = open(category, "r")
        categories_list = load(category)['categories']

        pages         = []
        subcategories = []
        category_tags = []

        for cat in categories_list:
           pages_rtn, \
               subcategories_rtn, \
               category_tags_rtn = download_pages_by_category(cat,depth)
           pages         += pages_rtn
           subcategories += subcategories_rtn
           category_tags += category_tags_rtn
    else:
        pages, subcategories, category_tags = download_pages_by_category(category,depth)

    for p in pages:
        print(p.title)
    print("\n")
    for s in subcategories:
        print(s.title)  
else:
    print("Error: You must specify a valid category. Try putting the category in quotes.")
  

  
    
    
    


