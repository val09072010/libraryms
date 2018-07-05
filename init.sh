#!/usr/bin/env bash

flask db init
flask db migrate
web/db_testdata_load.py