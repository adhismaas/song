from scipy import spatial
from os import listdir
from flask import request, jsonify
import os
import pandas as pd
import numpy as np
import flask
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Recommendation API</h1>
<p>Hi there!</p>'''


@app.route('/api/v1/resources/recommend/', methods=['POST'])
def api_recommend():
	ekspresi = request.get_json()
	if ekspresi is None:
		return jsonify("Error : No expression is passed [ERR_NO_EXPRESSION]")

	else:
		ekspresi = ekspresi['data']

	ekspresi = [10-x for x in ekspresi]
	print(ekspresi)
	lagu = listdir('data_train/')
	lagu = sorted(lagu, key=lambda x: float(x.split()[0]))
	
	
	recommend = []
	data = pd.read_csv("musicData.csv")
	data = data.fillna(0)
	
	dataCentro = data.groupby(['Id']).mean()
	dataDeviation = data.groupby(['Id']).std().mul(0.1)

	dataDeviation = dataDeviation.std(axis=1)
	
	dataCentro = dataCentro.values.tolist()
	dataDeviation = dataDeviation.values.tolist()

	for i in range(len(dataCentro)):
		temp = spatial.distance.cosine(ekspresi, dataCentro[i])
		if temp < dataDeviation[i] :
			recommend.append([i+1,temp,lagu[i]])

	recommend = sorted(recommend, key=lambda x: x[1])
	
	# return jsonify(200)
	return jsonify(recommend)



# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)

app.run()