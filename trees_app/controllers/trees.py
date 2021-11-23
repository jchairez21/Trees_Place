from flask import render_template, redirect, session, request, flash
from trees_app import app
from trees_app.models.user import User
from trees_app.models.tree import Tree


@app.route('/dashboard')
def dashboard():
    user = User.get_one({'id': session['logged_user']})
    all_trees = Tree.get_all()
    return render_template('dashboard.html', user=user, all_trees=all_trees)

# (1^) - Starting From Scratch!


@app.route('/trees/add')
def add_trees():
    user = User.get_one({'id': session['logged_user']})
    return render_template('add_trees.html', user=user)


@app.route('/create/trees', methods=['POST'])
def create_trees():
    if not Tree.validate_tree(request.form):
        return redirect('/trees/add')

    data = {
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date': request.form['date'],
        'user_id': session['logged_user']
    }
    Tree.save(data)
    # ^Tree object!
    return redirect('/dashboard')
# (2^) Adding


@app.route('/show/trees/<id>')
def show_trees(id):
    data = {
        'id': id
    }
    user = User.get_one({'id': session['logged_user']})
    tree_details = Tree.get_one(data)
    return render_template('view_tree_details.html', user=user, tree_details=tree_details)
# (3^)


@app.route('/my/trees')
# No id just going to this page!
def my_trees():
    logged_in_user = User.get_one({'id': session['logged_user']})
    all_my_trees = Tree.get_all()
    return render_template('my_trees.html', all_my_trees=all_my_trees, user=logged_in_user)
# (4^)


@app.route('/tree/delete/<id>')
def delete_trees(id):
    Tree.delete({'id': id})
    return redirect('/my/trees')
# (5^)


@app.route('/tree/edit/<id>')
def edit(id):
    logged_in_user = User.get_one({'id': session['logged_user']})
    this_tree = Tree.get_one({'id': id})
    return render_template('edit_tree.html', one_tree=this_tree, user=logged_in_user)


@app.route('/trees/update/<id>', methods=['POST'])
def update_trees(id):
    if not Tree.validate_tree(request.form):
        return redirect(f'/tree/edit/{id}')
    # (^^^       This is for VALIDATION!     ^^^)

    data = {
        'id': id,
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date': request.form['date']
        # Don't NEED user_id:session['logged_user']
    }
    Tree.update(data)
    return redirect('/my/trees')


# (6^)
