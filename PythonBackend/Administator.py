from Database import Database
from InstagramBot import InstagramBot
from EmailSender import Sender
from PyQt5.QtWidgets import *
from datetime import date


class Administrator:

    def __init__(self):
        self.bot = InstagramBot('***', '***')
        self.sender = Sender('***',
                             '***')  # с целью сохранения конфиденциальности логин и пароль был заменён на ***def start_db(self, name):self.db = Database(name)

    def start_db(self, name):
        self.db = Database(name)

    def SpamDebtorsInstagram(self):
        debtors = self.db.ReadDebtorsInstagrams()
        flag = False
        for debtor in debtors:
            if debtor[1]:
                flag = True
                self.bot.openInstagram()
                self.bot.logIn('___', '___')
                self.bot.sendMessage(debtor[1], f'Hello {debtor[0]} you should to return book into our library.')
        if flag:
            self.bot.closeBrowser()

    def SpamDebtorsEmails(self):
        debtors = self.db.ReadDebtorsEmails()
        for debtor in debtors:
            self.sender.sendMessage(debtor[1], f'Hello {debtor[0]} you should to return book into our library.')

    @staticmethod
    def capitalize(string):
        return string.capitalize()

    def ViewReaders(self, window):
        fio = window.ui.lineEdit_5.text().strip().lower()
        window.ui.tableWidget_2.setRowCount(0)
        if fio:
            users = self.db.ReadUsers(fio)
            books = []
            for i in range(len(users)):
                books.append(', '.join([book[0] for book in self.db.ReadDebtBooks(users[i][1])]))
                t = list(users[i])
                t[1] = ' '.join([self.capitalize(name) for name in users[i][1].split()])
                users[i] = tuple(t)

            window.ui.tableWidget_2.setRowCount(len(users))

            users = [users[i] + tuple([books[i]]) for i in range(len(users))]
            for i, user in enumerate(users):
                for j in range(len(user)):
                    window.ui.tableWidget_2.setItem(i, j, QTableWidgetItem(str(user[j])))

        window.clear_line_edits([window.ui.lineEdit_5])

    def IssueBook(self, window):
        book_id, fio, email, current_date = window.ui.lineEdit_2.text().strip().lower(), \
                                            window.ui.lineEdit_3.text().strip().lower(), \
                                            window.ui.lineEdit_8.text().strip().lower(), \
                                            date.today()
        try:
            self.db.IssueBook(book_id, fio, email, current_date)
        except ValueError as e:
            window.show_err(window.ui.err_3, e.__str__())
        else:
            window.show_succes(window.ui.err_3)
            window.clear_issue_page()

    def ReturnBook(self, window):
        book_id = window.ui.lineEdit_4.text().strip().lower()
        try:
            self.db.ReturnBook(book_id, date.today())
        except ValueError as e:
            window.show_err(window.ui.err_4, e.__str__())
        else:
            window.show_success(window.ui.err_4)
        window.clear_return_page()

    def DeleteBook(self, window):
        book_id = window.ui.lineEdit.text().strip().lower()
        try:
            self.db.DeleteBook(book_id)
        except ValueError as e:
            window.show_err(window.ui.err_2, e.__str__())
        else:
            window.show_success(window.ui.err_2)
        window.clear_delete_page()

    def AddBook(self, window):
        title, author, genre, publish_year = (window.ui.edit_Title.text().strip().lower(),
                                              window.ui.edit_Author.text().strip().lower(),
                                              window.ui.edit_Genre.text().strip().lower(),
                                              window.ui.edit_Id.text().strip().lower())
        if not title or not genre:
            if not title:
                window.show_err(window.ui.err_1, 'Empty title')
                window.ui.edit_Title.clear()
            else:
                window.show_err(window.ui.err_1, 'Empty genre')
                window.ui.edit_Genre.clear()
        else:
            self.db.AddBook(title.strip().strip().lower(), author.strip().strip().lower(), genre.strip().lower(),
                            publish_year)
            window.show_success(window.ui.err_1)
            window.clear_add_book_page()

    def ReadBooks(self, window):
        title, author = window.ui.lineEdit_11.text().strip().lower(), window.ui.lineEdit_12.text().strip().lower()
        window.ui.tableWidget.setRowCount(0)
        if title and author:
            books = self.db.ReadBooks(title, author)
            window.ui.tableWidget.setRowCount(len(books))
            for i, book in enumerate(books):
                for j in range(len(book)):
                    window.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(book[j]).capitalize()))
        window.clear_read_books_page()

    def AddUser(self, window):
        second_name = window.ui.lineEdit_13.text().strip().lower()
        first_name = window.ui.lineEdit_14.text().strip().lower()
        third_name = window.ui.lineEdit_16.text().strip().lower()
        email = window.ui.lineEdit_6.text().strip().lower()
        if not first_name or not second_name or not third_name or not email:
            if not first_name:
                window.show_err(window.ui.err_5, 'Empty first name')
                window.ui.lineEdit_13.clear()
            elif not second_name:
                window.show_err(window.ui.err_5, 'Empty second name')
                window.ui.lineEdit_14.clear()
            elif not third_name:
                window.show_err(window.ui.err_5, 'Empty third name')
                window.ui.lineEdit_16.clear()
            else:
                window.show_err(window.ui.err_5, 'Empty email')
                window.ui.lineEdit_6.clear()
        else:
            fio = f"{first_name} {second_name} {third_name}"
            self.db.AddUser(fio, window.ui.lineEdit_15.text(), email)
            window.show_success(window.ui.err_5)
            window.clear_add_user_page()
