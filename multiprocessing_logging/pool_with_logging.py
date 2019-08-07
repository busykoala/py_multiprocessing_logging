from multiprocessing.pool import Pool
import logging
import multiprocessing
import sys

RUN = 0
CLOSE = 1
TERMINATE = 2

# python version dependent import
# python < 3.2 does not provide methods in std. lib
if sys.version_info < (3, 2):
    from logutils.queue import QueueHandler, QueueListener
else:
    from logging.handlers import QueueHandler, QueueListener


class PoolWithLogging(Pool):
    """Custom multiprocessing Pool logging using the defined logger

    This class is though as an extension of 'multiprocessing.Pool' to be able
    to use the logger in the worker function of doing multiprocessing.
    """

    def __init__(self, processes=None, logger_name=None):
        if not logger_name:
            logger_name = __name__
        self.logger_name = logger_name
        self.mp_queue_listener, self.mp_queue = self.logger_init()
        initargs = tuple([self.mp_queue])
        initializer = self.worker_init(self.mp_queue)
        super(PoolWithLogging, self).__init__(processes=processes,
                                              initializer=initializer,
                                              initargs=initargs)

    def close(self):
        super(PoolWithLogging, self).close()
        self.mp_queue_listener.stop()

    def worker_init(self, mp_queque):
        # all records from worker processes go to qh and then into q
        qh = QueueHandler(mp_queque)
        logger = logging.getLogger(self.logger_name)
        logger.addHandler(qh)

    def logger_init(self):
        mp_queue = multiprocessing.Queue()
        # this is the handler for all log records
        handler = logging.StreamHandler()

        # ql gets records from the queue and sends them to the handler
        mp_queue_listener = QueueListener(mp_queue, handler)
        mp_queue_listener.start()

        logger = logging.getLogger(self.logger_name)
        # add handler to logger so records from this process are handled
        logger.addHandler(handler)

        return mp_queue_listener, mp_queue
