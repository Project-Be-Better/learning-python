import time
import tracemalloc
import os


def error_generator(filename):
    with open(filename) as f:
        for line in f:
            if "ERROR" in line:
                yield line.strip().upper()


# for e in error_generator("system.log"):
#     print(e)
start = time.time()
tracemalloc.start()
log_path = os.path.join(os.path.dirname(__file__), "system_big.log")
gen_errors = error_generator(log_path)
count = sum(1 for _ in gen_errors)
print("Generator version - errors found:", count)
print("Time:", time.time() - start, "seconds")
print("Memory:", tracemalloc.get_traced_memory()[1] / 1024 / 1024, "MB")
tracemalloc.stop()
