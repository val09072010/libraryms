# -*- coding: utf-8 -*-
from web import web, db
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, session, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import SearchForm, AddEditBookForm, AddAuthorForm, LoginForm
from .models import Book, Author, User
from .resources import Resources as Res


@web.route('/')
@web.route('/index')
def index():
    return render_template("index.html", title=Res.TITLE)


@web.route('/results')
def results():
    current_books = []
    book_not_found_msg = Res.NOTHING_FOUND
    if 'books' in session:
        current_books = session['books']
    return render_template("results.html", books=current_books, title=Res.TITLE, page_action=Res.RESULT_ACTION,
                           msg=book_not_found_msg)


@web.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        title_to_search = form.search_title.data.strip()
        author_to_search = form.search_author.data.strip()
        if title_to_search:
            search_title = "%{0}%".format(title_to_search)
            raw_books = db.session.query(Book).filter(Book.title.ilike(search_title))
        elif author_to_search:
            search_author = "%{0}%".format(author_to_search)
            raw_books = db.session.query(Book).join(Book.authors).filter(Author.last_name.ilike(search_author))
        else:
            raw_books = Book.query.all()
        session['books'] = [b.to_dict for b in raw_books]
        return redirect(url_for("results"))
    return render_template("search.html", form=form, title=Res.TITLE, page_action=Res.SEARCH_ACTION)


@web.route('/edit_book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id).first_or_404()
    form = AddEditBookForm()
    form.authors.choices = list((str(i.id), i) for i in db.session.query(Author).all())
    if form.validate_on_submit():
        title = form.book_title.data.strip()
        genre = form.book_genre.data.strip()
        author_id = int(form.authors.data)
        book.title = title
        book.genre = genre
        book.authors = [db.session.query(Author).filter_by(id=author_id).first()]
        db.session.commit()
        flash(Res.FLASH_EDIT_BOOK.format(title, genre, author_id))
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.authors.default = str(book.authors[0].id)
        form.process()
        form.book_title.data = book.title
        form.book_genre.data = book.genre
    return render_template("add_edit_book.html", form=form, title=Res.TITLE, page_action=Res.EDIT_BOOK_ACTION)


@web.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddEditBookForm()
    form.authors.choices = list((str(i.id), i) for i in db.session.query(Author).all())
    if form.validate_on_submit():
        title = form.book_title.data.strip()
        genre = form.book_genre.data.strip()
        author_id = int(form.authors.data)
        flash(Res.FLASH_ADD_BOOK.format(title, genre, author_id))
        author = db.session.query(Author).filter_by(id=author_id).first()
        book = Book(title, genre, [author])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add_edit_book.html", form=form, title=Res.TITLE, page_action=Res.ADD_BOOK_ACTION)


@web.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AddAuthorForm()
    if form.validate_on_submit():
        last_name = form.last_name.data.strip()
        existing_authors = db.session.query(Author).filter_by(last_name=last_name).all()
        if existing_authors and len(existing_authors) > 0:
            form.errors['author'] = Res.ADD_AUTHOR_ERROR
        else:
            author = Author(form.first_name.data.strip(), last_name)
            db.session.add(author)
            db.session.commit()
            flash(Res.FLASH_ADD_AUTHOR.format(author.id, author.first_name, author.last_name))
            return redirect(url_for('index'))
    return render_template("add_author.html", form=form, title=Res.TITLE, page_action=Res.ADD_AUTHOR_ACTION)


@web.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(Res.LOGIN_ERROR)
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form, title=Res.TITLE, page_action=Res.SIGNIN_ACTION)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
