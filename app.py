from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('todo-list', user='', password = '', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Tasks(BaseModel):
  task = CharField()

class Dates(BaseModel):
  due_date = CharField()
  task_id = IntegerField()

db.connect()
# db.drop_tables([Tasks,Dates])
# db.create_tables([Tasks,Dates])

app = Flask(__name__)

# Tasks(task='Feed the cat').save()
# Tasks(task='BLALALAL').save()

@app.route('/', methods=['GET','POST'])
@app.route('/task/', methods=['GET', 'POST'])
@app.route('/task/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
      return jsonify(model_to_dict(Tasks.get(Tasks.id == id)))
    else:
      taskslist = []
      for task in Tasks.select():
        taskslist.append(model_to_dict(task))
      return jsonify(taskslist)

  if request.method == 'PUT':
    body = request.get_json()
    Tasks.update(body).where(Tasks.id == id).execute()
    return 'Task updated successfully'   

  if request.method == 'POST':
    new_task = dict_to_model(Tasks, request.get_json())
    new_task.save()
    return jsonify({"success": True})  

  if request.method == 'DELETE':
    Tasks.delete().where(Tasks.id == id).execute()
    return 'DELETE request successful'


app.run(debug=True, port=9000)