import cmd

from utils import utils as u


class TaskTracker(cmd.Cmd):
    """Class that contains all the cli commands that will be performed"""

    prompt = "TaskTracker>> "
    intro = "Hello, type help for the list of available commands."

    def __init__(self):
        super().__init__()

    def do_add(self, args: str) -> None:
        """Adds a task, creates task_list.json if it does not exists

        Args:
            args (str): task description that will be added
        """
        u.create_task_file()
        current_tasks = u.read_task()
        u.write_task(current_tasks, args)

    def do_update(self, args: str) -> None:
        """update a task

        Args:
            args: Format must be "ID(int), task(str)"
            example: update 1 update my task
        """
        args_list = args.split(" ", 1)
        task_options = {
            "id": args_list[0],
            "task": args_list[1],
            "current_task": u.read_task(),
            "operation": "update task",
        }
        u.process_task(task_options)

    def do_delete(self, args: int) -> None:
        """delete a task

        Args:
            args (int): id of the task that will be deleted
        """
        task_options = {
            "id": args,
            "current_task": u.read_task(),
            "operation": "delete task",
        }
        u.process_task(task_options)

    def do_mark_in_progress(self, args: int) -> None:
        """update status to in-progress

        Args:
            args (int): id of the task that will be updated
        """
        task_options = {
            "id": args,
            "status": "in-progress",
            "current_task": u.read_task(),
            "operation": "update status",
        }
        u.process_task(task_options)

    def do_mark_done(self, args: int) -> None:
        """update status to done

        Args:
            args (int): id of the task that will be updated
        """
        task_options = {
            "id": args,
            "status": "done",
            "current_task": u.read_task(),
            "operation": "update status",
        }
        u.process_task(task_options)

    def do_list(self, args=None):
        """Shows all the list of task with or without actions

        Args:
            args (str): the status that will be shown

        Raises:
            Exception: When the input is not "done, in-progress or todo"
        """
        if args == "done" or args == "in-progress" or args == "todo":
            current_tasks = u.read_task(args)
            [print(f"{key}: {value}") for key, value in current_tasks.items()]
        elif args == "":
            args = None
            current_tasks = u.read_task(args)
            [
                print(f"{key}: {value}")
                for key, value in current_tasks["list_of_tasks"].items()
            ]

        else:
            raise (Exception("Available options are: done, in-progress, todo"))

    def do_exit(self, args) -> bool:
        """exits the program

        Returns:
            True: boolean
        """
        return True


def main():
    run_task_tracker = TaskTracker()
    run_task_tracker.cmdloop()


if __name__ == "__main__":
    main()
