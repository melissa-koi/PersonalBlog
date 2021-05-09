from flask import render_template, redirect, url_for, flash, request, abort
from . import main
# from flask_login import login_required, current_user
from .forms import ReviewForm
# from ..models import Post, User, Comment, Upvote, Downvote
# from .. import db, photos
import markdown2

@main.route('/')
def index():
    title = 'Home - Welcome to The Blogging Website'
    return render_template('index.html', title=title)

@main.route('/review/')
def single_review(id):
    revForm = ReviewForm()
    review=Review.query.get(id)
    if review is None:
        abort(404)
    format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('add_blog.html',review = review,format_review=format_review)