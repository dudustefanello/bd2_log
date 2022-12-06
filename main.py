from connection import get_connection
from initial import set_initial
from log import read_log


def main():
    initial = set_initial()

    logs = read_log()

    with get_connection() as conn:
        with conn.cursor() as curs:
            for log in logs:
                curs.execute(log[0])
                initial[log[1]][int(log[2]) - 1] = int(log[3])

    return {'INITIAL': initial}

if __name__ == '__main__':
    print(main())
