# -*- coding: utf-8 -*-
from web import web, db, text
from flask import render_template
from .resources import Resources as Res


@web.errorhandler(404)
def not_found_error(error):
    text.currentaction = Res.ERR_404
    return render_template("404.html", text=text), 404


@web.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    text.currentaction = Res.ERR_500
    return render_template("500.html", text=text), 500
