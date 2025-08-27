import time
import tracemalloc
import os


def get_errors_list(filename):
    errors = []
    with open(filename) as f:
        for line in f:
            if "ERROR" in line:
                errors.append(line.strip().upper())
    return errors


# log_path = os.path.join(os.path.dirname(__file__), "system.log")
# errors = get_errors_list(log_path)
# for e in errors:
#     print(e)


# --- List Version ---
start = time.time()
tracemalloc.start()
log_path = os.path.join(os.path.dirname(__file__), "system_big.log")
list_errors = get_errors_list(log_path)
print("List version - errors found:", len(list_errors))
print("Time:", time.time() - start, "seconds")
print("Memory:", tracemalloc.get_traced_memory()[1] / 1024 / 1024, "MB")
tracemalloc.stop()
