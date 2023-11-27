from flask import Flask,render_template,request,url_for,redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app=Flask(__name__)
mongo_url="mongodb://localhost:27017"
mongo_var=MongoClient(mongo_url)
db=mongo_var.employee_details
collection=db.employee

@app.route('/')
def home():
    data_url=collection.find({})
    return render_template("home.html",datum=data_url)

@app.route('/find')
def find():
    data_url=collection.find({"Name":"Gloria"})
    return render_template("home.html",datum=data_url)

@app.route('/insert',methods=["POST","GET"])
def insert():
    if request.method=="POST":
        Name=request.form.get("Name")
        Age=request.form.get("Age")
        Gender=request.form.get("Gender")
        dict1={}
        dict1.update({"Name":Name})
        dict1.update({"Age":Age})
        dict1.update({"Gender":Gender})
        collection.insert_one(dict1)
    data_url=collection.find({})
    return render_template("home.html",datum=data_url)

@app.route('/edit/<string:id>',methods=["POST","GET"])
def edit(id):
    if request.method=="POST":
        Name=request.form.get("Name")
        Age=request.form.get("Age")
        Gender=request.form.get("Gender")    
        collection.update_one({"_id":ObjectId(id)},{"$set":{"Name":Name,"Age":Age,"Gender":Gender}})
        return redirect(url_for("home"))
    return render_template("edit.html")

@app.route('/delete/<string:id>',methods=["POST","GET"])
def delete(id):    
    collection.delete_one({"_id":ObjectId(id)})
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)