#IMPORTS
from get_info import get_age

#generate two different types of e-mail message: if there are children the e-mail message changes
def generate_emails(name, check_in, check_out, adults, children, rooms, phone) -> str:
    #if there are children store their age in a list
    if children > 0:
        children_age = []
        for child in range(children):
            child_age = get_age()
            children_age.append(child_age)

    if children > 0:
        email = f"Dear Reservations Team,\nI hope this email finds you well. I am writing to inquire about the availability of rooms at your hotel for the following stay:\nCheck-in Date: {check_in}; \nCheck-out Date: {check_out}; \nNumber of Rooms Required: {rooms}; \nNumber of Adults: {adults}; \nNumber of Children: {children}; \nAge of Children: {children_age}.\nCould you please confirm the availability for the requested dates and provide me with the total cost of the stay? Additionally, if there are any special offers or packages available during this period, I would be grateful if you could share those details as well.\nPlease also let me know the process for securing the reservation, including any deposit requirements or cancellation policies.\nThank you in advance for your assistance. I look forward to your prompt response.\nBest regards,\n{name}\n{phone}"
    else:
        email = f"Dear Reservations Team,\nI hope this email finds you well. I am writing to inquire about the availability of rooms at your hotel for the following stay:\nCheck-in Date: {check_in}; \nCheck-out Date: {check_out}; \nNumber of Rooms Required: {rooms}; \nNumber of Adults: {adults}.\nCould you please confirm the availability for the requested dates and provide me with the total cost of the stay? Additionally, if there are any special offers or packages available during this period, I would be grateful if you could share those details as well.\nPlease also let me know the process for securing the reservation, including any deposit requirements or cancellation policies.\nThank you in advance for your assistance. I look forward to your prompt response.\nBest regards,\n{name}\n{phone}"

    return email