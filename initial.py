import json

from connection import get_connection


def set_initial():
    insert = True
    initial = json.loads(open('metadado.json').read())['INITIAL']
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute('TRUNCATE TABLE tabela;')

            for i in initial:
                for j in range(0, len(initial[i])):
                    if insert:
                        curs.execute('INSERT INTO tabela (id, {}) VALUES ({}, {})'.format(i, j + 1, initial[i][j]))
                    else:
                        curs.execute('UPDATE tabela SET {} = {} WHERE id = {};'.format(i, initial[i][j], j + 1))

                insert = False
    return initial

if __name__ == '__main__':
    set_initial()