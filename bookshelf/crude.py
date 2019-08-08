#This file is the crud methods for the events

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crude = Blueprint('crude', __name__)


@crude.route('/')
def eventslist():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    events, next_page_token = get_model().events_list(cursor=token)

    return render_template(
        "eventslist.html",
        events=events,
        next_page_token=next_page_token)


    



@crude.route('/<id>')
def viewevents(id):
    event = get_model().readevent(id)
    return render_template("eventsview.html", event=event)


# [START add]
@crude.route('/add', methods=['GET', 'POST'])
def addevents():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        event = get_model().createevent(data)

        return redirect(url_for('.viewevents', id=event['id']))

    return render_template("eventsform.html", action="Add", event={})
# [END add]


@crude.route('/<id>/edit', methods=['GET', 'POST'])
def editevents(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crude.route('/<id>/delete')
def deleteevents(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
