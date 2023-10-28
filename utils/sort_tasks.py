import datetime


def sort_tasks(tasks: list[dict]):
    for i in range(len(tasks) - 1):
        for j in range(len(tasks) - i - 1):
            if tasks[j]["deadline"] is not None:
                current_task = datetime.datetime.strptime(tasks[j]["deadline"], '%d-%m-%Y')
            else:
                current_task = datetime.datetime(datetime.MAXYEAR, 12, 31)

            if tasks[j + 1]["deadline"] is not None:
                next_task = datetime.datetime.strptime(tasks[j + 1]["deadline"], '%d-%m-%Y')
            else:
                next_task = datetime.datetime(datetime.MAXYEAR, 12, 31)

            if current_task > next_task:
                tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]

    return tasks
