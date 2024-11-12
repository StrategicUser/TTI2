from bottle import get, run, template

animals = [{'name' : 'Ellie', 'Type' : 'Elephant'},
			{'name': 'Python', 'Type' : 'Snake'}]

@get('/animals')
def getAll():
	return {'animals' : animals}

@get('/animal/<name>')
def getOne(name):
	the_animal = [animal for animal in animals if animal['name'] == name]
	return {'animal' : the_animal[0]}

if __name__ == '__main__':
	run(debug=True, reloader=True)

