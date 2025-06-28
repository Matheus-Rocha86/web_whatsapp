import fdb


class CustomersDatabase:
    """
    Realiza operações de busca no banco de dados alvo.
    Os objetos da classe são uma lista de tuplas com
    três variáveis.

    :param user: nome do usuário cobrador.
    :param data_inf: data inicial no formato, xx/xx/xxxx.
    :param data_sup: data final no formato, xx/xx/xxxx.
    """
    def __init__(self, user: str, data_inf: str, data_sup: str, excluded_customers: list, inserted_customers: list):
        self.user = user
        self.data_inf = data_inf
        self.data_sup = data_sup
        self.excluded_customers = excluded_customers
        self.inserted_customers = inserted_customers

    def db_customers(self):
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
                sql1, (self.data_inf, self.data_sup, vlr)
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

            # Changes in the customer list
            customers_list = self.number_processing(result)
            customer_list_some_deleted = self.to_delete_customers(
                self.excluded_customers, customers_list
            )
            if self.inserted_customers[0] != '':
                customer_list_some_inserted = self.to_insert_customers(
                    self.inserted_customers, customer_list_some_deleted
                )
                return customer_list_some_inserted
            return customer_list_some_deleted

    def number_processing(self, ans):
        """Filters numbers equal to 13 digits"""

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

    def to_insert_customers(self, inserted_customers, list_customers: list):
        for customer in inserted_customers:
            list_customers.append(customer)
        return list_customers
