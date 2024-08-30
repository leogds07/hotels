#IMPORTS
from get_info import get_name, get_location, get_phone, check_in, check_out, adults, children, get_rooms, get_email, get_pwd, get_proxy_login, get_proxy_pwd, get_api_key
from get_website import get_json, extract_websites
from scrape_websites import get_addresses
from generate_email import generate_emails
from send_email import send_emails
import os
import sys

def main():
    #get info
    location = get_location()
    name = get_name()
    check_in_date = check_in()
    check_out_date = check_out()
    n_adults = adults()
    n_children = children()
    n_rooms = get_rooms()
    phone = get_phone()
    sender = get_email()
    encrypted_pwd = get_pwd()
    proxy_login = get_proxy_login()
    proxy_pwd_encrypted = get_proxy_pwd()
    encrypted_api_key = get_api_key()

    #generate e-mail message
    message = generate_emails(name, check_in_date, check_out_date, n_adults, n_children, n_rooms, phone)

    #extract websites
    json_data = get_json(location, encrypted_api_key)
    websites = extract_websites(json_data)

    #get e-mail addresses
    addresses = get_addresses(websites, proxy_login, proxy_pwd_encrypted)

    #send mail
    subject = 'Booking Request'
    send_emails(sender, addresses, subject, message, encrypted_pwd)

    #delete key file (Gmail password) and handle possible errors
    file_path = 'python/secret.key'
    try:
        os.remove(file_path)
        print('The key file has been deleted successfully.')
    except FileNotFoundError:
        sys.exit(f'{file_path} does not exist')
    except PermissionError:
        sys.exit(f'Permission denied: {file_path} cannot be deleted')
    except Exception as e:
        sys.exit(f'Error: {e}')

if __name__ == "__main__":
    main()
