# Course: Advanced Database Systems (CRN-23223)
# Author: Bhavesh Asanabada (#700744873)
#
# -------------- PROGRAMMING ASSIGNMENT - 1 ----------------
# Implementing a server applications and performing CRUD operations of datasets.
# Tools Used :
#    1. MongoDB (local instance) (port: 27017)
#    2. Flask web framework
# ----------------------------------------------------------

# Import statements
from flask import Flask, Response, request
import json

# Import MongoDB connection client
from dataHandler.MongoConnect import mongo_connect

app = Flask(__name__)
# Initializing the mongo client, if successful 'db' would be the 'database'
db = mongo_connect()


@app.route('/')
def hello_world():  # put application's code here
    return str(db)


# GET-ALL: Method to get all the movies from a collection
@app.route("/api", methods=["GET"])
def get_hulu_data():
    try:
        data = list(db.hulu.find())  # Collection Name = hulu
        for record in data:
            record["_id"] = str(record["_id"])
        return Response(response=json.dumps(data), status=500, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "Cannot get the movie"}), status=500,
                        mimetype="application/json")


# GET-SPECIFIC: Method to get movie by title
@app.route("/api/<string:fname>", methods=["GET"])
def get_specific_data(fname):
    try:
        data = list(db.hulu.find({"title": fname}))
        for record in data:  # Collection Name = hulu
            record["_id"] = str(record["_id"])
        return Response(response=json.dumps(data), status=500, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "Cannot get the movie"}), status=500,
                        mimetype="application/json")


# CREATE: Add movie to collection
@app.route("/api", methods=["POST"])
def add_data():
    try:
        id = request.json['id']
        title = request.json['title']
        clips_count = request.json['clips_count']
        description = request.json['description']
        episodes_count = request.json['episodes_count']
        genres = request.json['genres']
        score = request.json['score']
        seasons_count = request.json['seasons_count']
        company = request.json['company']
        released_at = request.json['released_at']
        rating = request.json['rating']

        def_record = db.hulu.insert_one(
            {'id': id, 'title': title, 'clips_count': clips_count, 'description': description,
             'episodes_count': episodes_count, 'genres': genres, 'score': score, 'seasons_count': seasons_count,
             'company': company, 'released_at': released_at, 'rating': rating}
        )

        return Response(response=json.dumps({"message": "Movie Added Successfully", "id": f"{def_record.inserted_id}"}),
                        status=200,
                        mimetype="application/json"
                        )

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "Movie not added"}),
                        status=500,
                        mimetype="application/json"
                        )


# UPDATE: Change movie information
# Updating information based on title
@app.route("/api/<string:fname>", methods=['PATCH'])
def update_movie(fname):
    try:
        resp = db.hulu.update_one({"title": fname},
                                  {'$set': {
                                      'id': request.json['id'],
                                      'title': request.json['title'],
                                      'description': request.json['description'],
                                      'score': request.json['score'],
                                      'rating': request.json['rating']
                                  }})

        # Check for any modifications
        if resp.modified_count == 1:
            # For any modifications, update the record
            return Response(response=json.dumps({"message": "Movie updated"}),
                            status=200,
                            mimetype="application/json"
                            )
        else:
            # For no modifications
            return Response(response=json.dumps({"message": "Nothing updated"}),
                            status=200,
                            mimetype="application/json"
                            )

    # If movie title doesn't match
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "Movie not updated"}),
                        status=500,
                        mimetype="application/json"
                        )


# DELETE: Delete a movie from database
# Deleting movie by the title
@app.route("/api/<string:fname>", methods=['DELETE'])
def delete_movie(fname):
    try:
        resp = db.hulu.delete_one({"title": fname})
        if resp.deleted_count == 1:

            return Response(response=json.dumps({"message": "Movie deleted"}),
                            status=200,
                            mimetype="application/json"
                            )
        else:
            return Response(response=json.dumps({"message": "nothing to delete"}),
                            status=200,
                            mimetype="application/json"
                            )

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "Movie not deleted"}),
                        status=500,
                        mimetype="application/json"
                        )


if __name__ == '__main__':
    app.run(debug=True)
