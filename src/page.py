from lib.controllers import display_page, parse_text
from             sys import argv


if len(argv) > 1:
    page = ' '.join(argv[1:]) 
    display_page(page)
else:
    print("Error: You must specify a valid page. Try putting the page in quotes.")

