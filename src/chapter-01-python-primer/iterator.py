import os


def read_lines(filename):
    """Yield lines from a file, line by line"""
    with open(filename) as f:
        for line in f:
            yield line.strip()


def filter_errors(lines):
    """Yield only lines with the ERROR"""
    for line in lines:
        if "ERROR" in line:
            print(">> Error is found")
            yield line


if __name__ == "__main__":
    log_path = os.path.join(os.path.dirname(__file__), "system.log")
    lines = read_lines(log_path)
    errors = filter_errors(lines)

    for error in errors:
        print(error)
