@echo off

C:\server\Python3\Scripts\flask.exe db init
C:\server\Python3\Scripts\flask.exe db migrate
C:\server\Python3\python.exe web\db_testdata_load.py