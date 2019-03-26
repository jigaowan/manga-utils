import os
import sqlite3
from shutil import copyfile

select_sql = """
SELECT series.name,books.title,books.series_index,books.author_sort,books.path,data.name FROM
(SELECT id,title,series_index,author_sort,path FROM books)books
LEFT JOIN
(SELECT book,series FROM books_series_link)books_series_link
ON books.id = books_series_link.book
LEFT JOIN
(SELECT id,name FROM series)series
ON books_series_link.series = series.id
LEFT JOIN
(SELECT book,format,name FROM data WHERE format = 'CBZ')data
ON books.id = data.book
ORDER BY books.author_sort,series.name,books.series_index
"""

db_file = 'metadata.db'
old_path = '/volume1/share/books'
new_path = '/volume1/share/comic'

if not os.path.exists(new_path):
    os.mkdir(new_path)

with sqlite3.connect(os.path.join(old_path, db_file)) as db:
    books = db.execute(select_sql).fetchall()
for book in books:
    series = book[0]
    title = book[1]
    author = book[3]
    path = book[4]
    file_name = book[5]
    book_old = os.path.join(old_path, path, file_name + '.cbz')
    author_path = os.path.join(new_path, author)
    if not os.path.exists(author_path):
        os.mkdir(author_path)
    if not series:
        series = title
    series_path = os.path.join(author_path, series)
    if not os.path.exists(series_path):
        os.mkdir(series_path)
    book_new = os.path.join(series_path, title + '.cbz')
    if os.path.exists(book_new) and os.path.isfile(book_new) and (
            os.path.getsize(book_old) == os.path.getsize(book_new)):
        continue
    copyfile(book_old, book_new)
