def format_print(data):
    # Imprime o cabeçalho
    print(f"{'NOME':<60} | {'VALOR':<10} | {'TELEFONE':>14}")
    print("-" * 90)

    # Imprime os dados
    for nome, valor, telefone in data:
        print(f"{nome:<60} | {valor:>10.2f} | {telefone:<14}")
    print("-" * 90)
