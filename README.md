# Automated Messaging

This program is designed to send automated WhatsApp messages
to a group of contacts, without requiring them to be saved in advance.

## Libraries Used
- Selenium
- SQLite 3
- fdb

The remaining libraries used are Python standard libraries.

## Main
The program's main file accepts the following parameters: a date up to which the data will be displayed. The input format should follow pt-BR: dd/MM/YYYY. The program also accepts a name,
for example, the user who will query the database.

The final output of the program is a list containing the contact's name, value, and the date the message was sent.

## Classes principais:
- auto_messenger.py
    - Contains the core logic.
- browser.py
    - Handles browser configuration (Chrome).

## Classes secudárias e módulos:
- clients.py
    - Responsible for querying the database.
- db_whatsapp.py (módulo)
    - Inserts data into the SQLite 3 database.
- format_print.py
    - Formats numbers and other output data.

---

# Nota final
The most important thing is to download the script, use it in the way that best suits you, and always remember—programming is fun. So, have fun! 