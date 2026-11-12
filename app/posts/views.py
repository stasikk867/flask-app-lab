from datetime import datetime

from flask import (
    flash,
    redirect,
    render_template,
    url_for
)

from app.extensions import db
from app.posts import posts_bp
from app.posts.forms import PostForm, DeletePostForm
from app.posts.models import Post


@posts_bp.route("/", methods=["GET"])
def all_posts():
    posts = db.session.scalars(
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    ).all()

    return render_template("posts.html", posts=posts)


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            category=form.category.data,
            is_active=form.enabled.data,
            author="Anonymous"
        )

        db.session.add(post)
        db.session.commit()

        flash("Post successfully created.", "success")
        return redirect(url_for("posts.all_posts"))

    if not form.is_submitted():
        form.publish_date.data = datetime.now().replace(
            second=0, microsecond=0
        )

    return render_template(
        "add_post.html", form=form, title="Create post"
    )


@posts_bp.route("/<int:id>", methods=["GET"])
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        post.is_active = form.enabled.data

        db.session.commit()

        flash("Post successfully updated.", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    if not form.is_submitted():
        form.title.data = post.title
        form.content.data = post.content
        form.publish_date.data = post.posted
        form.category.data = post.category
        form.enabled.data = post.is_active

    return render_template(
        "add_post.html", form=form, title="Update post"
    )


@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    form = DeletePostForm()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

        flash("Post successfully deleted.", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "delete_confirm.html", post=post, form=form
    )
