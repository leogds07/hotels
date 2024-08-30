#IMPORTS
import re
import sys
from handle_password import generate_key, load_key, encrypt_message


#FUNCTIONS
def get_name() -> str:
    name = input('Full Name: ')
    
    if name.isdigit():
        raise ValueError('Name cannot include numbers')
    
    return name

def get_phone() -> str:
    phone = input('Phone (including prefix): ')

    return phone

def get_location() -> str:
    location = input("Location: ").strip(' ')

    #check if location is int
    if location.isdigit():
        raise ValueError("Location cannot be a number")
    
    #location already validated with the prompt given to ChatGPT -> if the location doesn't exist, the response will be "location does not exist."

    return location

def check_in() -> str:
    check_in = input(f"Check in date (YYYY-MM-DD): ")

    if not re.search(r"^\d{4}-\d{2}-\d{2}$", check_in):
        sys.exit("Wrong Format")

    return check_in

def check_out() -> str:
    check_out = input("Check out date (YYYY-MM-DD): ")

    if not re.search(r"^\d{4}-\d{2}-\d{2}$", check_out):
        sys.exit("Wrong Format")

    return check_out

def adults() -> str:
    try:
        adults = int(input("Adults number: "))
    except ValueError:
        sys.exit("Cannot input letters")
    
    if adults < 1:
        sys.exit("Minimum: 1")

    return str(adults)

def children() -> int:
    try:
        children = int(input("Children number (age 0-17): "))
    except ValueError:
        sys.exit("Cannot input letters")

    if children < 0:
        sys.exit("Minimum: 0")

    return children

def get_age() -> int:
    try:
        age = int(input("Child Age: "))
    except ValueError:
        sys.exit("Cannot input letters")

    if age < 0:
        sys.exit("Minimum: 0")

    return age

def get_rooms() -> str:
    try:
        rooms = int(input("Rooms: "))
    except ValueError:
        sys.exit("Cannot input letters")

    if rooms < 1:
        sys.exit("Minimum: 1")

    return str(rooms)

def get_email() -> str:
    email = input('E-mail: ')

    if not re.search(r"^\w+@\w.+\.(com|edu|gov|net|org|it|en|es)$", email):
        sys.exit('Invalid e-mail')
    
    return email

def get_pwd():
    pwd = input("\n///\nYou have to write Gmail's app password.\nGo to your Google Account and Log In\n-> Security\n-> Check if 2 step verification is active (if not, activate it)\n-> In the search bar, search for 'App Password'\n-> Add an app password for Gmail\nALERT! Remember to take a screenshot, because you will not be able to check the password again.\nIf you forgot to take a screenshot, you will have to delete the password and generate a new one.\nApp Password: ")

    #validate password
    if not re.search(r'^\w{4}\s\w{4}\s\w{4}\s\w{4}$', pwd):
        sys.exit('Wrong format')

    #encrypt password
    generate_key()
    key = load_key()
    encrypted_password = encrypt_message(pwd, key)

    return encrypted_password

def get_price() -> int: #ACTUALLY NOT USED
    try:
        price = int(input('Price (1-5): '))
    except ValueError:
        sys.exit('Price has to be an int')

    if not 0 < price < 6:
        sys.exit('Min: 1, Max: 5')
    
    return price

def get_proxy_login() -> str:
    proxy_login = input("Proxy Login")

    if proxy_login is None:
        sys.exit("Proxy Login cannot be None")

    return proxy_login

def get_proxy_pwd():
    proxy_pwd = input("Proxy Password: ")

    if proxy_pwd is None:
        sys.exit("Proxy Password cannot be None")

    #encrypt pwd
    key = load_key()
    encrypted_pwd = encrypt_message(proxy_pwd, key)

    return encrypted_pwd

def get_api_key():
    api_key = input("Api Key (hasdata.com): ")

    #encrypt key
    key = load_key()
    encrypted_key = encrypt_message(api_key, key)

    return encrypted_key