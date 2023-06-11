from flask import Flask, request, render_template, redirect, url_for, jsonify
from forms import LibraryForm
from models import libraries

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/libraries/", methods=['GET', 'POST'])
def library_list():
        form = LibraryForm()
        error = ""
        if request.method == "POST":
            if form.validate_on_submit():
                libraries.create(form.data)
                libraries.save_all()
            return redirect(url_for("library_list"))
        return render_template ("index.html", form=form, libraries=libraries.all(), error=error)


@app.route("/libraries/<int:library_id>/", methods=["GET", "POST"])
def library_details(library_id):
        library = libraries.get(library_id)
        form = LibraryForm(data=library)

        if request.method == "POST":
            if form.validate_on_submit():
                libraries.update(library_id, form.data)
                return redirect(url_for("library_details", library_id=library_id))
        return render_template ("index.html", form=form, library_id=library_id)


    ### REST ###


@app.route("/api/v1/libraries/", methods=["GET"])
def libraries_list_api_v1():
        return jsonify(libraries.all())

@app.route("/api/v1/libraries/<int:library_id>/", methods=["GET"])
def library_details_api_v1(library_id):
        library = libraries.get(library_id)
        if library:
            return jsonify(library)
        else:
            return jsonify(error="Library not found"), 404

@app.route("/api/v1/libraries/", methods=["POST"])
def create_library_api_v1():
        data = request.json
        libraries.create(data)
        libraries.save_all()
        return jsonify(success=True)

@app.route("/api/v1/libraries/<int:library_id>/", methods=["PUT"])
def update_library_api_v1(library_id):
        library = libraries.get(library_id)
        if library:
            data = request.json
            libraries.update(library_id, data)
            return jsonify(success=True)
        else:
            return jsonify(error="Library not found"), 404

@app.route("/api/v1/libraries/<int:library_id>/", methods=["DELETE"])
def delete_library_api_v1(library_id):
        library = libraries.get(library_id)
        if library:
            libraries.delete(library_id)
            return jsonify(success=True)
        else:
            return jsonify(error="Library not found"), 404



if __name__ == "__main__":
    app.run(debug=True)
