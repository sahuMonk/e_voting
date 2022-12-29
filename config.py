import os


class Config(object):
    DEBUG = True
    SECRET_KEY = 'BadSecretKey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///votrbase.db'