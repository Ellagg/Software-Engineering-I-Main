from flask import Flask, render_template


app = Flask(__name__)

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
    return render_template("viewAll.html")

@app.route("/search", methods = ["GET"])
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(port = 2000, debug = True)
