import time 
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor


def factorize(number):

    return list(filter(lambda x: number % x == 0, range(1, number+1)))


if __name__ == '__main__':

    numbers = [128, 255, 99999, 10651060]

    result = []

    start_time = time.time()

    with ProcessPoolExecutor(cpu_count()) as executor:

        for i in executor.map(factorize, numbers):
            result.append(i)

    end_time = time.time() - start_time

    print(result)
    print(end_time)