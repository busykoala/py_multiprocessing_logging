from multiprocessing import Pool
from time import sleep
import datetime


ELEMENTS = [True for v in range(1000)]


def repeat_for_each_element(element):
    print(datetime.datetime.now())
    sleep(1)


def main():
    pool = Pool(processes=100)
    pool.map(repeat_for_each_element, ELEMENTS)


if __name__ == "__main__":
    main()
