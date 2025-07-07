import sys
from auto_messenger import AutoMessenger
from clients import CustomersDatabase
from browser import WebChromeBrowser
from format_print import format_print
from datetime import datetime
from users import check_users
from checker_data import get_user_input, get_yes_no_input

"""
The program sends notifications via instant messages
integrated with WhatsApp.
Used for credit recovery actions.
"""

if __name__ == "__main__":
    print('-' * 25)
    user = input('Digite o usuário\n>>> ')
    user_bool = check_users(user)
    if user_bool is not True:
        print('-' * 25)
        sys.exit()
    print('-' * 25)

    start_date = (
        datetime.strptime('31/12/1900', "%d/%m/%Y").date()
    ).strftime('%Y-%m-%d')

    print('Digite a data')
    end_date = get_user_input('>>> ')

    # Customer exclusion
    excluded_customers = [
        ('')
    ]
    # Customer inclusion
    inserted_customers = [
        ('')
    ]
    db = CustomersDatabase(
        user,
        start_date,
        end_date,
        excluded_customers,
        inserted_customers
    )
    customers = db.db_customers()

    # Print the list on screen
    print()
    format_print(customers)

    # Question about billing message
    message_type = get_yes_no_input(
        'Deseja alterar a mensagem de cobrança? Sim[S]/Não[Enter]\n>>> '
    )

    # Flow control
    if message_type == 'S':
        print('Mensagem de cobrança alterada.')
        print()
    else:
        print('Mensagem de cobrança não alterada.')
    question = input('DESAJA CONTINUAR? (Y) ou (N)\n>>> ').upper()

    if question == 'Y':
        # Set browser and website
        manager = WebChromeBrowser()
        driver = manager.get_driver()

        # Instantiate the message object
        kwargs = {
            'customers': customers,
            'browser': driver,
            'website': 'https://web.whatsapp.com/'
        }
        if message_type == 'S':
            kwargs['billing_message'] = message_type

        message_conf = AutoMessenger(**kwargs)

        # Send the charges
        billed_customers = message_conf.run_billing()
    else:
        print('Thanks!')
        sys.exit()
