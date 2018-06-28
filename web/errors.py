# -*- coding: utf-8 -*-
from web import web, db
from flask import render_template
from .resources import Resources as Res


@web.errorhandler(404)
def not_found_error(error):
    return render_template("404.html", title=Res.TITLE, page_action=Res.ERR_404), 404


@web.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template("500.html", title=Res.TITLE, page_action=Res.ERR_500), 500
