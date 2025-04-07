import sqlite3
from datetime import datetime

# --- Database Setup ---
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        due_date TEXT,
        completed INTEGER DEFAULT 0
    )
''')
conn.commit()


# --- Functions ---
def add_task(title, due_date):
    cursor.execute("INSERT INTO tasks (title, due_date) VALUES (?, ?)", (title, due_date))
    conn.commit()
    print(" Task added!")


def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print(" No tasks found.")
    else:
        for task in tasks:
            status = "" if task[3] else ""
            print(f"[{task[0]}] {status} {task[1]} (Due: {task[2]})")


def mark_completed(task_id):
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    print(" Task marked as completed!")


def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print(" Task deleted!")


# --- Main Menu ---
def main():
    while True:
        print("\n  Task Tracker Menu")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task Title: ")
            due_date = input("Due Date (YYYY-MM-DD): ")
            try:
                datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
                add_task(title, due_date)
            except ValueError:
                print(" Invalid date format.")
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            task_id = int(input("Enter Task ID to mark as completed: "))
            mark_completed(task_id)
        elif choice == "4":
            task_id = int(input("Enter Task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice. Try again.")

    conn.close()

if __name__ == "__main__":
    main()
