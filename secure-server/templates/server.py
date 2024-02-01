from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route and a function to handle requests to that route
@app.route('/')
def hello():
    return 'Hello, World!'

def build_db() -> None:
    db.drop_all()
    db.create_all()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

