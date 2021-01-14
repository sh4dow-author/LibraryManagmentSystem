import sqlite3 as sq


class Database:
    def __init__(self, database_name):
        self.__database_name = database_name
        self._db = sq.connect('databases/library.db')
        self._cur = self._db.cursor()

    def AddBook(self, _title, _author, _genre, _publish_year):
        self._cur.execute(
            'INSERT INTO books (title, author, genre, publish_year) VALUES (?,?,?,?)',
            (_title, _author, _genre, _publish_year))
        self._db.commit()

    def DeleteBook(self, book_id):
        try:
            self._cur.execute(f'SELECT * FROM books WHERE book_id == {book_id}').fetchone()[0]
        except Exception as exc:
            raise ValueError('There are no this book!') from exc
        else:
            self._cur.execute(f'DELETE FROM books WHERE book_id == {book_id}')
            self._db.commit()
            self._cur.execute(f'DELETE FROM journal WHERE book_id == {book_id}')
            self._db.commit()

    def AddUser(self, fio, instagram, email):
        self._cur.execute(
            f'INSERT INTO users (fio, instagram, email) VALUES (?,?,?)', (fio, instagram, email))
        self._db.commit()

    def ReadBooks(self, _title, _author):
        if _title == '*' and _author == '*':
            self._cur.execute(f'SELECT * FROM books')
        elif _title == '*':
            self._cur.execute(f'SELECT * FROM books WHERE author == "{_author}"')
        elif _author == '*':
            self._cur.execute(f'SELECT * FROM books WHERE title == "{_title}"')
        else:
            self._cur.execute(f'SELECT * FROM books WHERE (title == "{_title}" AND author == "{_author}")')
        return self._cur.fetchall()

    def IssueBook(self, book_id, _fio, _email, take_date):
        try:
            self._cur.execute(f'SELECT * FROM books WHERE book_id == {book_id}').fetchone()[0]
        except Exception as exc:
            raise ValueError('There are no this book!') from exc
        else:
            try:
                user_id = \
                    self._cur.execute(
                        f'SELECT user_id FROM users WHERE fio == "{_fio}" AND email == "{_email}"').fetchone()[0]
            except Exception as exc:
                raise ValueError('There are no this user!')
            else:
                self._cur.execute(
                    'INSERT INTO journal (book_id, user_id, date_of_taking, return_date) VALUES (?,?,?,NULL)',
                    (book_id, user_id, take_date))
                self._db.commit()
                self._cur.execute(f'UPDATE books SET is_free = 0 WHERE book_id == {book_id}')
                self._db.commit()

    def ReturnBook(self, book_id, return_date):
        try:
            self._cur.execute(f'SELECT * FROM books WHERE book_id == {book_id}').fetchone()[0]
        except Exception as exc:
            raise ValueError('There are no this book!')
        else:
            self._cur.execute(f'UPDATE journal SET  return_date = "{return_date}" WHERE book_id == {book_id}')
            self._db.commit()
            self._cur.execute(f'UPDATE books SET is_free = 1 WHERE book_id == {book_id}')
            self._db.commit()

    def ReadUsers(self, fio):
        if fio == '*':
            self._cur.execute(f'SELECT * FROM users')
        else:
            self._cur.execute(f'SELECT * FROM users WHERE fio == "{fio}"')
        return self._cur.fetchall()

    def ReadDebtBooks(self, fio):
        user_id = self._cur.execute(f'SELECT user_id FROM users WHERE fio == "{fio}"').fetchone()[0]
        book_ids = self._cur.execute(
            f'SELECT book_id FROM journal WHERE user_id == {user_id} AND return_date IS NULL').fetchall()
        book_ids = [id[0] for id in book_ids]
        return self._cur.execute(
            f'SELECT title FROM books WHERE book_id IN({", ".join(list(map(str, book_ids)))})').fetchall()

    def ReadDebtorsEmails(self):
        user_ids = self._cur.execute(f'SELECT user_id FROM journal WHERE return_date IS NULL').fetchall()
        debtors_set = set()
        for id in user_ids:
            debtors_set.add(id[0])
        emails = []
        for id in debtors_set:
            emails.append(self._cur.execute(f'SELECT fio, email FROM users WHERE user_id == {id}').fetchone())
        return emails

    def ReadDebtorsInstagrams(self):
        user_ids = self._cur.execute(
            f'SELECT user_id FROM journal WHERE return_date IS NULL').fetchall()

        debtors_set = set()
        for id in user_ids:
            debtors_set.add(id[0])
        instagrams = []
        for id in debtors_set:
            instagrams.append(
                self._cur.execute(f'SELECT fio, instagram FROM users WHERE user_id == {id}').fetchone())
        return instagrams

    def __del__(self):
        self._db.close()
