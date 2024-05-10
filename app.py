from flask import Flask, render_template,url_for,request,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer,default = 0)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return self.content
    
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        

        except:
            return 'Error committing to the database'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks, message='successful')
       

@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Todo.query.get(id)
    
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'error deleting'


@app.route('/update/<int:id>',methods = ['POST','GET'])
def update(id):
    task = Todo.query.get(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'error updating'

    else:
        return render_template('update.html',task_update=task)

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
