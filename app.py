from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':'library',
    'host':'localhost',
    'port':27017
}

db = MongoEngine()
db.init_app(app)

class Book(db.Document):
    book_id = db.IntField(required = True, min_value = 0)
    title = db.StringField(required = True)
    author = db.StringField(required = True)
    first_sentence = db.StringField()
    published = db.BooleanField()
    def to_json(self):
        return {'id': self.id,
                'title': self.title,
                'author': self.author,
                'first_sequence': self.first_sentence,
                'published': self.published}

@app.route('/add', methods = ['POST'])
def add_book():
    print('executing POST request')
    #record = json.loads(request.data)
    record = request.data
    record = json.loads(record)

    book = Book(book_id = record['book_id'],
                title = record['title'],
                author = record['author'],
                first_sentence = record['first_sentence'],
                published = record['published'])
    book.save()
    return jsonify(book)

@app.route('/get', methods = ['GET'])
def get_book():
    book_id = request.args.get('book_id')
    print('THE ID YOU WERE LOOKING FOR {}'.format(book_id))
    try:
        book = Book.objects.get(book_id = book_id)
        return jsonify(book)
    except:
        return jsonify({'error': 'No book with that id'})

"""  
@app.route('/')
def hello_finamaze():
    return 'hello  !'

@app.route('/books/all')
def api_all():
    return jsonify(books)


@app.route('/books')
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error : give me an id stupid"
    rslt = list()
    for book in books:
        if book['id'] == id:
            rslt.append(book)

    return jsonify(rslt)
"""
if __name__ == '__main__':
    app.run(debug = True)