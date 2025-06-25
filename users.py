def check_users(user: str):
    USER_CAD = ['matheus', 'joelma']
    try:
        if user.isdigit() is True:
            raise TypeError('Você digitou um número')
    except TypeError as e:
        print(f'Error: {e}')
        return False
    if user.lower() in USER_CAD:
        return True
    else:
        print('Usuário inexistente.')
        return False
