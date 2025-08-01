from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Ghostlinkz is live!"

# Add your link cleaning routes here

if __name__ == "__main__":
    app.run()

