from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://ellaggordon:Extinctfame007@players.rbqni.mongodb.net/")  # Change URL as needed
db = client["SoftwareEngineeringI"]  # Replace with your database name
collection = db["players"]  # Replace with your collection name

@app.route("/", methods = ["GET"])
def home():
    return render_template("index.html")

@app.route("/positionSort", methods = ["GET"])
def positionSort():
    return render_template("positionSort.html")

@app.route("/addPlayer", methods = ["GET"])
def addPlayer():
    return render_template("addPlayer.html")

@app.route("/viewAll", methods = ["GET"])
def viewAll():
    players = list(collection.find({}, {"_id": 0}))  # Fetch all players
    return render_template("viewAll.html", players=players)
    #return render_template("viewAll.html")

@app.route("/search", methods = ["GET"])
def search():
    return render_template("search.html")


# CRUD
# Add a Player
@app.route("/addPlayer", methods=["POST"])
def addnewplayer():
    data = request.json
    if not all(key in data for key in ["name", "age", "position", "goals_scored"]):
        return jsonify({"error":"Missing required fields"}), 400
    
    player_id = collection.insert_one(data).inserted_id
    return jsonify({"message": "Player added", "id": str(player_id)}), 201

# READ: Get all players
# @app.route("/players", methods=["GET"])
# def get_players():
#     players = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
#     return jsonify(players), 200

# READ: Get a player by name
@app.route("/players/<name>", methods=["GET"])
def get_player(name):
    player = collection.find_one({"name": name}, {"_id": 0})
    if not player:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(player), 200

# READ: Get all players by position
# @app.route("/players/position/<position>", methods=["GET"])
# def get_players_by_position(position):
#     players = list(collection.find({"position": position}, {"_id": 0}))
#     if not players:
#         return jsonify({"error": "No players found for this position"}), 404
#     return jsonify(players), 200

if __name__ == "__main__":
    app.run(port = 2000, debug = True)
    # app.run(debug=True)
