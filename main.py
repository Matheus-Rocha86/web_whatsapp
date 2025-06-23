import sys
from auto_messenger import AutoMessenger
from clients import CustomersDatabase
from browser import WebChromeBrowser
from format_print import format_print
from db_whatsapp import insert_data

""" O programa realiza notificações por mensagens
    instantâneas integrado ao Whatsapp. Utilizado
    para ações de recuperação de créditos.
"""
if __name__ == "__main__":
    print('-' * 25)
    user = input("Digite o usuário: ")
    print('-' * 25)
    end_date = input("Digite a data: ")
    print('-' * 25)
    start_date = '31/12/1900'
    message_type = input('Pressione "s" para alterar a mensagem de cobrança: ').upper()
    excluded_customers = [
        ('')
    ]
    customer_list = CustomersDatabase(user, start_date, end_date)
    charges = customer_list.db_customers()
    refined_charges = customer_list.number_processing(charges)
    refined_charges_copy = refined_charges.copy()
    ajusted_refined_charges = customer_list.to_delete_customers(
        excluded_customers,
        refined_charges_copy
    )

    # Imprimir a lista em tela
    print()
    format_print(ajusted_refined_charges)

    # Controle de fluxo
    question = input('DESAJA CONTINUAR? (Y) ou (N): ').upper()

    if question == 'Y':
        # Definir o navegador e o site
        manager = WebChromeBrowser()
        driver = manager.get_driver()

        # Instanciar o objeto mensagem
        if message_type == 'S':
            message_conf = AutoMessenger(
                ajusted_refined_charges,
                driver,
                'https://web.whatsapp.com/',
                billing_message=message_type
            )
        else:
            message_conf = AutoMessenger(
                ajusted_refined_charges,
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
