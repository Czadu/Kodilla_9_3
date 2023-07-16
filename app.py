from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/Jrgrz/Desktop/Python/Kodilla_learning/Kodilla_13/Kodilla_13_4/LIBRARY fin/library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<Author %r>' % self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    description = db.Column(db.String(500))
    borrowed = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id')) # corrected line

    def __repr__(self):
        return '<Title %r>' % self.id


@app.route("/libraries/", methods=['GET', 'POST'])
def library_20():
    if request.method == "POST":
        new_title = request.form['title']
        new_year = request.form['year']
        new_description = request.form['description']
        author_name = request.form['author']
        new_borrowed = request.form.get("borrowed", False) == "True"

        # Check if the author already exists
        author = Author.query.filter_by(name=author_name).first()

        # If the author does not exist, create a new author
        if author is None:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()

        # Now create the new book with the author
        new_book = Book(title=new_title, year=new_year, description=new_description, 
                           borrowed=new_borrowed, author_id=author.id)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/libraries/')
        except:
            return 'ERROR'
    else:
        libraries = Book.query.order_by(Book.date_created).all()
        return render_template("library.html", libraries=libraries)


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    book_to_update = Book.query.get_or_404(id)
    if request.method == "POST":
        book_to_update.title = request.form['title']
        book_to_update.year = request.form['year']
        book_to_update.description = request.form['description']
        author_name = request.form['author']
        author = Author.query.filter_by(name=author_name).first()
        if author is None:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        book_to_update.author_id = author.id
        book_to_update.borrowed = request.form.get("borrowed", False) == "True"
        try:
            db.session.commit()
            return redirect('/libraries/')
        except:
            return "ERROR"
    else:
        return render_template("update.html", book_to_update=book_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Book.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/libraries/')
    except:
        return "ERROR"



if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
            db.create_all()
    app.run(debug=True)
