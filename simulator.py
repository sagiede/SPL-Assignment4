import sqlite3
import os
dbcon = sqlite3.connect('world.db')


def count_available_tasks():
    cursor = dbcon.cursor()
    cursor.execute("SELECT COUNT(id) FROM tasks")
    return cursor.fetchone()[0]


def main():
    with dbcon:
        cursor = dbcon.cursor()

        while count_available_tasks() > 0 and os.path.isfile('world.db'):
            cursor.execute("SELECT * FROM tasks ORDER BY id")
            tasks = cursor.fetchall()

            for task in tasks:
                if task[3] == 0:
                    cursor.execute("SELECT * FROM workers WHERE id = ?", [task[2]])
                    worker = cursor.fetchone()
                    cursor.execute("DELETE FROM tasks WHERE id = ?", [task[0]])
                    cursor.execute("UPDATE workers SET status = ? WHERE id = ?", ['idle', worker[0]])
                    print('{name} says: All Done!'.format(name=worker[1]))

            cursor.execute("SELECT * FROM tasks ORDER BY id")
            tasks = cursor.fetchall()
            for task in tasks:
                cursor.execute("SELECT * FROM workers WHERE id = ?", [task[2]])
                worker = cursor.fetchone()
                if worker is not None:
                    if worker[2] == "idle":
                        if task is not None:
                            cursor.execute("UPDATE workers SET status = ? WHERE id = ?", ['busy', worker[0]])
                            cursor.execute("UPDATE resources SET amount = amount - ? WHERE name = ?", [task[5], task[4]])
                            print('{name} says: work work'.format(name=worker[1]))
                    elif worker[2] == "busy":
                        cursor.execute("SELECT * FROM tasks WHERE worker_id=? ORDER BY id", [worker[0]])
                        current_task = cursor.fetchone()
                        if current_task[0] == task[0]:
                            cursor.execute("UPDATE tasks SET time_to_make = time_to_make - 1 WHERE id = ?", [task[0]])
                            print('{name} is busy {task_name}...'.format(name=worker[1], task_name=task[1]))
                    dbcon.commit()


if __name__ == '__main__':
    main()
