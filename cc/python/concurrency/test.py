# SuperFastPython.com
# example of waiting for tasks to complete
from time import sleep
from random import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import concurrent.futures
# from concurrent.futures import TimeoutError

# custom task that will sleep for a variable amount of time
def task1(name):
    # sleep for less than a second
    sleep(random())
    print(f'Task 1 done: {name}')

def task2(name):
    # sleep for less than a second
    sleep(random())
    print(f'Task 2 done: {name}')    

empty_list = []
with ThreadPoolExecutor() as executor:
    task1_futures = [executor.submit(task1, i) for i in range(10)]
    task2_futures = [executor.submit(task2, i) for i in empty_list]

    # futures = task1_futures + task2_futures

    done, not_done = wait(task1_futures + task2_futures)
    print('here')


