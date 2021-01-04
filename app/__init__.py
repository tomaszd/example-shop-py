import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cors = CORS()


def create_app(options={}):
    if 'TESTING' in options and options['TESTING']:
        config_name = 'app.config.TestingConfig'
    else:
        config_name = os.getenv(
            'APP_SETTINGS',
            'app.config.DevelopmentConfig'
        )
    app = Flask(__name__)
    app.config.from_object(config_name)
    add_debug_page(app)
    init_extensions(app)
    register_blueprints(app)

    return app


def init_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)


def register_blueprints(app):
    from app.restapi import api
    app.register_blueprint(api, url_prefix='/api')


def add_debug_page(app):
    @app.route('/')
    def index():
        content = """Endpoints:</br>             
         <a href="/api/categories">/api/categories</a></br>
         <a href="/api/countries">/api/countries</a></br>
         <a href="/api/customers">/api/customers</a></br>
         <a href="/api/products">/api/products</a></br>
         <a href="/api/orders">/api/orders</a></br>
         Statistics:</br>
         <a href="/api/statistics/sells_by_product">/api/statistics/sells_by_product</a></br>
         <a href="/api/statistics/products_by_category">/api/statistics/products_by_category</a></br>
         <a href="/api/statistics/sells_by_product">/api/statistics/sells_by_product</a></br>
         <a href="/api/statistics/units_delivered_by_product_by_country">/api/statistics/units_delivered_by_product_by_country</a></br>
         """
        return content
