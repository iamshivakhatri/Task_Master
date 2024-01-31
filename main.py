from datetime import datetime as dt
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods = ["POST", "GET"])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding the task to the database"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', task = tasks)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)