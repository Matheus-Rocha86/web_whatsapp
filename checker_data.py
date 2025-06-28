import sys
from datetime import datetime


def get_user_input(prompt, date_format="%d/%m/%Y", output_format="%Y-%m-%d"):
    """Gets input from the user and converts it to the desired format."""
    try:
        user_input = input(prompt)
        return datetime.strptime(user_input, date_format).date().strftime(output_format)
    except Exception as e:
        print('-' * 25)
        print(f'Error: {e}')
        print('-' * 25)
        print()
        sys.exit()
    print('-' * 25)


def get_yes_no_input(prompt, error_message="Incorrect data entry!"):
    """Gets a Yes/No response from the user."""
    try:
        response = input(prompt).upper()
        if response not in ('S', ''):
            raise ValueError(error_message)
        return response
    except ValueError as e:
        print(f"Error: {e}")
        print('-' * 25)
        sys.exit()
