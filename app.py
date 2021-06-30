from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo.db').replace("://"
                                                                                                           , "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<{self.text}>'


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        date = datetime.today().strftime("%d/%A/%B/%Y")
        all_tasks = Task.query.all()

        return render_template('index.html', date=date, all_tasks=all_tasks)
    elif request.method == 'POST':
        task = request.form['task-text']
        to_add = Task(text=task)
        db.session.add(to_add)
        db.session.commit()
        return redirect('/')


@app.route('/delete/<int:task_id>')
def delete(task_id):
    to_delete = Task.query.get(task_id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
