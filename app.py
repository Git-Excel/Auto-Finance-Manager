from flask import Flask

# Create the Flask app
app = Flask(__name__)

# Set up a basic route
@app.route("/")
def home():
    return "Welcome to Auto Finance Manager!"

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
