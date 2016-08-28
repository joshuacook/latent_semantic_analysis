from lib.controllers import index_pages
from       sys import argv


if len(argv) > 1:
    index_pages(" ".join(argv[1:]))
else:
    print("Error: a Valid Category must be supplied")
    


