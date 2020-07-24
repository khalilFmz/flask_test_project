from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
import json

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':'library',
    'host':'localhost',
    'port':27017
}

db = MongoEngine()
db.init_app(app)

class Book(db.Document):
    id = db.IntField(required = True, min_value = 0)
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

@app.route('/', methods = ['PUT'])
def add_book(**kwargs):
    record = json.loads(request.data)
    book = Book(id = request['id'],
                title = request['title'],
                author = request['author'],
                first_sentence = request['first_sentence'],
                published = request['request'])
    #book = Book(**kwargs)
    book.save()
    return jsonify(book.to_json)

@app.route('/', methods = ['GET'])
def get_book():
    book_id = request.args.get('id')
    book = Book.objects.get(id = book_id).first()
    if not book:
        return jsonify({'error': 'No book with that id'})
    else:
        return jsonify(book.to_json)

    
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

if __name__ == '__main__':
    app.run(debug = True, port = 8000)