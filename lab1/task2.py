import threading
import time
import random as rnd
import numpy as np


def sequential_matmul(A, B):
    res = [
        [0 for _ in range(k)]
        for _ in range(m)
    ]

    for row in range(m):
        for col in range(k):
            for elt in range(n):
                res[row][col] += A[row][elt] * B[elt][col]

    return res


class Thread(threading.Thread):
    def __init__(self, A, B, res, row_ind):
        super().__init__()
        self.A = A
        self.B = B
        self.res = res
        self.row_ind = row_ind

    def run(self):
        inner_prod(self.A, self.B, self.res, self.row_ind)


def inner_prod(A, B, res, row_ind):
    row = [0] * k
    for i in range(k):
        for j in range(n):
            row[i] += A[row_ind][j] * B[j][i]
    res[row_ind] = row


def parallel_matmul(A, B):
    res = [
        [0] for _ in range(m)
    ]

    threads = []
    for i in range(m):
        thread = Thread(A, B, res, i)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return res


if __name__ == '__main__':
    m, n, k = [rnd.randint(200, 300) for i in range(3)]

    A = [
        [rnd.randint(1, 10) for _ in range(n)]
        for _ in range(m)
    ]
    B = [
        [rnd.randint(1, 10) for _ in range(k)]
        for _ in range(n)
    ]

    start_time = time.time()
    seq_res = sequential_matmul(A, B)
    exec_time = time.time() - start_time
    print(f'Sequential time: ', exec_time)

    start_time = time.time()
    par_res = parallel_matmul(A, B)
    exec_time = time.time() - start_time
    print(f'Parallel time: ', exec_time)

    np_ans = np.dot(A, B)

    assert (np_ans == seq_res).all()
    assert (np_ans == par_res).all()
    assert seq_res == par_res
