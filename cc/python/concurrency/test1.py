# SuperFastPython.com
# example of waiting for tasks to complete
from time import sleep
from random import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import concurrent.futures

def task(name):
    # sleep for less than a second
    sleep(random())
    print(f'Done: {name}')

# start the thread pool
with ThreadPoolExecutor(2) as executor:
    # submit tasks and collect futures
    futures = [executor.submit(task, i) for i in range(10)]
    # wait for all tasks to complete
    print('Waiting for tasks to complete...')
    try:
        wait(futures, timeout=1, return_when=concurrent.futures.ALL_COMPLETED)
    except concurrent.futures.TimeoutError as e:
        print('HERE')
        print(e)

    print('All tasks are done!')