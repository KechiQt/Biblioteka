import sys
import pandas as pd

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

import gui
from SqliteHelper import *

helper = SqliteHelper("Library.db")


def show_message(title, message):
    QMessageBox.information(None, title, message)


class Example(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_4.clicked.connect(self.groupbox_data_add)
        self.pushButton_2.clicked.connect(self.groupbox_data_add)
        self.Ksave.clicked.connect(self.addData)
        self.Kdelete.clicked.connect(self.delete_row)
        self.Knew.clicked.connect(self.addRowTable)
        self.ExportButt.clicked.connect(self.export_table)
        self.Ksearch.clicked.connect(self.findParam)
        self.Ksearch_2.clicked.connect(self.findParam)
        self.Asearch.clicked.connect(self.findParam)
        self.Search_Butt.clicked.connect(self.findParam)
        self.pushDel.clicked.connect(self.lineEditK.clear)
        self.Rdeltext.clicked.connect(self.RlineEdit.clear)
        self.tabWidget.currentChanged.connect(self.refresh)
        name_tables = self.ViewTab()
        name_tables.itemSelectionChanged.connect(self.EnableButtom)
        self.tableWidgetPublic.itemClicked.connect(self.ClickedPubliher)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.EnableButtom)
        self.timer.start()

        self.LoadData()

    def EnableButtom(self):
        name_tables = self.ViewTab()
        if name_tables.hasFocus():
            self.Kdelete.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.Ksave.setEnabled(True)
        else:
            self.Kdelete.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            if name_tables == self.tableWidgetPublic:
                self.Ksave.setEnabled(True)
                self.ExportButt.setEnabled(False)
                name_tables.setFocusPolicy(QtCore.Qt.NoFocus)
                if self.Check_ID.text() == '':
                    self.Kdelete.setEnabled(False)
                else:
                    self.Kdelete.setEnabled(True)
            else:
                self.Ksave.setEnabled(False)
                self.ExportButt.setEnabled(True)

        if name_tables == self.tableWidget_2:
            self.Ksave.setEnabled(False)
            self.Knew.setEnabled(False)
        else:
            self.Knew.setEnabled(True)

    def get_table(self):
        return self.tabWidget.currentIndex()

    def ViewTab(self):
        tables = None
        indexT = self.get_table()

        if indexT == 0:
            tables = self.KtableWidget
        elif indexT == 1:
            tables = self.RtableWidget
        elif indexT == 2:
            tables = self.tableWidgetPublic
        elif indexT == 3:
            tables = self.tableWidget_2
        return tables

    def table_select(self):
        name_tables = self.get_table()
        dateT = None

        if name_tables == 0:
            dateT = helper.select("SELECT IdBook, NameB, Author, Genre, YearOfPub,NameP FROM Book"
                                  " LEFT JOIN Publishers ON Book.IdPublisher = Publishers.IdPublisher")
        elif name_tables == 1:
            dateT = helper.select("SELECT * FROM Reader")
        elif name_tables == 2:
            dateT = helper.select("SELECT IdPublisher, NameP FROM Publishers")
        elif name_tables == 3:
            dateT = helper.select("SELECT IdDelivery, NameB, Lastname, Firstname, Fastername, dataDelivery, dataReturn "
                                  "FROM Delivery INNER JOIN Book ON Delivery.IdBook = Book.IdBook "
                                  "INNER JOIN Reader ON Delivery.IdReader = Reader.IdReader")
        return dateT

    def table_insert(self, lists):
        name_tables = self.get_table()
        if name_tables == 0:
            helper.insert("INSERT INTO Book (NameB, Author, Genre, YearOfPub, IdPublisher) "
                          "VALUES(?,?,?,?,?)", lists)
        elif name_tables == 1:
            helper.insert("INSERT INTO Reader(Lastname, Firstname, Fastername, Address, Tel) "
                          "VALUES(?,?,?,?,?)", lists)
        elif name_tables == 2:
            helper.insert("INSERT INTO Publishers (NameP, Country, City, Founded, Tel, Email, Comment) "
                          "VALUES(?,?,?,?,?,?,?)", lists)
        elif name_tables == 3:
            helper.insert("INSERT INTO Delivery (IdBook, IdReader, dataDelivery) "
                          "VALUES(?,?,?)", lists)

    def table_update(self, lists):
        name_tables = self.get_table()
        tables_ID = self.getRowTableID()
        if name_tables == 0:
            helper.edit("UPDATE Book SET NameB =?, Author =?, Genre =?, YearOfPub =?, IdPublisher =? "
                        "WHERE IdBook = " + tables_ID, lists)
        elif name_tables == 1:
            helper.edit("UPDATE Reader SET Lastname =?, Firstname =?, Fastername =?, Address =?, Tel =? "
                        "WHERE IdReader = " + tables_ID, lists)
        elif name_tables == 2:
            helper.edit("UPDATE Publishers SET NameP =?, Country =?, City =?, Founded =?, Tel =? , Email =?, Comment =?"
                        "WHERE IdPublisher = " + tables_ID, lists)
        elif name_tables == 3:
            helper.edit("UPDATE Delivery SET dataReturn =? WHERE IdDelivery = " + tables_ID, lists)

    def table_delete(self, id_table):
        name_tables = self.get_table()

        if name_tables == 0:
            helper.delete("DELETE FROM Book WHERE IdBook =" + id_table)
        elif name_tables == 1:
            helper.delete("DELETE FROM Reader WHERE IdReader =" + id_table)
        elif name_tables == 2:
            helper.delete("DELETE FROM Publishers WHERE IdPublisher =" + id_table)
        elif name_tables == 3:
            helper.delete("DELETE FROM Delivery WHERE IdDelivery =" + id_table)

    def LoadData(self):
        name_tables = self.ViewTab()
        tableDate = self.table_select()
        for row_number, item_date in enumerate(tableDate):
            name_tables.insertRow(row_number)
            for column_number, data in enumerate(item_date):
                cell = QtWidgets.QTableWidgetItem(str(data))
                name_tables.setItem(row_number, column_number, cell)

    def addRowTable(self):
        name_tables = self.ViewTab()

        rowPosition = name_tables.rowCount()
        name_tables.insertRow(rowPosition)

        if name_tables == self.tableWidgetPublic:
            self.ClearPublishers()

    def ClearPublishers(self):
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.textEdit.clear()
        self.Check_ID.setText("")

    def addData(self):
        liste = []
        name_tables = self.ViewTab()
        errorCheck = False
        if name_tables != self.tableWidgetPublic:
            cols = name_tables.columnCount()
            for cols in range(cols):
                if cols == 0:
                    continue
                else:
                    getItem = name_tables.item(name_tables.currentRow(), cols).text()
                    if getItem.strip(" ") != '':
                        liste.append(getItem)
                    else:
                        errorCheck = True
        else:
            name = self.lineEdit_4.text()
            county = self.lineEdit_5.text()
            city = self.lineEdit_6.text()
            founder = self.lineEdit_7.text()
            tel = self.lineEdit_8.text()
            email = self.lineEdit_9.text()
            comment = self.textEdit.toPlainText()
            if name.strip(" ") != '' and county.strip(" ") != '' and city.strip(" ") != '' \
                    and founder.strip(" ") != '' and tel.strip(" ") != '' and email.strip(" ") != '':
                liste = (name, county, city, founder, tel, email, comment)
            else:
                errorCheck = True
        if errorCheck:
            show_message("Error", "Заполните значение пустые ячейки ")
        else:
            if self.Check_ID.text() != "" or self.getRowTableID() is not False:
                self.table_update(liste)
            else:
                self.table_insert(liste)
            self.refresh()

    def getRowTableID(self):
        name_tables = self.ViewTab()
        if name_tables.item(name_tables.currentRow(), 0) is None:
            return False
        else:
            print(name_tables.item(name_tables.currentRow(), 0).text())
            return name_tables.item(name_tables.currentRow(), 0).text()

    def delete_row(self):
        id_delete = self.getRowTableID()
        self.table_delete(id_delete)
        self.refresh()

    def field_sort(self):
        tables = self.get_table()
        sortField = None

        if tables == 0:
            sortField = self.lineEditK
        elif tables == 1:
            sortField = self.RlineEdit
        elif tables == 2:
            sortField = self.lineSearch
        elif tables == 3:
            sortField = self.lineEdit_delivery
        return sortField

    def findParam(self):
        liste = []
        name_tables = self.ViewTab()
        paramName = str(self.field_sort().text())
        for row in range(name_tables.rowCount()):
            for col in range(name_tables.columnCount()):
                pitem = name_tables.item(row, col)
                if pitem:
                    pName = pitem.text()
                    if pName == paramName:
                        self.setColortoRow(name_tables, row, QColor("yellow"))
                        liste.append(pitem)
        if not liste:
            show_message("Message", "Item not found")

    def setColortoRow(self, tables, rowIndex, color):
        for j in range(tables.columnCount()):
            tables.item(rowIndex, j).setBackground(color)

    def ClickedPubliher(self):
        item_list = self.getRowTableID()
        result = helper.select("SELECT * FROM Publishers WHERE IdPublisher = %s" % item_list)
        new_list = [item for sublist in result for item in sublist]

        ID, name, county, city, founder, tel, email, comment = new_list
        self.lineEdit_4.setText(name)
        self.lineEdit_5.setText(county)
        self.lineEdit_6.setText(city)
        self.lineEdit_7.setText(founder)
        self.lineEdit_8.setText(tel)
        self.lineEdit_9.setText(email)
        self.textEdit.setText(comment)

        self.Check_ID.setText(str(ID))

    def refresh(self):
        self.clearDate()
        self.LoadData()
        self.field_sort().clear()
        self.ClearPublishers()
        self.field_sort().setFocusPolicy(Qt.WheelFocus)
        self.field_sort().setFocus(Qt.OtherFocusReason)
        self.groupbox_data_read()

    def items_reader(self):
        listCombobox = []
        reader_list = helper.select("SELECT Lastname, Firstname, Fastername FROM Reader")

        items = len(reader_list)
        for item in range(items):
            reader_date = reader_list[item]
            nameR = ' '.join(reader_date)
            listCombobox.append(nameR)
        return listCombobox

    def items_book(self):
        books_list = helper.select("SELECT NameB FROM Book")
        data_book = [item for sublist in books_list for item in sublist]
        return data_book

    def items_combobox(self):
        self.BookEx.addItems(self.items_book())
        self.ReaderEx.addItems(self.items_reader())

    def GetDatetime(self):
        rbt = self.sender()
        if rbt == self.pushButton_4:
            dt = self.dateTimeEdit_Vozvrat.dateTime()
            dt_string = dt.toString(self.dateTimeEdit_Vozvrat.displayFormat())
            return dt_string
        elif rbt == self.pushButton_2:
            dt = self.dateTimeEdit_delivery.dateTime()
            dt_string = dt.toString(self.dateTimeEdit_delivery.displayFormat())
            return dt_string

    def getCombobox(self):
        book_text = self.BookEx
        reader_text = self.ReaderEx
        return book_text, reader_text

    def groupbox_data_read(self):
        self.BookEx.clear()
        self.ReaderEx.clear()

        self.GetDatetime()
        self.items_combobox()

    def groupbox_data_add(self):
        itemsCombobox = self.getCombobox()
        list_reader = []
        listre = []
        date_text = self.GetDatetime()

        UsedBut = self.sender()
        if UsedBut == self.pushButton_4:
            listre.append(date_text)
            self.table_update(listre)
        elif UsedBut == self.pushButton_2:
            book_text = itemsCombobox[0].currentText()
            reader_text = itemsCombobox[1].currentText()

            result_b = helper.select("SELECT IdBook FROM Book WHERE NameB = '{}'".format(book_text))
            result_b = [item for sublist in result_b for item in sublist]

            for word in reader_text.split():
                list_reader.append(word)
            result = helper.select("SELECT IdReader FROM Reader WHERE Lastname = '{}'  AND Firstname = '{}'"
                                   " AND Fastername = '{}' ".format(list_reader[0], list_reader[1], list_reader[2], ))
            result = [item for sublist in result for item in sublist]

            listre.extend((result_b[0], result[0], date_text))
            print(listre)

            self.table_insert(listre)
        self.refresh()

    def export_table(self):
        name_tables = self.ViewTab()
        xls_list = []
        items = {}
        iters = name_tables.rowCount()
        open('exportTable.xlsx', 'w').close()
        for row in range(iters + 1):
            if row != 0:
                items['' + str(row)] = xls_list
                xls_list = []
            if row == iters:
                break
            for col in range(name_tables.columnCount()):
                xls_list.append(name_tables.item(row, col).text())
        xls_date = pd.DataFrame(items)

        xls_date.to_excel('exportTable.xlsx', index=False)

    def clearDate(self):
        name_tables = self.ViewTab()
        name_tables.clearSelection()
        while name_tables.rowCount() > 0:
            name_tables.removeRow(0)
            name_tables.clearSelection()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F12:
            self.close()
        if event.key() == Qt.Key_F5:
            self.refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = Example()
    form.show()

    sys.exit(app.exec())
