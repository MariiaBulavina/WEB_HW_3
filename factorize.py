import time


def factorize(number):
    return list(filter(lambda x: number % x == 0, range(1, number+1)))


if __name__ == '__main__':

    numbers = [128, 255, 99999, 10651060]
    start_time = time.time()
    result = list(map(factorize, numbers))
    end_time = time.time() - start_time

    print(result)
    print(end_time) 