from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/Jrgrz/Desktop/Python/Kodilla_learning/Kodilla_13/Kodilla_13_4/LIBRARY fin/library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#Initialize the database
db = SQLAlchemy(app)

#Create db model
class Library(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(200), nullable=False)
      year = db.Column(db.String(4), nullable=False)
      description = db.Column(db.String(500))
      author = db.Column(db.String(200), nullable=False)
      borrowed = db.Column(db.Boolean)
      date_created = db.Column(db.DateTime, default=datetime.utcnow)

      def __repr__(self):
            return '<Title %r>' % self.id


@app.route("/libraries/", methods=['GET', 'POST'])
def library_20():
    if request.method == "POST":
        new_title = request.form['title']
        new_year = request.form['year']
        new_description = request.form['description']
        new_author = request.form['author']
        new_borrowed = request.form.get("borrowed", False) == "True"
        new_book = Library(title=new_title, year=new_year, description=new_description, author=new_author,
                           borrowed=new_borrowed)
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/libraries/')
        except:
            return 'ERROR'
    else:
        libraries = Library.query.order_by(Library.date_created).all()
        return render_template("library.html", libraries=libraries)

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    library_to_update = Library.query.get_or_404(id)
    if request.method == "POST":
        library_to_update.title = request.form['title']
        library_to_update.year = request.form['year']
        library_to_update.description = request.form['description']
        library_to_update.author = request.form['author']
        library_to_update.borrowed = request.form.get("borrowed", False) == "True"
        try:
            db.session.commit()
            return redirect('/libraries/')
        except:
            return "ERROR"
    else:
        return render_template("update.html", library_to_update=library_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    library_to_delete = Library.query.get_or_404(id)

    try:
        db.session.delete(library_to_delete)
        db.session.commit()
        return redirect('/libraries/')
    except:
        return "ERROR"


if __name__ == "__main__":
    with app.app_context():
        # Create the database tables
            db.create_all()
    app.run(debug=True)
