# Library-Managment-System
This is a course project in python. This application helps librarians monitor readers, as well as notify them if they do not return books
____
## Nedeed libraries installation:

### Selenium

```python
pip install selenium
```

### smtplib

```python
pip install smtplib
```

### PyQt5

```python
pip install PyQt5
pip install PyQt5-tools
```

____
## In this project we home some functions:

### Add book
  In this function we add book into our database. For adding we should enter title, author, genre and publish year of a book. Necessary data is title and genre, unnecessary data is publish year, cause not always we know specific year of book publishing, and author, cause not always we know real author of a book.
For inteface used lineEdits, pushButtons and labels.
### Delete book
  In this function we delete book from database. For book deliting we should enter book id, these data are enough, cause every book have unique id.
For inteface used lineEdits, pushButtons and labels.
### View books
  In this function we show queried books by title and author name. If you enter in some of fields '*', '*', these function will return all meanings of this field.
For interface used lineEdits, pushButtons, labels and tableWidget.
### Issue book
  In this function we are editing our database. The database change is that we enter into the journal table with user_id, book_id, date_of_taking, and return_date (which is None by default). And we make field is_free of a book False. All fields: book_id, FIO, email are necessary.
For interface used lineEdits, pushButtons and labels. 
### Return book
  In this function we are editing our database. We editing field return_date in table journal and setting current date for specific book_id.
For interface used lineEdit, pushButtons and labels.
### Add student
  In this function we add student into our database. We are edditing user table in our database. For adding we should enter neccessary fields: first name, second name, third name and email, actually we can write instagram nickname but it is unnecessary.
For interface was used lineEdits, labels and pushButtons.
### View Students
  In this function we show queried student FIO. If you enter in FIO field '*', '*', these function will return all meanings of this field.
For interface used lineEdits, pushButtons, labels and tableWidget.
### Spam Debtors
  In this fucntion we writing messages to debtors instagrams using library selenium(and writed on it InstagramBot) and to spam into emails we use library smtplib.
