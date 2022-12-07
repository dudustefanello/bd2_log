import re

def get_log_lines():
    return open('entrada.log').read().splitlines()

def compare(e):
    return e[1]

def read_log():
    lines = get_log_lines()
    transactions = []
    transactions2 = []
    redo = set()
    operacoes = []
    commits = {}
    i = 0
    for i in range(len(lines) - 1, 0, -1):
        check = re.search('<CKPT \(([T0-9,]+)\)>', lines[i])
        if check:
            transactions = check[1].split(',')
            transactions2 = check[1].split(',') # apenas para imprimir saída
            continue

        start = re.search('<start (T[0-9]+)>', lines[i])
        if (
            start
            and start[1] in transactions # start de transação do Checkpoint
        ):
            transactions.pop(transactions.index(start[1]))
            if len(transactions) == 0:
                break # encontrou o último start das transações do Checkpoint
            continue

        commit = re.search('<commit (T[0-9]+)>', lines[i])
        if commit and commit[1] not in commits:
            # armazena a linha, para não fazer operações após o último commit
            commits.update({commit[1]: i})

    for j in range(i, len(lines) - 1):
        operacao = re.search('<(T[0-9]+),([0-9]+),([A-Z]),[0-9]+,([0-9]+)>', lines[j])
        if (
            operacao and operacao[1] in commits # Transação commitou
            and commits[operacao[1]] > j        # Commitou após a linha atual
        ):
            operacoes.append((
                'UPDATE tabela SET {} = {} WHERE id = {};'.format(operacao[3], operacao[4], operacao[2]),
                operacao[3], operacao[2], operacao[4],
            ))
            redo.add(operacao[1])

    for i in redo:
        if i in transactions2:
            transactions2.remove(i)
        print('Transação {} realizou REDO'.format(i))

    for i in transactions2:
        print('Transação {} não realizou REDO'.format(i))

    return operacoes


if __name__ == '__main__':
    print(read_log())
