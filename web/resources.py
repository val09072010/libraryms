# -*- coding: utf-8 -*-
class Resources:
    TITLE = u'LMS'
    SEARCH_ACTION = u'Search'
    SIGNIN_ACTION = u'Sign In'
    ADD_BOOK_ACTION = u'Add book'
    EDIT_BOOK_ACTION = u'Edit book'
    ADD_AUTHOR_ACTION = u'Add author'
    RESULT_ACTION = u'Search results'
    DEL_BOOK_ACTION = u'Delete book'

    FLASH_ADD_BOOK = u'Book "{0}" ({1}), author(s) #{2} added successfully'
    FLASH_DEL_BOOK = u'Book "{0}" ({1}) deleted successfully. Please note! Authors remain is system.'
    FLASH_EDIT_BOOK = u'Book "{0}" ({1}), author(s) #{2} updated successfully'
    FLASH_ADD_AUTHOR = u'Author {0}: {1} {2} added successfully'

    LOGIN_ERROR = u'Invalid username or password'
    ADD_AUTHOR_ERROR = u'Added author already exists!'
    NOTHING_FOUND = u'Sorry, we have found nothing for the search query, please try another one.'
    ERR_404 = u'Oops! Page not found. While we are looking for it please enjoy our ascii graphic!'
    ERR_500 = u'Ouch! Seems something serious has happened'
    ERROR_USER_INPUT_FORBID_CHARS = u'User input contains forbidden or suspicious characters!'

    FORM_SEARCH_BY_TITLE = u'Search by Book title'
    FORM_SEARCH_BY_AUTHOR = u'Search by Author'

    FORM_ADD_EDIT_BOOK_TITLE = u'Book title'
    FORM_ADD_EDIT_BOOK_GENRE = u'Genre'
    FORM_ADD_EDIT_BOOK_AUTHORS = u'Select authors'
    FORM_ADD_EDIT_BOOK_SUBMIT = u'Save changes'

    FORM_ADD_AUTHOR_FNAME = u'First name'
    FORM_ADD_AUTHOR_LNAME = u'Last name'

    FORM_LOGIN_LOGIN = u'Login or email'
    FORM_LOGIN_PASS = u'Password'

    FORM_DEL_CONFIRM = u'I confirm'
    FORM_DEL_ASK = u'Please confirm that you want to delete the book:'
