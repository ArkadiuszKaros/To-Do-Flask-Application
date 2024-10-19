# Importing libraries

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import random


# Configure Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    insert_date = db.Column(db.DateTime, nullable = False)

with app.app_context():
    db.create_all()

cirles = []

for _ in range(45):
    size = random.randint(50, 150)  
    position_x = random.uniform(0, 100)  
    position_y = random.uniform(0, 100)  

    cirles.append({
            "size": size,
            "position_x": position_x,
            "position_y": position_y
        })

@app.route('/')
def start():
    tasks = Task.query.all()

    return render_template('start.html', tasks=tasks, circles=cirles)

@app.route('/add', methods = ['POST'])
def add_task():
    new_task_name = request.form.get('newTask')
    new_task = Task(
        text=new_task_name,
        insert_date=datetime.now()
    )
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('start'))

@app.route('/remove/<int:task_id>', methods = ['POST'])
def remove_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('start'))

if __name__ == "__main__":
    app.run(debug=True)
