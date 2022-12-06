import threading
import time


class Thread(threading.Thread):
    def __init__(self, rows, row_index):
        super().__init__()
        self.rows = rows
        self.row_index = row_index

    def run(self):
        print(f'Thread {self.row_index} started.')
        print_rows(self.rows)
        print(f'Thread {self.row_index} finished.')


def print_rows(rows):
    time.sleep(0.1)
    for row in rows:
        print(row)


if __name__ == '__main__':
    threads_n = 4
    threads = []

    rows_templates = [
        ['row1 item1', 'row1 item2', 'row1 item3'],
        ['row2 item1', 'row2 item2', 'row2 item3'],
        ['row3 item1', 'row3 item2', 'row3 item3'],
        ['row4 item1', 'row4 item2', 'row4 item3'],
    ]

    for i, rows in enumerate(rows_templates):
        thread = Thread(rows, i+1)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
