import random

messages = [
    "INFO: System started",
    "ERROR: Disk full",
    "WARNING: CPU usage high",
    "INFO: User login",
    "ERROR: Network unreachable",
    "INFO: Shutdown complete",
]

with open("system_big.log", "w") as f:
    for _ in range(1_000_000):
        f.write(random.choice(messages) + "\n")
