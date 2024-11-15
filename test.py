import json
from flask import Flask, request, render_template, url_for
app = Flask(__name__)

#Lista tasks1.json i html format och även i hemsidan
@app.route("/")
def index():
    with open("tasks1.json", "r") as file:
         tasks=json.load(file)   
    return render_template("index.html", tasks=tasks)

# Lista json filen i postman som jsonfil 
@app.route("/Todo", methods = ["GET"])
def show_list():
     with open("tasks1.json", "r") as f:
          show = json.load(f)
     return show

#routen används för att lägga en ny task genom Postman
@app.route("/Todo/add",methods=["POST"])
def add_new():
     with open("tasks1.json", "r") as file:
          add_task = json.load(file) 
          
     data=request.get_json()
     id = data.get("id")
     description = data.get("description")
     category = data.get("category")
     status = data.get("status")
     if not category or not description or not id or status is None:
          return {"OBS": " Du måste lägga till id, description, category och status! "}, 400
     
     add_task.append(data)
     with open("tasks1.json", "w") as file:
          json.dump(add_task, file, indent=4)

     return {"msg": "Tasken har lagts till!"} 

#routen ska användas för att söka efter en task med hjälp av id i Postman 
@app.route("/Todo/search/<int:id>", methods=["GET"])
def search(id):
     with open("tasks1.json") as f:
          data = json.load(f)

     task = next ((i for i in data if i["id"] == id), None)
     if task:
          return task
     return f"Task with ID {id} not found", 404

#routen används för att ta bort en task i postman     
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
     with open("tasks1.json", "r") as f:
          data = json.load(f)
    
     lenght = len(data) 
     data = [tasks1 for tasks1 in data if tasks1.get("id") != id]
     if len(data) == lenght:
        return {"error": f"Task with ID{id} not found"}, 404
     with open("tasks1.json", "w") as f:
          json.dump(data, f, indent=4)
     return {"msg": f"Task with ID {id} has succesfully deleted!"}, 200


@app.route("/uppdate/<int:id>", methods=["PUT"])
def uppdate_task(id):
     with open("tasks1.json", "r") as f:
          data = json.load(f)

     task = next((t for t in data if t["id"] == id), None)
     if task is None:
          return {"error": "Task hittades inte"}, 404

     update_data = request.get_json()
     if not update_data:
          return {"msg": "No data to uppdate"}, 400

     for key, value in update_data.items():
          if key in task:
               task[key]=value
    
     with open ("tasks1.json", "w") as f:
          json.dump(data, f, indent=4)
     
     return{"msg": "The task has succesfully uppdated", "task": task}, 200
     
@app.route("/tasks/complete/<int:id>", methods=["PUT"])
def complete_task(id):
     with open("tasks1.json", "r") as f:
          data = json.load(f)

     i = next((t for t in data if t["id"] == id), None)
     if i is None:
          return {"error": "Task hittades inte"}, 404

     i ["status"] = "completed"

     with open ("tasks1.json", "w") as f:
          json.dump(data, f, indent=4)
          return{"msg": "The task has succesfully uppdated", "task": i}, 200
     
@app.route("/tasks/category/<string:category>", methods=["GET"])
def open_by_category(category):
     with open("tasks1.json", "r") as f:
          cat_data = json.load(f)

     e = [i for i in cat_data if i.get("category") == category]
     if not e:
          return{"msg": "Det finns inga category med dem uppgifter"}, 404
     return (e), 200

@app.route("/tasks/categories", methods = ["GET"])
def all_categories():
    with open("tasks1.json", "r") as file:
        em_data = json.load(file)
    return em_data
    

if __name__ == "__main__":
    app.run(debug=True)