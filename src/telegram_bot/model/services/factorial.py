from multiprocessing.pool import ThreadPool


def calculate_factorial_range(start, end, cache=None):
    if cache is None:
        cache = {}
    result = 1
    for i in range(start, end + 1):
        if i in cache:
            result *= cache[i]
        else:
            result *= i
            cache[i] = result
    return result


def calculate_factorial_threaded(number: int) -> int:
    half = number // 2
    cache = {}

    pool = ThreadPool(processes=2)
    result1 = pool.apply_async(calculate_factorial_range, args=(1, half, cache))
    result2 = pool.apply_async(calculate_factorial_range, args=(half + 1, number, cache))

    pool.close()
    pool.join()
    return result1.get() * result2.get()


def calculate_and_print_factorial(number: int):
    if number > 1000 or number < -1000:
        result = calculate_factorial_threaded(number)
        result_str = str(result)[:5]
    else:
        result_str = str(calculate_factorial_threaded(number))
    return result_str
