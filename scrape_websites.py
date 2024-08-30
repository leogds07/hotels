# IMPORTS
from bs4 import BeautifulSoup
import httpx
import re
import time
from handle_password import decrypt_message, load_key

def get_addresses(websites, proxy_login, proxy_password_encrypted) -> list:
    #decrypt proxy password
    key = load_key()
    proxy_pwd_decrypted = decrypt_message(proxy_password_encrypted, key)

    # Initialize addresses list
    addresses = []

    # Proxy configuration with login and password
    proxy_host = 'gw.dataimpulse.com'
    proxy_port = 823
    proxy_login = proxy_login
    proxy_password = proxy_pwd_decrypted
    proxy = f'http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}'

    proxies = {
        'http://': proxy,
        'https://': proxy
    }

    #many websites accept requests only from real browsers, so we set these headers to mimic a real browser
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'en-US,en;q=0.9',
    }

    # keep track of the index
    i = 0
    #keep track of e-mails found
    found = 0

    # Use a session to manage cookies (cookies are sent within the request)
    with httpx.Client(headers=headers, follow_redirects=True, proxies=proxies, timeout=30.0) as client:
        for website in websites:
            i += 1

            try:
                # delay between requests
                time.sleep(1)

                # get response and parse it
                response = client.get(website)
                if response.status_code == 403:
                    print(f"Access to {website} is forbidden (Error: 403). Skipping...")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract footer
                footer = soup.find('footer') or soup.find(id="footer")

                #if footer is found
                if footer:
                    if matches := re.search(r'^[\w\.-]+@[\w\.-]+\.\w+$', footer.get_text(), re.IGNORECASE):
                        address = matches.group(0)
                        print(f"E-mail address n.{i} of website: {website} has been found in footer")
                        addresses.append(address)
                        found += 1

                    #if email can't be found in footer, search for specific tags: span, div, and a and i
                    else:
                        tags = footer.find_all(['span', 'div', 'a', 'i'])
                        if tags: #if tags are found
                            for tag in tags: #iterate through tags
                                if matches := re.search(r'^[\w\.-]+@[\w\.-]+\.\w+$', tag.get_text(), re.IGNORECASE):
                                    address = matches.group(0)
                                    print(f"E-mail address n.{i} of website: {website} has been found in tag: '{tag}' within footer")
                                    addresses.append(address)
                                    found += 1
                                    break
                            
                            #if there are tags, but no e-mail in them, search for href="mailto:"
                            else:
                                tags = footer.find_all(href=re.compile(r"^mailto:.*"))
                                if tags: #check if tags with href="mailto:" have been found
                                    for tag in tags: #iterate through tags
                                        if matches := re.search(r'[\w\.-]+@[\w\.-]+\.\w+', str(tag), re.IGNORECASE):
                                            address = matches.group(0)
                                            print(f"E-mail address n.{i} of website: {website} has been found in tag: '{tag}' within footer thanks to href=mailto:")
                                            addresses.append(address)
                                            found += 1
                                            break
                                    
                                    #if href="mailto:" tags are found but no email in them
                                    else:
                                        print(f"E-mail address n.{i} of website: {website} can't be found. There are some href='mailto:' tags (n. of tags: {len(tags)} but no e-mail in them. This is the first tag: {tag[0]})")

                                #if there are no href="mailto:" tags, search for the whole pure HTML script without converting it to text
                                else:
                                    if matches := re.search(r"[\w\.-]+@[\w\.-]+\.\w+", str(soup), re.IGNORECASE):
                                        address = matches.group(0)
                                        print(f"E-mail address n.{i} of website {website} has been found searching for the whole pure HTML script")
                                        addresses.append(address)
                                        found += 1

                                    #if e-mail address can't be found in footer or in nested tags within footer or in href="mailto:", search the whole page
                                    else:
                                        html_text = soup.get_text()
                                        if matches := re.search(r'^[\w\.-]+@[\w\.-]+\.\w+$', html_text, re.IGNORECASE):
                                            address = matches.group(0)
                                            print(f"E-mail address n.{i} of website: {website} has been found searching the whole page")
                                            addresses.append(address)
                                            found += 1
                                        
                                        #search for contact page
                                        else:
                                            print(f"E-mail address n.{i} can't be found in website: {website}. Searching for specific contact page...")
                                            contact_page = f"{website}contatti"
                                            # get response from the new web address and parse it
                                            response_contact = client.get(contact_page)

                                            if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                if response_contact.status_code == 403:
                                                    print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                    continue
                                                
                                                soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                #search e-mail address using re
                                                if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                    address = matches.group(0)
                                                    print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                else: #if no e-mail found in contact page
                                                    print(f"E-mail address n.{i} of website: {website} can't be found in contact page: {contact_page}")

                                            else: #if contact page has not been found, search for another one
                                                contact_page = f"{website}/contatti"
                                                # get response from the new web address and parse it
                                                response_contact = client.get(contact_page)

                                                if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                    if response_contact.status_code == 403:
                                                        print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                        continue
                                                    
                                                    soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                    #search e-mail address using re
                                                    if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                        address = matches.group(0)
                                                        print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                    else:
                                                        print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                                                else: #if contact page has not been found, search for another one
                                                    contact_page = f"{website}contacts"
                                                    # get response from the new web address and parse it
                                                    response_contact = client.get(contact_page)

                                                    if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                        if response_contact.status_code == 403:
                                                            print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                            continue
                                                        
                                                        soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                        #search e-mail address using re
                                                        if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                            address = matches.group(0)
                                                            print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                        else:
                                                            print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                                                    else: #if contact page has not been found, search for another one
                                                        contact_page = f"{website}/contacts"
                                                        # get response from the new web address and parse it
                                                        response_contact = client.get(contact_page)

                                                        if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                            if response_contact.status_code == 403:
                                                                print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                                continue
                                                            
                                                            soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                            #search e-mail address using re
                                                            if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                                address = matches.group(0)
                                                                print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                            else:
                                                                print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                                                        else: #if contact page has not been found, search for another one
                                                            contact_page = f"{website}contact-us"
                                                            # get response from the new web address and parse it
                                                            response_contact = client.get(contact_page)

                                                            if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                                if response_contact.status_code == 403:
                                                                    print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                                    continue
                                                                
                                                                soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                                #search e-mail address using re
                                                                if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                                    address = matches.group(0)
                                                                    print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                                else:
                                                                    print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                                                            else: #if contact page has not been found, search for another one
                                                                contact_page = f"{website}/contact-us"
                                                                # get response from the new web address and parse it
                                                                response_contact = client.get(contact_page)

                                                                if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                                    if response_contact.status_code == 403:
                                                                        print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                                        continue
                                                                    
                                                                    soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                                    #search e-mail address using re
                                                                    if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                                        address = matches.group(0)
                                                                        print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                                    else:
                                                                        print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                                                                else: #if contact page has not been found, search for another one
                                                                    contact_page = f"{website}contactus"
                                                                    # get response from the new web address and parse it
                                                                    response_contact = client.get(contact_page)

                                                                    if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                                        if response_contact.status_code == 403:
                                                                            print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                                            continue
                                                                        
                                                                        soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                                        #search e-mail address using re
                                                                        if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                                            address = matches.group(0)
                                                                            print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                                        else:
                                                                            print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                                                                    else: #if contact page has not been found, search for another one
                                                                        contact_page = f"{website}/contactus"
                                                                        # get response from the new web address and parse it
                                                                        response_contact = client.get(contact_page)

                                                                        if response_contact: #if there is a response from the contact page (so contact page has been found)
                                                                            if response_contact.status_code == 403:
                                                                                print(f"Access to {contact_page} is forbidden (Error: 403). Skipping...")
                                                                                continue
                                                                            
                                                                            soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                                                                            #search e-mail address using re
                                                                            if matches := re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", soup_contact.get_text(), re.IGNORECASE):
                                                                                address = matches.group(0)
                                                                                print(f"E-mail address n.{i} of website: {website} found in contact page: {contact_page}")
                                                                            else:
                                                                                print(f"E-mail address n.{i} of website: {website} can't be found even after searching for contact page: {contact_page}")

                #if footer can't be found, search the whole page
                else:
                    print(f"E-mail address n.{i} of website: {website}. No footer, searching for specific tags...")
                    html_text = soup.get_text()
                    if matches := re.search(r'^[\w\.-]+@[\w\.-]+\.\w+$', html_text, re.IGNORECASE):
                        address = matches.group(0)
                        print(f"E-mail address n.{i} of website: {website} has been found searching for the whole page, there wasn't the footer")
                        addresses.append(address)
                        found += 1
                    #if no e-mail found searching for the whole page, search for specific tags
                    else:
                        tags = soup.find_all(['span', 'div', 'a', 'i'])
                        if tags: #if tags are found
                            for tag in tags: #iterate through tags
                                if matches := re.search(r'^[\w\.-]+@[\w\.-]+\.\w+$', tag.get_text(), re.IGNORECASE):
                                    address = matches.group(0)
                                    print(f"E-mail address n.{i} of website: {website} has been found in tag: '{tag}' within footer")
                                    addresses.append(address)
                                    found += 1
                                    break
                            #if there are not tags, search for href="mailto:"
                            else:
                                tags = soup.find_all(href=re.compile(r"^mailto:.*"))
                                if tags: #check if tags with href="mailto:" have been found
                                    for tag in tags: #iterate through tags
                                        if matches := re.search(r'[\w\.-]+@[\w\.-]+\.\w+', str(tag), re.IGNORECASE):
                                            address = matches.group(0)
                                            print(f"E-mail address n.{i} of website: {website} has been found in tag: '{tag}'. There was no footer, but thanks to href=mailto:")
                                            addresses.append(address)
                                            found += 1
                                            break
                                    #if href="mailto:" tags are found but no email in them
                                    else:
                                        print(f"E-mail address n.{i} of website: {website} can't be found. There are some href='mailto:' tags (n. of tags: {len(tags)} but no e-mail in them. This is the first tag: {tag[0]})")
                                else: #if there are no href="mailto:" tags
                                    print(f"E-mail address n.{i} of website: {website} can't be found. There is no footer, no e-mail in tags and there are no href='mailto:' tags")
                        else: #if there aren't tags
                            print(f"E-mail address n.{i} of website: {website} can't be found. No footer and no tags")
            #handle possible errors
            except httpx.RequestError as e:
                print(f"An error in hotel n.{i} occurred while requesting {website}: {e}")
            except Exception as e:
                print(f"An error in hotel n.{i} occurred while processing {website}: {e}")

    #print the ratio found/total
    print(f"E-mails found: {found}/{i}")

    return addresses