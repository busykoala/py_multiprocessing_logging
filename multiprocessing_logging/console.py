from datetime import datetime
import logging
import multiprocessing
import os
import sys

# python version dependent import
# python < 3.2 does not provide methods in std. lib
if sys.version_info < (3, 2):
    from logutils.queue import QueueHandler, QueueListener
else:
    from logging.handlers import QueueHandler, QueueListener

current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, 'log_example.log')
logging.basicConfig(filename=log_path)
# test_logger = logging.getLogger('test_logger')


def do_job(i):
    # time.sleep(random())
    logging.info('do_job called with: {} => {}'.format(i, datetime.now()))
    return i*2


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
    processes = 100
    q_listener, q = logger_init()

    logging.info('Hi, I\'m the main thread')

    pool = multiprocessing.Pool(processes, worker_init, [q])
    return_values = pool.map(do_job, tasks)

    print(return_values)

    pool.close()
    pool.join()
    q_listener.stop()


if __name__ == '__main__':
    main()
