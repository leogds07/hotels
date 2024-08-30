# HOTEL AUTOMATION

## Overview

A lot of people, when searching for hotels for their holiday, usually go on websites such as booking.com and search for some hotels that match their preferences. Then, they go on the hotels' website and search for the hotels' e-mail address, to later send an e-mail to request an offer. This is because when someone books from booking.com or similar, these websites add expensive fees, which could be easily avoided by booking directly from the hotel itself.

The problem in all of this is that people get tired and annoyed repeating this process over and over. Sometimes it is even difficult to find a hotel's e-mail address, as it could be in the footer, hidden in the menu, or in the contact page... In fact, this makes you lose some precious time!

What this project does is automate this process, asking the user for some infos, such as a location, two dates, the number of people and rooms, and then it sends an e-mail to 15/20 hotels found in that location.

## Key Features

* Website searching -> After the location is given by the user, the program uses an API that scrapes data from Google Maps, searching for "Hotels in {location}" and retrieving the website.

* E-mail retrieving -> This process has certainly been the most challenging one: as I wrote earlier, there are some website that put their e-mail explicitly in the footer, others put a hyperlink, others put it in the contacts page, and there are some that don't even want to know anything about being scraped. Because of this, I implemented a very complex, but well-structured algorithm that searches for the e-mail in every place within the hotel's website. The actual ratio of E-mails Found/Total ranges from 13/20 to 19/20, but there is still room for improvements.

* Sending the e-mails -> To send the e-mails, I used the SMTP library, which works perfectly. The only issue is that it isn't really user-friendly, as to be able to send the e-emails the user has to type in the Gmail's App Password (which is afterwards encrypted): most of the people don't even know what that is and it isn't even that simple to create. Therefore, this will be the first factor improve with the purpose of simplifying this approach.

## Future Features

* Improvement of e-mail retrieving algorithm

* Improvement of UI and Accessibility to send the e-mails

## Abandoned Features

* ChatGPT API to find the e-mail addresses of the each hotel, just giving a location -> Due to restrictions, ChatGPT wasn't giving out the right e-mail addresses

* TripAdvisor API to find the hotels' websites -> TripAdvisor was giving out only 10 hotels per request, most of the time not providing neither the e-mail nor the website

## How to Install and Run the Project

In progress...

## Credits

I was he only one to work at this project, but I have to mention:

* [Hasdata](hasdata.com) -> This is the API that I used to get the hotels' website link from Google Maps. Perfect tool.

* [DataImpulse](dataimpulse.com) -> This is the tool that I used for the proxies to scrape the hotels' website to get their e-mails. This was perfect as well.


Copyright © 2024 Leonardo Giuliani de Santis

All rights reserved. This software and associated documentation files (the "Software")
may not be used, copied, modified, merged, published, distributed, sublicensed, and/or sold
without explicit permission from the author.

For permissions, please contact:
leogiulianidesantis@gmail.com
+39 392 064 7910# hotels
