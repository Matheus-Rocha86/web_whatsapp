import sqlite3
from pathlib import Path


def insert_data(dados):
    """
    Função para inserir dados dinamicamente em uma tabela SQLite.

    :param dados: Lista de tuplas contendo os dados a serem inseridos.
    """

    # Caminho
    ROOT_DIR = Path(__file__).parent
    DB_NAME = 'db.whatsapp.sqlite3'
    DB_FILE = ROOT_DIR / DB_NAME
    TABLE_NAME = 'deadbeat_customers'

    try:
        with sqlite3.connect(DB_FILE) as conexao:
            cursor = conexao.cursor()

            # Cria a tabela se não existir
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} '
                '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'nome TEXT, '
                'valor REAL, '
                'data TEXT)'
            )

            # Query SQL fixa com os nomes das colunas
            sql = (
                f'INSERT INTO {TABLE_NAME} '
                '(nome, valor, data) VALUES (?, ?, ?) '
            )

            # Verifica se é uma lista de tuplas ou uma única tupla
            if isinstance(dados, list):
                cursor.executemany(sql, dados)
            else:
                cursor.execute(sql, dados)

            conexao.commit()

    except sqlite3.Error as erro:
        print(f"Erro ao inserir dados: {erro}")
