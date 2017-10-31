#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import psycopg2


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} no found in the {1} file'.format(section, filename))

    return db


def create_tables():
    """Create necessary table"""

    commands = (
        """
        CREATE TABLE items (
            id SERIAL PRIMARY KEY,
            item VARCHAR(255) NOT NULL,
            count INTEGER NOT NULL,
            price NUMERIC NOT NULL
        )
        """,
    )

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def connect():
    """Connect to DB"""
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # TODO: implement singleton design pattern for database connection
    create_tables()
    connect()
