# -*- coding: utf-8 -*-
from web import web, db
from web.models import User, Book, BooksAuthors, Author


@web.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book':Book, 'BooksAuthors': BooksAuthors, 'Author': Author}
