from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crudu = Blueprint('crudu', __name__)


# [START list]
@crudu.route("/")
def userslist():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    users, next_page_token = get_model().users_list(cursor=token)

    return render_template("userslist.html", users=users,next_page_token=next_page_token)
# [END list]



@crudu.route('/<id>')
def viewuser(id):
    user = get_model().readuser(id)
    return render_template("usersview.html", user=user)


# [START add]
@crudu.route('/add', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = get_model().createuser(data)

        return redirect(url_for('.viewuser', id=user['id']))

    return render_template("usersform.html", action="Add", user={})
# [END add]


@crudu.route('/<id>/edit', methods=['GET', 'POST'])
def edituser(id):
    user = get_model().readuser(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = get_model().update(data, id)

        return redirect(url_for('.viewuser', id=user['id']))

    return render_template("usersform.html", action="Edit", user=user)


@crudu.route('/<id>/delete')
def deleteuser(id):
    get_model().deleteuser(id)
    return redirect(url_for('.userslist'))
