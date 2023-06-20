#PATHETICALLY WRITTEN

# Hey All: As of version SQLAlchemy 3.0 to create your db file you will need to run some commands like this in the shell :
# from project import app, db
# app.app_context().push()
# db.create_all()

# Then the .db file is created in a folder called "Instance" in your project. 

# Hope this helps some one

from flask_pymongo import PyMongo    
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/firstApplication")
dbno = mongodb_client.db


class Tasks(db.Model):
    taskid = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String,nullable=False)
    priority = db.Column(db.Integer,nullable=False,default=100)

    def __repr__(self):
        return f"TaskID : {self.taskid},task : {self.task},priority : {self.priority}"

sampleTodos= [   {
                'name':'do the dishesc mate',
                'priority':'4'
                },
                {
                'name':'study',
                'priority':'2'
                },
                {
                'name':'clean the house',
                'priority':'1'
                },
                {
                'name':'get a life',
                'priority':'3'
                } ]

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/methods/<name>', methods=['GET','POST'])
def method(name):
    if name == 'get':
        todos = Tasks.query.all()
        print(todos)
        return render_template('methods/get.html', todos=todos,count=0)
    if name == 'post':
        if request.method == 'POST':
            task = request.form['task']
            priority = request.form['priority']
            newTask = {'name': task,'priority' : priority}
            sampleTodos.append(newTask)
            print(sampleTodos)
            taskObject = Tasks(task=task,priority=priority)
            db.session.add(taskObject)
            db.session.commit()
            return render_template('methods/post.html',added=True)
        return render_template('methods/post.html',added=False)

    if name == 'put':
        return render_template('methods/put.html')
    if name == 'delete':
        return render_template('methods/delete.html')
    
@app.route('/methods/delete/<int:id>')
def delete(id):
    tsk=Tasks.query.get(id)
    db.session.delete(tsk)
    db.session.commit()
    todos = Tasks.query.all()
    print(todos)
    return render_template('methods/get.html', todos=todos,count=0)
    
@app.route('/mongo' ,methods=['POST','GET'])
def addDB():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        newUser = {'name': name,'age' : age}
        #sampleTodos.append(newTask)        
        dbno.userDetails.insert_one(newUser)
        return render_template('formMongo.html' , added = True)

    return render_template('formMongo.html', added = False)

if __name__ == '__main__':
    app.run(debug = True)

