import os
import threading
import operator
import random as rnd


FILES_N = 9
DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'task3_files'
)


class Thread(threading.Thread):
    def __init__(self, filename, res):
        super().__init__()
        self.filename = filename
        self.res = res

    def run(self):
        self.res[0] += calc_file(self.filename)


def get_filename(i):
    return f'in_{i}.txt'


def generate_files():
    ops = ["+", "-", "*", "/"]

    for i in range(1, FILES_N+1):
        with open(os.path.join(DIR_PATH, get_filename(i)), 'w') as f:
            f.write(f'{rnd.choice(ops)}\n'
                    f'{rnd.randint(1, 10)} {rnd.randint(1, 10)}')


def write_res(res):
    with open(os.path.join(DIR_PATH, 'out.txt'), 'w') as f:
        f.write(str(res))


def calc_file(filename):
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    with open(os.path.join(DIR_PATH, filename), 'r') as f:
        lines = f.readlines()
        op = lines[0].replace('\n', '')
        vals = lines[1].split(' ')

        return operations[op](
            int(vals[0]),
            int(vals[1])
        )


def calc_files_parallel():
    res = [0]

    threads = []
    for i in range(1, FILES_N+1):
        thread = Thread(get_filename(i), res)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return res[0]


if __name__ == '__main__':
    generate_files()
    write_res(calc_files_parallel())
