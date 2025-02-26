from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

CONNECTION_STRING = 
# MongoDB connection
client = MongoClient(CONNECTION_STRING)
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

@app.route("/search", methods = ["GET"])
def search():
    return render_template("search.html")

@app.route("/viewAll", methods = ["GET"])
def viewAll():
    players = list(collection.find({}, {"_id": 0}))  # Fetch all players
    return render_template("viewAll.html", players=players)
    #return render_template("viewAll.html")

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

    collection.insert_one(new_player)

    return redirect(url_for('addPlayer'))

# Get every player in the database and display them all
@app.route('/viewAll')
def show_players():
    players = list(collection.find({}, {"_id": 0})) 
    return render_template('viewAll.html', players=players)

@app.route('/search', methods=['POST'])
def search_player():
    name = request.form.get("name")  # Get the name from the form

    # Search for the player in MongoDB (case-insensitive search)
    player = collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}}, {"_id": 0})

    if player:
        return render_template('search.html', player=player)
    else:
        return render_template('search.html', message="Player not found.")

@app.route('/positionSort', methods=['GET', 'POST'])
def search_by_position():
    if request.method == 'POST':
        position = request.form.get("position")

        players = list(collection.find({"position": position}, {"_id": 0})) 
        if players:
            return render_template('positionSort.html', players=players, position=position)
        else:
            return render_template('positionSort.html', message="No players found in position: {position}")
    
    return render_template('search_position.html')

if __name__ == "__main__":
    app.run(port = 2000, debug = True)
    
