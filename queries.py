from sqlalchemy import *

DB_URL = "sqlite:///websites.db"


def connect_db():
    return create_engine(url=DB_URL, echo=False).connect()


def insert_html(url, html):
    conn = connect_db()
    conn.execute(text("UPDATE websites SET html = :html WHERE url = :url"),
                 {"url": url, "html": html})


def get_all_urls():
    conn = connect_db()
    return [i[0] for i in conn.execute(text("SELECT url FROM websites")).all()]


def get_previous_html(url):
    conn = connect_db()

    id = conn.execute(text("SELECT websiteID FROM websites WHERE url = :url"),
                      {"url": url}).fetchone()[0]

    prev_html = conn.execute(text("SELECT html FROM websites WHERE websiteID = :id"),
                             {"id": id}).fetchone()

    # TODO: except -> no url found
    return prev_html[0]

def delete_all():
    conn = connect_db()

    conn.execute(text("DELETE FROM websites"))