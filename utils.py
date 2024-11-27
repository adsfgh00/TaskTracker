import os
import json
import datetime


CURRENT_DIRECTORY = os.getcwd()
FILE_PATH = os.path.join(CURRENT_DIRECTORY, "task_list.json")


class utils:
    """Class that contains a set of utility functions"""

    @classmethod
    def create_task_file(cls):
        """This function creates a file 'task_list.json'

        Raises:
            Exception: Unexpected error occured

        """
        if not (os.path.isfile(FILE_PATH)):
            try:
                with open(FILE_PATH, "w") as new_file:
                    print(
                        f"file task_list.json created in '{CURRENT_DIRECTORY}'"
                    )
            except Exception as e:
                print(f"Error: {e}")

    @classmethod
    def read_task(cls, action=None) -> dict:
        """reads the task_list.json file

        Args:
            action (str, optional)[todo, in-progress, done]: The type of status will be shown. Defaults to None.

        Returns:
            dict: list of all tasks in dictionary form
        """
        current_tasks = []

        if os.path.getsize(FILE_PATH) != 0:
            try:
                with open(FILE_PATH, "r") as read_tasks:
                    current_tasks = json.load(read_tasks)
                    if action is not None:
                        current_tasks = cls.filter_task(current_tasks, action)
            except Exception as e:
                print(f"Error: {e}")
        return current_tasks

    @staticmethod
    def filter_task(current_tasks: list, action: str) -> dict:
        """Returns a filtered tasks based on status

        Args:
            current_tasks (list): current list of task
            action (str): The type of status

        Returns:
            dict: filtered task that only contains the input action
        """
        filtered_task = {}
        for x in current_tasks["list_of_tasks"]:
            if current_tasks["list_of_tasks"][x]["status"] == action:
                filtered_task[x] = current_tasks["list_of_tasks"][x]
        return filtered_task

    @staticmethod
    def generate_id(current_task: dict) -> int:
        """Generates a unique id

        Args:
            current_task (dict): dictionary containing all the tasks on task_list.json file

        Returns:
            int: generated unique id
        """
        for id in range(0, len(current_task["list_of_tasks"]) + 1, 1):
            if str(id) in current_task["list_of_tasks"]:
                continue
            else:
                return id
        return id

    @classmethod
    def write_task(cls, current_task: dict, task: str) -> None:
        """writes on the task_list.json file and checks if the file is empty or not

        Args:
            current_task (dict): dictionary containing all the tasks on task_list.json file
            task (str): task description

        Raises:
            FileNotFoundError: task_list.json cannot be found
            Exception: Unexpected error occured
        """
        id = 0
        if "list_of_tasks" in current_task:
            id = cls.generate_id(current_task)
            try:
                with open(FILE_PATH, "w") as write_tasks:
                    current_task["list_of_tasks"][id] = {
                        "description": task,
                        "status": "todo",
                        "createdAt": datetime.datetime.now().strftime(
                            "%Y-%b-%d %H:%M:%S"
                        ),
                        "updatedAt": datetime.datetime.now().strftime(
                            "%Y-%b-%d %H:%M:%S"
                        ),
                    }

                    json.dump(current_task, write_tasks, indent=4)

            except FileNotFoundError as e:
                print("task_list.json cannot be found")
            except Exception as e:
                print(f"Error: {e}")
        else:
            try:
                with open(FILE_PATH, "w") as write_tasks:
                    list_of_task = {
                        "list_of_tasks": {
                            id: {
                                "description": task,
                                "status": "todo",
                                "createdAt": datetime.datetime.now().strftime(
                                    "%Y-%b-%d %H:%M:%S"
                                ),
                                "updatedAt": datetime.datetime.now().strftime(
                                    "%Y-%b-%d %H:%M:%S"
                                ),
                            }
                        }
                    }
                    json.dump(list_of_task, write_tasks, indent=4)

            except FileNotFoundError as e:
                print("task_list.json cannot be found")
            except Exception as e:
                print(f"Error: {e}")

    @classmethod
    def process_task(cls, task_options: dict) -> None:
        """writes on a specific task id based on the options provided

        Args:
            task_options (dict): contains the fields that needed for an update

        Raises:
            FileNotFoundError: task_list.json cannot be found
            Exception: Unexpected error occured
        """
        current_task = task_options["current_task"]
        id = task_options["id"]
        if str(id) in current_task["list_of_tasks"]:
            try:
                with open(FILE_PATH, "w") as write_tasks:
                    if task_options["operation"] == "update task":
                        current_task = cls.update_task(
                            current_task,
                            id,
                            task_options["task"],
                        )
                    elif task_options["operation"] == "delete task":
                        current_task = cls.delete_task(
                            current_task,
                            id,
                        )
                    elif task_options["operation"] == "update status":
                        current_task = cls.update_status(
                            current_task,
                            id,
                            task_options["status"],
                        )
                    json.dump(current_task, write_tasks, indent=4)
            except FileNotFoundError as e:
                print("task_list.json cannot be found")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(
                "Invalid id. Please check tasktracker.py if the id already exists. Try Again"
            )

    @staticmethod
    def update_task(current_task: dict, id: int, task: str) -> dict:
        """performs an update on current_task dictionary

        Args:
            current_task (dict): dictionary containing all the tasks on task_list.json file
            id (int): task id that will get updated
            task (str): updated description

        Returns:
            dict: current_task that now contains the updated task
        """
        current_task["list_of_tasks"][id]["description"] = task
        current_task["list_of_tasks"][id][
            "updatedAt"
        ] = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
        return current_task

    @staticmethod
    def update_status(current_task: dict, id: int, status: str) -> dict:
        """performs an update on current_task dictionary

        Args:
            current_task (dict): dictionary containing all the tasks on task_list.json file
            id (int): task id that will get updated
            status (str): updated status

        Returns:
            dict: current_task that now contains the updated status
        """
        current_task["list_of_tasks"][id]["status"] = status
        current_task["list_of_tasks"][id][
            "updatedAt"
        ] = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
        return current_task

    @staticmethod
    def delete_task(
        current_task: dict,
        id: int,
    ) -> dict:
        """performs a delete on current_task dictionary

        Args:
            current_task (dict): dictionary containing all the tasks on task_list.json file
            id (int): task id that will get deleted

        Returns:
            dict: current_task minus the deleted task
        """
        del current_task["list_of_tasks"][id]
        return current_task
