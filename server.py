from flask import Flask, render_template, request, jsonify
import scripts.webcrawler

app = Flask(__name__)

@app.route('/')
def render():
    return render_template('myfile.html')

@app.route('/suggestions')
def getSuggestions():
	print request.method
	if request.method == 'GET':
		return "No input file specified"
	else:
		return render_template('myfile.html')

@app.route('/suggestions/movies')
def getMovies():
	return jsonify({'data':'Movie Data'})


if __name__=='__main__':
    app.run(debug=True, port=3134)