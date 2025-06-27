import sys
from auto_messenger import AutoMessenger
from clients import CustomersDatabase
from browser import WebChromeBrowser
from format_print import format_print
from db_whatsapp import insert_data
from datetime import datetime
from users import check_users

""" O programa realiza notificações por mensagens
    instantâneas integrado ao Whatsapp. Utilizado
    para ações de recuperação de créditos.
"""
if __name__ == "__main__":
    print('-' * 25)
    print('Digite o usuário')
    user = input('>>> ')
    user_bool = check_users(user)
    if user_bool is not True:
        print('-' * 25)
        sys.exit()
    print('-' * 25)
    try:
        print('Digite a data')
        end_date = (
            datetime.strptime(input('>>> '), "%d/%m/%Y").date()
        ).strftime('%Y-%m-%d')
    except Exception as e:
        print('-' * 25)
        print(f'Error: {e}')
        print('-' * 25)
        print()
        sys.exit()
    print('-' * 25)
    start_date = (
        datetime.strptime('31/12/1900', "%d/%m/%Y").date()
    ).strftime('%Y-%m-%d')
    print('Deseja alterar a mensagem de cobrança? Sim[S]/Não[Enter]')
    try:
        message_type = input('>>> ').upper()
        if message_type != 'S' and message_type != '':
            raise ValueError('Entrada de dados incorreta!')
    except ValueError as e:
        print(f'Error: {e}')
        print('-' * 25)
        sys.exit()

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
    # Imprimir a lista em tela
    print()
    format_print(customers)

    # Controle de fluxo
    if message_type == 'S':
        print('Mensagem de cobrança alterada.')
        print()
    else:
        print('Mensagem de cobrança não alterada.')
    print('DESAJA CONTINUAR? (Y) ou (N)')
    question = input('>>> ').upper()

    if question == 'Y':
        # Definir o navegador e o site
        manager = WebChromeBrowser()
        driver = manager.get_driver()

        # Instanciar o objeto mensagem
        if message_type == 'S':
            message_conf = AutoMessenger(
                customers,
                driver,
                'https://web.whatsapp.com/',
                billing_message=message_type
            )
        else:
            message_conf = AutoMessenger(
                customers,
                driver,
                'https://web.whatsapp.com/'
            )
        # Envia as cobranças
        billed_customers = message_conf.run_billing()

        # Grava no banco de dados
        insert_data(billed_customers)

    else:
        print('Obrigado!')

        # Encerra a aplicação
        sys.exit()
