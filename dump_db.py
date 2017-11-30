import psycopg2
import psycopg2.extras
import json
import datetime

conn = psycopg2.connect("dbname=wiki_development user=postgres password=root110120")

cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cursor.execute('select id, title, raw_content, namespace, verified, created_at, updated_at from pages')

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

pages = cursor.fetchall()

for page in pages:
    if page['verified'] is None:
        page['verified'] = True

cursor.execute('select * from page_changes')
changes = cursor.fetchall()

cursor.execute('select * from users')
users = cursor.fetchall()

cursor.execute('select * from repo_links')
repo_links = cursor.fetchall()

cursor.execute('select * from page_verifications')
verifications = cursor.fetchall()

cursor.execute('select * from pages_users')
page_users = cursor.fetchall()

cursor.execute('select * from triples')
triples = cursor.fetchall()

with open('db.json', 'w') as f:
    json.dump({
        'pages': pages,
        'page_changes': changes,
        'users': users,
        'repo_links': repo_links,
        'page_verifications': verifications,
        'page_users': page_users,
        'triples': triples
    }, f, default=datetime_handler, indent=4)
