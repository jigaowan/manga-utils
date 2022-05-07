import os
import sys
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

if len(sys.argv) not in (1, 3):
    raise ValueError('wrong args number')

if len(sys.argv) == 3:
    old_path = sys.argv[1]
    new_path = sys.argv[2]

if not os.path.isdir(old_path):
    raise ValueError('source is not dir')

if not os.path.exists(os.path.join(old_path, db_file)):
    raise ValueError('source is not calibre dir')

print(f'source dir is {old_path}')
print(f'output dir is {new_path}')

if not os.path.exists(new_path):
    print(f'not found output dir')
    os.mkdir(new_path)
    print(f'create output dir success')

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
        print(f'not found author path {author}')
        os.mkdir(author_path)
        print(f'create author path {author} success')
    if not series:
        series = title
    series_path = os.path.join(author_path, series)
    if not os.path.exists(series_path):
        print(f'not found series path {series}')
        os.mkdir(series_path)
        print(f'create series path {series} success')
    book_new = os.path.join(series_path, title + '.cbz')
    if os.path.exists(book_new) and os.path.isfile(book_new) and (
            os.path.getsize(book_old) == os.path.getsize(book_new)):
        print(f'manga {title} is exist')
        continue
    print(f'not found manga {title}')
    copyfile(book_old, book_new)
    print(f'link manga {title} success')
print(f'link calibre mangas library to new dir finish')
