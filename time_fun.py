from task import Task
import sys


if __name__ == "__main__":
    user_task = Task(sys.argv[1:])
    user_task.progress()
