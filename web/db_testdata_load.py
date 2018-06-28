# -*- coding: utf-8 -*-
from web import db


db.create_all()
with open("..\\scripts\\initdb.sql", encoding="utf-8") as f:
    sql_queries = f.readlines()
    for sql_query in sql_queries:
        db.engine.execute(sql_query)