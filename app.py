from flask import Flask, request, render_template, redirect, url_for
from forms import LibraryForm
from models import librarys

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/librarys", methods=['GET', 'POST'])
def library_list():
    form = LibraryForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            librarys.create(form.data)
            librarys.save_all()
        return redirect(url_for("library_list"))
    return render_template ("index.html", form=form, librarys=librarys.all(), error=error)


@app.route("/librarys/<int:library_id>/", methods=["GET", "POST"])
def library_details(library_id):
    library = librarys.get(library_id)
    form = LibraryForm(data=library)

    if request.method == "POST":
        if form.validate_on_submit():
            librarys.update(library_id, form.data)
        return redirect(url_for("library_list"))
    return render_template ("index.html", form=form, library_id=library_id)



if __name__ == "__main__":
    app.run(debug=True)
