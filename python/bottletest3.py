from bottle import get, run, template

@route('/login')
def login():
	return '<h1>On the login page</h1>'

@route('/register')
def register():
	return '<h1>On the register page</h1>'

@route('/article/<id>')
def article(id):
	return '<h1>You are viewing artical ' + id + '</h1>'

if __name__ == '__main__':
	run(debug=True, reloader=True)

