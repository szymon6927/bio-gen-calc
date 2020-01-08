from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required

from app.blog.models import Article
from app.blog.models import Feed
from app.database import db
from app.userpanel.decorators import superuser_required
from app.userpanel.forms import ArticleForm
from app.userpanel.forms import FeedForm
from app.userpanel.services.blog_aggregator_service import BlogAggregatorService
from app.userpanel.views import userpanel


@userpanel.route('/blog-aggregator/feeds')
@login_required
@superuser_required
def feed_list_view():
    feed_list = Feed.query.all()

    return render_template('userpanel/blog_aggregator/feeds.html', feeds=feed_list)


@userpanel.route('/blog-aggregator/feed/<int:feed_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def feed_details_view(feed_id):
    feed = Feed.query.get_or_404(feed_id)

    form = FeedForm(obj=feed)

    if form.validate_on_submit():
        feed.name = form.name.data
        feed.url = form.url.data

        db.session.add(feed)
        db.session.commit()

        flash('You have successfully edited the feed.', 'success')

        return redirect(url_for('userpanel.feed_details_view', feed_id=feed_id))

    return render_template('userpanel/blog_aggregator/feed_details.html', form=form, feed=feed)


@userpanel.route('/blog-aggregator/feed/delete/<int:feed_id>')
@login_required
@superuser_required
def feed_delete_view(feed_id):
    feed = Feed.query.get_or_404(feed_id)

    db.session.delete(feed)
    db.session.commit()

    flash(f'You have successfully delete the feed - {feed.url}', 'success')

    return redirect(url_for('userpanel.feed_list_view'))


@userpanel.route('/blog-aggregator/feed/add', methods=['GET', 'POST'])
@login_required
@superuser_required
def feed_add_view():
    form = FeedForm()

    if form.validate_on_submit():
        feed = Feed()
        feed.name = form.name.data
        feed.url = form.url.data

        db.session.add(feed)
        db.session.commit()

        flash('You have successfully added the feed.', 'success')

        return redirect(url_for('userpanel.feed_list_view'))

    return render_template('userpanel/blog_aggregator/feed_add.html', form=form)


@userpanel.route('/blog-aggregator/article/<int:article_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def article_details_view(article_id):
    article = Article.query.get_or_404(article_id)

    form = ArticleForm(obj=article)

    if form.validate_on_submit():
        article.title = form.title.data
        article.link = form.link.data
        article.pub_date = form.pub_date.data
        article.desc = form.desc.data
        article.was_published = form.was_published.data

        db.session.commit()

        flash('You have successfully edited the article.', 'success')

        return redirect(url_for('userpanel.article_details_view', article_id=article_id))

    return render_template('userpanel/blog_aggregator/article_details.html', article=article, form=form)


@userpanel.route('/blog-aggregator/article/delete/<int:article_id>')
@login_required
@superuser_required
def article_delete_view(article_id):
    article = Article.query.get_or_404(article_id)

    db.session.delete(article)
    db.session.commit()

    flash(f'You have successfully delete the article - {article.title}.', 'success')

    return redirect(url_for('userpanel.articles_list_view'))


@userpanel.route('/blog-aggregator/articles')
@login_required
@superuser_required
def articles_list_view():
    articles = Article.query.order_by(Article.created_at).all()

    return render_template('userpanel/blog_aggregator/articles.html', articles=articles)


@userpanel.route('/blog-aggregator/article/add', methods=['GET', 'POST'])
@login_required
@superuser_required
def article_add_view():
    form = ArticleForm()

    if form.validate_on_submit():
        article = Article()

        article.title = form.title.data
        article.link = form.link.data
        article.pub_date = form.pub_date.data
        article.desc = form.desc.data
        article.was_published = form.was_published.data

        db.session.add(article)
        db.session.commit()

        flash(f'You have successfully added the article.', 'success')

        return redirect(url_for('userpanel.articles_list_view'))

    return render_template('userpanel/blog_aggregator/article_add.html', form=form)


@userpanel.route('/blog-aggregator/parse', methods=['GET', 'POST'])
@login_required
@superuser_required
def aggregator_run_view():
    BlogAggregatorService.aggregate()

    return redirect(url_for('userpanel.articles_list_view'))
