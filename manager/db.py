from flask import current_app, g
import mysql.connector as cnx
from mysql.connector import errorcode
import click

def get_db():
    if 'db' not in g:
        g.db = cnx.connect(**current_app.config['DATABASE'])
    
    try:
        g.db.database = "hoteldb"
    except cnx.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            g.db.cursor().execute("CREATE DATABASE hoteldb DEFAULT CHARACTER SET 'utf8'")
            g.db.close()

            return get_db()
        else:
            raise(err)

    g.db.autocommit = True

    return g.db.cursor()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.execute(f.read(), multi=True)


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initialized the database")


def insert_example_dataset():
    db = get_db()

    with current_app.open_resource("example.sql") as f:
        db.execute(f.read(), multi=True)


@click.command('ins-example')
def init_db_examples():
    insert_example_dataset()
    click.echo("Examples inserted")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_db_examples)
