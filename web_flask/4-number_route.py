#!/usr/bin/python3
""" Starts a flask web app with four routes """

from flask import Flask


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
	return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
	return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
	""" replaces text with a variable """
	text = text.replace('_', ' ')
	return 'C {}'.format(text)

@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def py_text(text = "is cool"):
	""" replaces text with a variable with a default """
	text = text.replace('_', ' ')
	return "Python {}".format(text)

@app.route('/number/<int:n>')
def number_text(n):
	""" replace n with an int only if n is an int """
	n = str(n)
	return '{} is a number'.format(n)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
