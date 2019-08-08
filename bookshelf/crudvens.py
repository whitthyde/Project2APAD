from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crudvens = Blueprint('crudvens', __name__)


# [START list]
@crudvens.route("/")
def venueslist():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    venues, next_page_token = get_model().venues_list(cursor=token)

    return render_template("venueslist.html", venues=venues,next_page_token=next_page_token)
# [END list]



@crudvens.route('/<id>')
def viewvenue(id):
    venue = get_model().readvenue(id)
    return render_template("venueview.html", venue=venue)


# [START add]
@crudvens.route('/add', methods=['GET', 'POST'])
def addvenue():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        venue = get_model().createvenue(data)

        return redirect(url_for('.viewvenue', id=venue['id']))

    return render_template("venueform.html", action="Add", venue={})
# [END add]


@crudvens.route('/<id>/edit', methods=['GET', 'POST'])
def editvenue(id):
    venue = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        venue = get_model().update(data, id)

        return redirect(url_for('.viewvenue', id=venue['id']))

    return render_template("venueform.html", action="Edit", venue=venue)


@crudvens.route('/<id>/delete')
def deletevenue(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
