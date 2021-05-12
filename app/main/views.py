from flask import render_template, redirect, url_for, flash, request, abort
from . import main
from flask_login import login_required, current_user
from .forms import PostForm, CommentForm, UpdateProfile
from ..models import Post, User
from .. import db, photos


@main.route('/')
def index():
    title = 'Home - Welcome to The Blogging Website'
    posts_display = Post.query.all()
    return render_template('index.html', title=title, posts_display=posts_display)

@main.route('/forms/blog', methods=['GET', 'POST'])
def blogform():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author = form.author.data
        user_id = current_user._get_current_object().id
        post_obj = Post(title=title, content=content, author = author,user_id = user_id)
        post_obj.save_post()
        return redirect(url_for('main.index'))
    return render_template('blog_form.html', form=form)

@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('blog_form.html', form=form)

