from flask import Flask, render_template, request, redirect, url_for
import json
import os



app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Helper function to get tasks
def get_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Helper function to save tasks
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

@app.route('/health', methods=['GET'])
def health_check():
    return "Healthy", 200

@app.route('/')
def index():
    tasks = get_tasks()
    # Sort days of the week in order
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    sorted_tasks = {day: tasks.get(day, []) for day in days_of_week}
    return render_template('index.html', tasks=sorted_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['taskName']
    task_duration = request.form['taskDuration']
    task_status = request.form['taskStatus']
    task_day = request.form['taskDay']

    tasks = get_tasks()

    if task_day not in tasks:
        tasks[task_day] = []

    new_task = {
        'name': task_name,
        'duration': task_duration,
        'status': task_status
    }

    tasks[task_day].append(new_task)
    save_tasks(tasks)

    return redirect(url_for('index'))

@app.route('/update_status/<task_day>/<task_index>', methods=['POST'])
def update_status(task_day, task_index):
    tasks = get_tasks()
    task = tasks[task_day][int(task_index)]

    new_status = request.form['taskStatus']
    task['status'] = new_status
    save_tasks(tasks)

    return redirect(url_for('index'))

@app.route('/delete_task/<task_day>/<task_index>', methods=['POST'])
def delete_task(task_day, task_index):
    tasks = get_tasks()
    del tasks[task_day][int(task_index)]

    # If there are no tasks left for the day, remove the day entry
    if not tasks[task_day]:
        del tasks[task_day]

    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
