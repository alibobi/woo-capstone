from flask import Flask, render_template

# Create a Flask application
app = Flask(__name__)

# Define a route and a function to handle requests to that route
@app.route('/')
def hello():
    return 'Hello, World!'

# Define a route and a function to handle requests to that route
@app.route('/test')
def test():
    return render_template('home.html')

def build_db() -> None:
    db.drop_all()
    db.create_all()

def run():
	app.run(debug=True, port=9999)



