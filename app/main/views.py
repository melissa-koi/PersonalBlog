from flask import render_template, redirect, url_for, flash, request, abort
from . import main
from flask_login import login_required, current_user
from .forms import PostForm, CommentForm, UpdateProfile
from ..models import Post, User, Comment
from .. import db, photos
from ..requests import get_quotes

@main.route('/')
def index():
    title = 'Home - Welcome to The Blogging Website'
    quote = get_quotes()
    posts_display = Post.query.all()
    return render_template('index.html', title=title, posts_display=posts_display, quote=quote)

@main.route('/forms/blog', methods=['GET', 'POST'])
@login_required
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
        post.author = form.author.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author
    return render_template('blog_form.html', form=form)

@main.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))

@main.route('/pitch/comments', methods = ['GET', 'POST'])
@login_required
def comments():
   form = CommentForm()
   comments = Comment.query.all()
   if form.validate_on_submit():
       comment = form.comment.data
       new_comment = Comment(comment = comment)
       new_comment.save()
       return redirect(url_for('main.comments'))

   return render_template('comment.html', form=form, comments=comments)

@main.route("/comment/<int:comment_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_comm(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('main.comments'))

@main.route('/user/<uname>')
@login_required
def profile(uname):
    uname = current_user.username
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template('profile/profile.html', user=user)

@main.route('/user/<uname>/update_profile', methods=['POST', 'GET'])
@login_required
def update_profile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/update.html', form=form, uname=uname)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))