import fdb
from datetime import datetime


class CustomersDatabase:
    """
    Realiza operações de busca no banco de dados alvo.
    Os objetos da classe são uma lista de tuplas com
    três variáveis.

    :param user: nome do usuário cobrador.
    :param data_inf: data inicial no formato, xx/xx/xxxx.
    :param data_sup: data final no formato, xx/xx/xxxx.
    """
    def __init__(self, user: str, data_inf: str, data_sup: str):
        self.user = user
        self.data_inf = data_inf
        self.data_sup = data_sup
        self.excluded_customers = []

    def db_customers(self):
        data_inf_obj = datetime.strptime(self.data_inf, "%d/%m/%Y").date()
        data_sup_obj = datetime.strptime(self.data_sup, "%d/%m/%Y").date()
        data_inf_standard = data_inf_obj.strftime('%Y-%m-%d')
        data_sup_standard = data_sup_obj.strftime('%Y-%m-%d')

        try:
            # Abrir um cursor e uma conexão
            connect = fdb.connect(
                host='resulthserv',
                database='c:/ResWinCS/Banco/RESULTH.FB',
                user='SYSDBA',
                password='masterkey'
            )
            cursor = connect.cursor()

            if self.user.lower() == 'joelma':
                opr = ('<')
            else:
                opr = ('>=')

            # Comandos SQL
            sql1 = f"""
            SELECT
                cliente.nome,
                SUM(docurec.valordocto - docurec.valorpago) AS saldo,
                cliente.fone
            FROM
                cliente
            INNER JOIN
                docurec
            ON
                cliente.codcliente = docurec.codcliente
            WHERE
                docurec.dt_vencimento BETWEEN ? AND ?
            AND
                docurec.situacao <> 2
            AND
                docurec.situacao <> 4
            AND
                cliente.ativo = 'S'
            GROUP BY
                cliente.nome,
                cliente.fone,
                cliente.ativo
            HAVING
                SUM(docurec.valordocto - docurec.valorpago) {opr} ?
        """
            # Valor total que o cliente deve
            vlr = 700

            result = cursor.execute(
                sql1, (data_inf_standard, data_sup_standard, vlr)
            )
            result = result.fetchall()
        except fdb.Error as e:
            print(f"Erro ao acessar o Firebird: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            connect.close()
            return result

    def number_processing(self, ans):
        filtered_ans = [item for item in ans if len(item[2]) == 13]
        return filtered_ans

    def to_delete_customers(self, excluded_customers, listed_customers):
        filtered_ans = [
            item
            for item in listed_customers
            if item[0] not in excluded_customers
        ]
        listed_customers.clear()
        listed_customers.extend(filtered_ans)
        return filtered_ans


if __name__ == "__main__":
    joelma = CustomersDatabase('joelma', '31/12/1900', '29/03/2025')
    matheus = CustomersDatabase('matheus', '31/12/1900', '29/03/2025')

    excluded_customers = [
        ('ADELINO CARNEIRO DE PAIVA')
    ]

    cliente_joelma = joelma.db_customers()
    cliente_joelma = joelma.number_processing(cliente_joelma)
    cliente_joelma_r = joelma.to_delete_customers(
        excluded_customers,
        cliente_joelma
    )

    for i in cliente_joelma_r:
        print(i)
