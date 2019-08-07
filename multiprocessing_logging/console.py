from datetime import datetime
from multiprocessing_logging.pool_with_logging import PoolWithLogging
from random import randrange
import logging
import time


def do_job(task):
    random_int = randrange(10)
    time.sleep(random_int)
    logging.info('func called with task: {}'.format(task))
    return random_int


def main():
    # setup logger
    test_logger = logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(asctime)s - %(process)s - %(message)s')
    logger_name = 'test_logger'
    test_logger = logging.getLogger(logger_name)

    tasks = [x for x in range(100)]
    # if there is no danger that the system can't handle the processes
    # it seems to be best to assign as many processes as there are tasks
    # to get the maximum speed for I/O tasks.
    processes = 100

    test_logger.info('Hi, I\'m the main thread')

    pool = PoolWithLogging(processes=processes,
                           logger_name=logger_name)
    start_time = time.time()
    return_values = pool.map(do_job, tasks)
    end_time = time.time()
    pool.close()

    test_logger.info('Hi, from the main thread again.')

    print('*** Handling all tasks took {} seconds ***'.format(
        end_time - start_time))


if __name__ == '__main__':
    main()
