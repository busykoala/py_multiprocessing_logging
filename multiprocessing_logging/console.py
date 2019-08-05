from datetime import datetime
from random import randrange
import logging
import multiprocessing
import os
import sys
import time

# python version dependent import
# python < 3.2 does not provide methods in std. lib
if sys.version_info < (3, 2):
    from logutils.queue import QueueHandler, QueueListener
else:
    from logging.handlers import QueueHandler, QueueListener

current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, 'log_example.log')
logging.basicConfig(filename=log_path)


def do_job(task):
    random_int = randrange(10)
    time.sleep(random_int)
    logging.info('do_job called with: {} => {}'.format(task, datetime.now()))
    return random_int


def worker_init(q):
    # all records from worker processes go to qh and then into q
    qh = QueueHandler(q)
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(qh)


def logger_init():
    q = multiprocessing.Queue()
    # this is the handler for all log records
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - %(message)s"))

    # ql gets records from the queue and sends them to the handler
    ql = QueueListener(q, handler)
    ql.start()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # add the handler to the logger so records from this process are handled
    logger.addHandler(handler)

    return ql, q


def main():
    tasks = [x for x in range(100)]
    # if there is no danger that the system can't handle the processes
    # it seems to be best to assign as many processes as there are tasks
    # to get the maximum speed for I/O tasks.
    processes = 100
    q_listener, q = logger_init()

    test_logger = logging.getLogger('test_logger')
    test_logger.info('Hi, I\'m the main thread')

    pool = multiprocessing.Pool(processes, worker_init, [q])

    start_time = time.time()
    return_values = pool.map(do_job, tasks)
    end_time = time.time()

    pool.close()
    pool.join()
    q_listener.stop()

    test_logger.info('Hi, from the main thread again')
    print('*** Handling all tasks took {} seconds ***'.format(
        end_time - start_time))

if __name__ == '__main__':
    main()
