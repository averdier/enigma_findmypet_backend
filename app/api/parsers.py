# coding: utf-8

from flask_restplus import reqparse


pet_parser = reqparse.RequestParser()
pet_parser.add_argument('key', help='Start key')
pet_parser.add_argument('limit', type=int, help='Items per page')