from         IPython import embed
from lib.controllers import *
from              os import system

class Menu:
    '''Display a menu and respond to choices when run.'''
    def __init__(self):
        system('clear')        
        
        self.choices = {
           1: download_pages_by_category,
           2: index_categories,
           3: index_pages,
           4: index_queries,
           5: display_category,
           6: display_page,
           7: display_query,
           8: search_pages_by_category,
           9: clear_database,
          10: quit,
          11: embed
        }
        
        self.prompts = {
           1: {'category_title'  :  "For which category would you like to download pages? ",
               'depth'           :  "At what depth would you like to search this category? "},
           2: None,
           3: {'category'        :  "For which category would you like to display pages? "},
           4: None,
           5: {'category'        :  "Which category would you like to display? "},
           6: {'page'            :  "Which page would you like to display? "},
           7: {'query_id'        :  "Which query would you like to display? "},
           8: {'category'        :  "Which category would you like to search? ",
               'search_term'     :  "Which page or search term would you like to search for? ",
               'matches'         :  "How many pages do you want to return? "},
           9: {'verification'    :  "Are you sure you want to clear the database? (yes) "},
          10: {'verification'    :  "Are you sure you want to quit? (yes) "},
          11: None
        }
        

    def __repr__(self):
        menu  = "          Notebook Menu\n"
        menu += "           1. Download Pages\n"
        menu += "           2. List Categories\n"
        menu += "           3. List Pages\n"
        menu += "           4. List Queries\n"
        menu += "           5. Display Category\n"
        menu += "           6. Display Page\n"
        menu += "           7. Display Query\n"
        menu += "           8. Find Similar Pages\n"
        menu += "           9. Clear Database\n"
        menu += "          10. Quit\n"
        menu += "          11. IPython\n"
        return menu

    def run(self):
        action = index_queries
        args = None
        while True:            
            if action:
                if action == embed:
                    action() 
                    system('clear')
                    print(self)
                else:
                    system('clear') 
                    print(self)  
                    if args == None:
                        action() 
                    else:
                        action(**args)                                       
                choice  = input_type_validator(int)
                action  = self.choices.get(choice)                
                args    = self.prompts.get(choice)
                if args is not None:
                    args = dict(args)
                    for key in args.keys():                     
                        args[key] = input(args[key])
            else:
                print("{0} is not a valid choice".format(choice))
