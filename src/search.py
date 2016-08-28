# from lib.natural_language_processing import *
# from                      lib.output import *
# from                       lib.pages import *
from lib.controllers import search_pages_by_category
from             sys import argv

category                 = argv[1]
matches                  = argv[2]
document_to_match        = ' '.join(argv[3:])

search_pages_by_category(category,matches,document_to_match)
