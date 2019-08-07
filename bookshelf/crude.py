

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crude = Blueprint('crude', __name__)


# [START list]
# @crude.route("/")
# def list():
#     token = request.args.get('page_token', None)
#     if token:
#         token = token.encode('utf-8')

#     books, next_page_token = get_model().list(cursor=token)

#     return render_template(
#         "list.html",
#         books=books,
#         next_page_token=next_page_token)
# [END list]

@crude.route('/events')
def events():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events, next_page_token = get_model().list(cursor=token)

    return "Hello World"


    render_template(
        "events.html",
        events=events,
        next_page_token=next_page_token)


@crude.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crude.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crude.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crude.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
