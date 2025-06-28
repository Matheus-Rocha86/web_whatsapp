def check_users(user: str):
    """## Check input data
    #### Checks both typing and whether the string is listed.
    """
    USER_CAD = ['matheus', 'joelma']
    try:
        if user.isdigit() is True:
            raise TypeError('You entered a number!')
    except TypeError as e:
        print(f'Error: {e}')
        return False
    if user.lower() in USER_CAD:
        return True
    else:
        print('Nonexistent user!')
        return False
