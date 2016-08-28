from mongoengine import register_connection
from          os import environ

def input_type_validator(datatype):
    input_value = None
    while input_value == None:
        try:
            input_value = datatype(input("Enter an option: "))
        except ValueError:
            print("Error: Invalid Choice")
    return input_value

def register_default_mongodb_connection():
    register_connection('default','queries',environ['MONGODB_PORT_27017_TCP_ADDR'],27017)
    
def wikimedia_page_format(page):
    return page.lower().capitalize().replace(' ','_')