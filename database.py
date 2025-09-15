import psycopg2
from functools import wraps


def connection(func):
    """Decorator for connection/disconnection to/from database and save changes"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        con = psycopg2.connect(database="postgres", user="postgres", password="", host="127.0.0.1", port="5432")
        cur = con.cursor()
        output = func(cur, *args, **kwargs)
        con.commit()
        con.close()
        return output
    return wrapper


@connection
def _create_table(cur) -> None:
    cur.execute("""CREATE TABLE LEADERBOARD
    (DIFFICULTY TEXT NOT NULL,
    NICKNAME TEXT NOT NULL,
    SCORE INT NOT NULL);""")


@connection
def _drop_table(cur) -> None:
    cur.execute("""DROP TABLE LEADERBOARD""")


@connection
def _clear_table(cur) -> None:
    cur.execute("""DELETE FROM LEADERBOARD""")


@connection
def _reset_table(cur) -> None:
    cur.execute("""DELETE FROM LEADERBOARD""")
    dif_list = ['Normal', 'Hard', 'Hell', 'Challenge', 'Very easy', 'Easy']
    for dif in dif_list:
        for i in range(10):
            cur.execute("""INSERT INTO LEADERBOARD (DIFFICULTY, NICKNAME, SCORE) 
                    VALUES (%s, %s, %s)""", (dif, f'Unknown', 10 - i))


@connection
def write_data(cur, data: dict[str, list[tuple[str, int]]]) -> None:
    cur.execute("""DELETE FROM LEADERBOARD""")
    for difficulty in data.keys():
        for name, score in data[difficulty]:
            cur.execute("""INSERT INTO LEADERBOARD (DIFFICULTY, NICKNAME, SCORE) 
                VALUES (%s, %s, %s)""", (difficulty, name, score))


@connection
def read_data(cur) -> dict[str, list[tuple[str, int]]]:
    cur.execute("""SELECT DIFFICULTY, NICKNAME, SCORE FROM LEADERBOARD""")
    data = {}
    rows = cur.fetchall()
    for row in rows:
        try:
            data[row[0]].append(row[1:])
        except KeyError:
            data[row[0]] = [row[1:]]
    return data


@connection
def _print_data(cur) -> None:
    cur.execute("""SELECT DIFFICULTY, NICKNAME, SCORE FROM LEADERBOARD""")
    data = {}
    rows = cur.fetchall()
    for row in rows:
        try:
            data[row[0]].append(row[1:])
        except KeyError:
            data[row[0]] = [row[1:]]
    for k, v in data.items():
        print('\n', k, sep='')
        for value in v:
            print(*value)


if __name__ == '__main__':
    #_print_data()
    print(read_data())
