from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PythonUi.MainWindow_UI import Ui_MainWindow
from PythonUi.UI_Functions import UI_Functuions
from PyQt5.Qt import QEvent, QColor, QPalette, QBrush
from PyQt5.QtCore import Qt
from PythonBackend.Database import Database
from datetime import date
from PythonBackend.EmailSender import Sender


class MainPage(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center_window()
        # If burger menu button has been clicked than we open Menu
        self.ui.toggleButton.clicked.connect(lambda: UI_Functuions().toggleMenu(self, True, 150))

        # Change page by button click
        self.ui.btn_add_book_page.clicked.connect(lambda: self.goToPage(0))
        self.ui.btn_delete_book_page.clicked.connect(lambda: self.goToPage(1))
        self.ui.btn_view_books_page.clicked.connect(lambda: self.goToPage(2))
        self.ui.btn_view_students_page.clicked.connect(lambda: self.goToPage(3))
        self.ui.btn_issue_book_to_student_page.clicked.connect(lambda: self.goToPage(4))
        self.ui.btn_return_book_page.clicked.connect(lambda: self.goToPage(5))
        self.ui.btn_add_student_page.clicked.connect(lambda: self.goToPage(6))
        self.ui.btn_spam_debtors_page.clicked.connect(lambda: self.goToPage(7))

        # Settings styles and headers for tableWidgets
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ['Book ID', 'Title', 'Author', 'Genre', 'Publishing year', 'Is Free'])
        self.ui.tableWidget_2.setHorizontalHeaderLabels(['User ID', 'FIO', 'Instagram', 'Email', 'Debt books'])
        self.styleTable(self.ui.tableWidget)
        self.styleTable(self.ui.tableWidget_2)

        # Database connecting
        self.db = Database('library.db')
        self.ui.pushButton.clicked.connect(lambda: self.addBook())
        self.ui.pushButton_3.clicked.connect(lambda: self.deleteBook())
        self.ui.pushButton_17.clicked.connect(lambda: self.readBooks())
        self.ui.pushButton_5.clicked.connect(lambda: self.issueBook())
        self.ui.pushButton_7.clicked.connect(lambda: self.returnBook())
        self.ui.pushButton_18.clicked.connect(lambda: self.addUser())
        self.ui.pushButton_11.clicked.connect(lambda: self.viewReaders())

        # Hiding all error labels before program downloads
        self.err_labels = [self.ui.err_1, self.ui.err_2, self.ui.err_3, self.ui.err_4, self.ui.err_5]
        self.hide_all_err_labels()

        # Connecting for cancel buttons clearing of all lineEdit fields functions
        self.cancel_btns = [self.ui.pushButton_2, self.ui.pushButton_4, self.ui.pushButton_6, self.ui.pushButton_8,
                            self.ui.pushButton_19]
        self.funcs = [self.clear_add_book_page, self.clear_delete_page, self.clear_issue_page, self.clear_return_page,
                      self.clear_add_user_page]
        for i, btn in enumerate(self.cancel_btns):
            btn.clicked.connect(self.funcs[i])

        # Connceting for spam debtors on email button function that will send messages on email for debtors
        self.sender = Sender('sh4dowauthor@gmail.com', 'PaShA_1712')
        self.ui.pushButton_10.clicked.connect(self.spamDebtorsEmail)

        qApp.installEventFilter(self)

    def spamDebtorsEmail(self):
        debtors = self.db.ReadDebtorsEmails()
        for debtor in debtors:
            self.sender.sendMessage(debtor[1],
                                    f'Hello {debtor[0]} you should to return book into our library.')

    def viewReaders(self):
        fio = self.ui.lineEdit_5.text()
        # print(fio)
        self.ui.tableWidget_2.setRowCount(0)
        if fio:
            users = self.db.ReadUsers(fio)
            books = []
            for user in users:
                books.append(', '.join([book[0] for book in self.db.ReadDebtBooks(user[1])]))
            self.ui.tableWidget_2.setRowCount(len(users))
            print(books)
            users = [users[i] + tuple([books[i]]) for i in range(len(users))]
            print(users)
            for i, user in enumerate(users):
                for j in range(len(user)):
                    self.ui.tableWidget_2.setItem(i, j, QTableWidgetItem(str(user[j])))
        self.clear_line_edits([self.ui.lineEdit_5])

    def goToPage(self, number):
        self.ui.stackedWidget.setCurrentIndex(number)
        self.hide_all_err_labels()
        for func in self.funcs:
            func()

    def hide_all_err_labels(self):
        for label in self.err_labels:
            label.hide()

    def show_err(self, label, msg):
        label.show()
        label.setText(msg)
        label.setStyleSheet('background-color: rgb(255, 39, 39);')

    def show_success(self, label: QLabel):
        label.show()
        label.setStyleSheet('background-color: rgb(40, 255, 29);')
        label.setText('Success')

    def clear_line_edits(self, ls):
        for lineedit in ls:
            lineedit.clear()

    def clear_add_book_page(self):
        self.clear_line_edits([self.ui.edit_Title, self.ui.edit_Author,
                               self.ui.edit_Genre, self.ui.edit_Id])

    def clear_add_user_page(self):
        self.clear_line_edits([self.ui.lineEdit_13, self.ui.lineEdit_14, self.ui.lineEdit_16, self.ui.lineEdit_6])

    def addUser(self):
        second_name = self.ui.lineEdit_13.text().strip().lower()
        first_name = self.ui.lineEdit_14.text().strip().lower()
        third_name = self.ui.lineEdit_16.text().strip().lower()
        email = self.ui.lineEdit_6.text().strip().lower()

        if not first_name or not second_name or not third_name or not email:
            if not first_name:
                self.show_err(self.ui.err_5, 'Empty first name')
                self.ui.lineEdit_13.clear()
            elif not second_name:
                self.show_err(self.ui.err_5, 'Empty second name')
                self.ui.lineEdit_14.clear()
            elif not third_name:
                self.show_err(self.ui.err_5, 'Empty third name')
                self.ui.lineEdit_16.clear()
            else:
                self.show_err(self.ui.err_5, 'Empty email')
                self.ui.lineEdit_6.clear()
        else:
            fio = f"{first_name} {second_name} {third_name}"
            self.db.AddUser(fio, self.ui.lineEdit_15.text(), email)
            self.show_success(self.ui.err_5)
            self.clear_add_user_page()

    def clear_return_page(self):
        self.clear_line_edits([self.ui.lineEdit_4])

    def returnBook(self):
        book_id = self.ui.lineEdit_4.text()
        try:
            self.db.ReturnBook(book_id, date.today())
        except ValueError as e:
            self.show_err(self.ui.err_4, e.__str__())
        else:
            self.show_success(self.ui.err_4)
        self.clear_return_page()

    def clear_delete_page(self):
        self.clear_line_edits([self.ui.lineEdit])

    def deleteBook(self):
        book_id = self.ui.lineEdit.text()
        try:
            self.db.DeleteBook(book_id)
        except ValueError as e:
            self.show_err(self.ui.err_2, e.__str__())
        else:
            self.show_success(self.ui.err_2)
        self.clear_delete_page()

    def addBook(self):
        title, author, genre, publish_year = self.ui.edit_Title.text(), self.ui.edit_Author.text(), \
                                             self.ui.edit_Genre.text(), self.ui.edit_Id.text()

        if not title or not genre:
            if not title:
                self.show_err(self.ui.err_1, 'Empty title')
                self.ui.edit_Title.clear()
            else:
                self.show_err(self.ui.err_1, 'Empty genre')
                self.ui.edit_Genre.clear()
        else:
            self.db.AddBook(title.strip().strip().lower(), author.strip().strip().lower(), genre.strip().lower(),
                            publish_year)
            self.show_success(self.ui.err_1)
            self.clear_add_book_page()

    def clear_read_books_page(self):
        self.clear_line_edits([self.ui.lineEdit_11, self.ui.lineEdit_12])

    def readBooks(self):
        title, author = self.ui.lineEdit_11.text().strip().lower(), self.ui.lineEdit_12.text().strip().lower()
        self.ui.tableWidget.setRowCount(0)
        if title and author:
            books = self.db.ReadBooks(title, author)
            self.ui.tableWidget.setRowCount(len(books))
            for i, book in enumerate(books):
                for j in range(len(book)):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(book[j])))
        self.clear_read_books_page()

    def clear_issue_page(self):
        self.clear_line_edits([self.ui.lineEdit_2, self.ui.lineEdit_3, self.ui.lineEdit_8])

    def issueBook(self):
        book_id, fio, email, data = self.ui.lineEdit_2.text().strip().lower(), self.ui.lineEdit_3.text().strip().lower(), \
                                    self.ui.lineEdit_8.text().strip().lower(), date.today()
        try:
            self.db.IssueBook(book_id, fio, email, data)
        except ValueError as e:
            self.show_err(self.ui.err_3, e.__str__())
        else:
            self.show_success(self.ui.err_3)
            self.clear_issue_page()

    def styleTable(self, widget):
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Active, QPalette.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        brush11 = QBrush(QColor(210, 210, 210, 128))
        brush11.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush11)
        # endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
        brush12 = QBrush(QColor(210, 210, 210, 128))
        brush12.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush12)
        # endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush13 = QBrush(QColor(51, 153, 255, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush13)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        brush14 = QBrush(QColor(210, 210, 210, 128))
        brush14.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush14)
        # endif
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        brush15 = QBrush(QColor(39, 44, 54, 255))
        brush15.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush16 = QBrush(QColor(210, 210, 210, 128))
        brush16.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush16)
        # endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush17 = QBrush(QColor(210, 210, 210, 128))
        brush17.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush17)
        # endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush18 = QBrush(QColor(210, 210, 210, 128))
        brush18.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush18)
        # endif
        widget.setPalette(palette1)
        widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        widget.setAlternatingRowColors(False)
        widget.setSelectionMode(QAbstractItemView.SingleSelection)
        widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        widget.setShowGrid(True)
        widget.setGridStyle(Qt.SolidLine)
        widget.setSortingEnabled(False)
        widget.horizontalHeader().setVisible(True)
        widget.horizontalHeader().setCascadingSectionResizes(True)
        widget.horizontalHeader().setDefaultSectionSize(200)
        widget.horizontalHeader().setStretchLastSection(True)
        widget.verticalHeader().setVisible(False)
        widget.verticalHeader().setCascadingSectionResizes(False)
        widget.verticalHeader().setHighlightSections(False)
        widget.verticalHeader().setStretchLastSection(True)

    def center_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def eventFilter(self, obj, event):
        if obj.objectName() == 'frame_left_menu':
            if event.type() == QEvent.Resize:  # if mouse on button than we will change png image
                if obj.width() < 141:
                    self.ui.btn_spam_debtors_page.setText(' ')
                    self.ui.btn_add_book_page.setText(' ')
                    self.ui.btn_delete_book_page.setText(' ')
                    self.ui.btn_add_student_page.setText(' ')
                    self.ui.btn_return_book_page.setText(' ')
                    self.ui.btn_issue_book_to_student_page.setText(' ')
                    self.ui.btn_view_books_page.setText(' ')
                    self.ui.btn_view_students_page.setText(' ')

                if obj.width() > 140:  # if we out from image than we will change png image to default
                    self.ui.btn_spam_debtors_page.setText(' Spam debtors')
                    self.ui.btn_add_book_page.setText(' Add book')
                    self.ui.btn_delete_book_page.setText(' Delete book')
                    self.ui.btn_add_student_page.setText(' Add student')
                    self.ui.btn_return_book_page.setText(' Return book')
                    self.ui.btn_issue_book_to_student_page.setText(' Issue book')
                    self.ui.btn_view_books_page.setText(' View books')
                    self.ui.btn_view_students_page.setText(' View students')

        return QWidget.eventFilter(self, obj, event)
