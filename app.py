from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import json
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
    return render_template("index.html")

@app.route("/positionSort", methods = ["GET"])
def positionSortDefault():
    return render_template("positionSort.html")

@app.route("/positionSort/<players_json>", methods = ["GET"])
def positionSort(players_json):
    players = json.loads(players_json)
    return render_template("positionSort.html", players=players)

@app.route("/addPlayer", methods = ["GET"])
def addPlayer():
    return render_template("addPlayer.html")

@app.route("/search", methods = ["GET"])
def searchDefault():
    return render_template("search.html")

@app.route("/search<players_json>", methods = ["GET"])
def search(players_json):
    players = json.loads(players_json)
    return render_template("search.html", players=players)

@app.route("/viewAll", methods = ["GET"])
def viewAll():
    response = requests.get("http://127.0.0.1:3000/display-all")
    players = response.json()
    # print(players)
    return render_template("viewAll.html", players=players)

# Add a player to database
@app.route("/addPlayer", methods=["POST"])
def add_player():
    name = request.form.get("name")
    age = int(request.form.get("age"))
    position = request.form.get("position")
    goals_scored = int(request.form.get("goals_scored"))


    new_player = {
        "name": name,
        "age": age,
        "position": position,
        "goals_scored": goals_scored
    }

    new_player_json = jsonify(new_player)
    temp = requests.post("http://127.0.0.1:4000/add-player", json = new_player)

    return redirect(url_for('addPlayer'))

@app.route('/search', methods=['POST'])
def search_player():
    name = request.form.get("name")  # Get the name from the form
    name = name.replace(" ", "+")

    response = requests.get("http://localhost:8080/players/namedplayers?name=" + name)
    players = response.json()
    players_json = json.dumps(players)

    if players:
        return redirect(url_for("search", players_json=players_json))
    else:
        return redirect(url_for('searchDefault'))

@app.route('/positionSort', methods=['POST'])
def search_by_position():

    position = request.form.get("position")

    response = requests.get("http://localhost:5000/sort-by-position?position=" + position)
    players = response.json()
    players_json = json.dumps(players)

    if players:
        return redirect(url_for("positionSort", players_json=players_json))
    else:
        return redirect(url_for('positionSortDefault'))

if __name__ == "__main__":
    app.run(port = 2000, debug = True)
    
