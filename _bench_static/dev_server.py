"""Tiny long-running script used as a fixture for background-process tool
scenarios (run_background_command / task_output / task_stop /
list_background_tasks). Ticks forever until killed."""
import time

if __name__ == "__main__":
    i = 0
    while True:
        i += 1
        print(f"tick {i}", flush=True)
        time.sleep(1)
