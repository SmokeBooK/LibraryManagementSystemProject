from fileinput import filename
from tabnanny import filename_only
from tkinter import filedialog
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QIcon
import sys
from datetime import datetime

from ui import res
from lib import db

class LibManage(QMainWindow):
    
    def buttons_menu(self):
       # ฟังก์ชันสำหรับตั้งค่าแท็บที่จะแสดงในหน้าต่างหลัก
       def set_index_tab(index):
           self.tabWidget.setCurrentIndex(index)

       # เชื่อมการคลิกปุ่ม listButton กับการแสดงแท็บที่ 0
       self.listButton.clicked.connect(lambda *args: set_index_tab(0))

       # เชื่อมการคลิกปุ่ม sellButton กับการแสดงแท็บที่ 1 
       self.sellButton.clicked.connect(lambda *args: set_index_tab(1))

       # เชื่อมการคลิกปุ่ม histButton กับการแสดงแท็บที่ 2
       self.histButton.clicked.connect(lambda *args: set_index_tab(2))

       # เชื่อมการคลิกปุ่ม addpageButton กับการแสดงแท็บที่ 3
       self.addpageButton.clicked.connect(lambda *args: set_index_tab(3))

       # เชื่อมการคลิกปุ่ม editpageButton กับการแสดงแท็บที่ 4
       self.editpageButton.clicked.connect(lambda *args: set_index_tab(4))

       # เรียกใช้ฟังก์ชัน initUI() เพื่อเริ่มต้นการสร้างองค์ประกอบบนหน้าจอ
       self.initUI()
    
    # ฟังก์ชันนี้ใช้สำหรับเริ่มต้นการทำงานของ object LibManage ใหม่
    def __init__(self):
        
        # เรียกใช้ฟังก์ชัน __init__ ของ class super
        super(LibManage, self).__init__()

        # โหลด UI จากไฟล์ "lib.ui" มาแสดงผลบน object นี้
        uic.loadUi('ui/lib.ui', self)

        # สร้าง object ของ class DB สำหรับเชื่อมต่อกับฐานข้อมูล
        self.db = db.DB()

        # ตั้งค่า tab แรก (index 0) ให้แสดงผล
        self.tabWidget.setCurrentIndex(0)
        # เชื่อมต่อสัญญาณการเปลี่ยนแปลงของ tab widget กับฟังก์ชัน change_tab
        self.tabWidget.currentChanged.connect(self.change_tab)

        # เรียกใช้งาน function buntons_menu() และเชื่อมต่อสัญญาณคลิกของปุ่ม pushButton ในแต่ละ function
        self.buttons_menu()
        self.pushButton_8.clicked.connect(self.add_book)
        self.pushButton_7.clicked.connect(self.search_book)
        self.pushButton_9.clicked.connect(self.refresh_book)
        self.pushButton_16.clicked.connect(self.search_edit)
        self.pushButton_17.clicked.connect(self.refresh_edit)
        self.pushButton_18.clicked.connect(self.add_to_edit)
        self.pushButton_20.clicked.connect(self.edit_book_bot)
        self.pushButton_19.clicked.connect(self.remove_book)
        self.pushButton_14.clicked.connect(self.add_to_cart)
        self.pushButton_10.clicked.connect(self.search_cart)
        self.pushButton_11.clicked.connect(self.refresh_cart)
        self.pushButton_15.clicked.connect(self.empty_cart)
        self.pushButton_12.clicked.connect(self.sell_cart)
        self.pushButton_13.clicked.connect(self.loan_cart)
        self.pushButton_24.clicked.connect(self.add_change_loan)
        self.pushButton_25.clicked.connect(self.change_loan)
        self.pushButton_22.clicked.connect(self.search_loan)
        self.pushButton_23.clicked.connect(self.refresh_loan)
        
        # กำหนดค่าเริ่มต้นให้ตัวแปร book_id_edit สำหรับการแก้ไขหนังสือ และ loan_id_change สำหรับการเปลี่ยนสถานะการยืม
        self.book_id_edit = None
        self.loan_id_change = None

        # กำหนดค่าเริ่มต้นให้ตัวแปร cart เป็น list ว่าง สำหรับเก็บ ID ของหนังสือที่จะทำการยืม
        self.cart = []

        # เรียกใช้ฟังก์ชัน change_tab เพื่อแสดงหน้าแรก (index 0)
        self.change_tab(0)

        # แสดงหน้าต่างโปรแกรม
        self.show()
    
    def initUI(self):
        self.setWindowTitle("Book+")
        self.setWindowIcon(QIcon('../library-manage-master/ui/icons/icon-windowIcon.png'))
        
    # ฟังก์ชันนี้ใช้สำหรับรีเฟรชหน้าต่างการยืมหนังสือ และเปลี่ยนไปยัง tab ที่ 2 (หน้าต่างการยืมหนังสือ)
    def refresh_loan(self):
        self.change_tab(2)
        self.lineEdit_17.setText('')
    
    #  ฟังก์ชันนี้ใช้สำหรับค้นหาข้อมูลการยืมหนังสือ
    def search_loan(self):
        user_input = self.lineEdit_17.text()
        # สร้างเงื่อนไขถ้า list loan ว่าง
        if user_input != '':
            # ค้นหาสินเชื่อโดยใช้ user_input และเก็บผลลัพธ์ไว้ในตัวแปร loan
            loan = self.db.search_loan(user_input)
            if len(loan) == 0:
                # สร้าง QmessageBox 
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No Loan found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(loan)
                
                # ตั้งค่าป้ายหัวคอลัมน์ของ tableWidget
                self.tableWidget.setColumnCount(5)
                self.tableWidget.setRowCount(rowCount)
                self.tableWidget.setHorizontalHeaderLabels(['Id', 'Name', 'User Id', 'Date', 'Days Gone By'])
                
                # สร้างเงื่อนไขถ้า list loan ไม่ว่าง
                if len(loan) != 0:
                    for i in range(len(loan)):
                        for j in range(5):
                            
                            # ถ้าเป็นคอลัมน์สุดท้าย (วันที่ผ่านมา)
                            if j == 4:
                                date_format = '%Y-%m-%d %H:%M:%S.%f'
                                a = datetime.strptime(loan[i][j+1], date_format)
                                b = datetime.strptime(str(datetime.now()), date_format)
                                delta = b - a
                                self.tableWidget.setItem(i, j, QTableWidgetItem(str(delta.days)))
                             # ถ้าเป็นคอลัมน์ที่ 4 (วันที่)
                            if j == 3:
                                self.tableWidget.setItem(i, j, QTableWidgetItem(loan[i][j+2]))
                            else:
                                # กำหนดค่าในเซลล์ tableWidget 
                                self.tableWidget.setItem(i, j, QTableWidgetItem(str(loan[i][j])))
                
                # ตารางจะพอดีกับหน้าจอแนวนอน
                self.tableWidget.horizontalHeader().setStretchLastSection(True)
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def change_loan(self):
        # ถ้า loan_id_change ยังไม่ได้รับการกำหนดค่า
        if self.loan_id_change == None:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        # ถ้า loan_id_change ได้รับการกำหนดค่าแล้ว
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Change the status of the borrowed book")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Information)
            result = msg.exec_()
            
            # ถ้าผู้ใช้ตอบตกลง (Ok)
            if result ==  QMessageBox.StandardButton.Ok:
                # เปลี่ยนสถานะการยืม
                self.db.change_loan_status(self.loan_id_change)
                # แสดงกล่องข้อความแจ้งผลสำเร็จ
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Status changed successfully.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                # รีเซ็ตค่า loan_id_change
                self.loan_id_change = None
                # รีเซ็ตตาราง tableWidget_6
                self.tableWidget_6.setColumnCount(2)
                self.tableWidget_6.setRowCount(0)
                self.tableWidget_6.setHorizontalHeaderLabels(['Name', 'Number'])
                
                # ตารางจะพอดีกับหน้าจอแนวนอน
                self.tableWidget_6.horizontalHeader().setStretchLastSection(True)
                self.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.change_tab(2)
    
    
    def add_change_loan(self):
        # ลองดึงรหัสจากตารางด้านบน
        try:
            user_input_id = self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        # ถ้าไม่สามารถดึงรหัสได้ (ผู้ใช้ไม่ได้เลือก)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            self.loan_id_change = user_input_id
            # ดึงข้อมูลสินเชื่อจากฐานข้อมูล
            loan = self.db.get_loan_cart(self.loan_id_change)
            rowCount = len(loan)
            self.tableWidget_6.setColumnCount(2)
            self.tableWidget_6.setRowCount(rowCount)
            self.tableWidget_6.setHorizontalHeaderLabels(['Name', 'Number'])
            
             # วนลูปเพื่อนำข้อมูลมาแสดงใน tableWidget_6
            for i in range(rowCount):
                for j in range(2):
                    if j == 0:
                        self.tableWidget_6.setItem(i, j, QTableWidgetItem(str(loan[i]['name'])))
                    if j == 1:
                        self.tableWidget_6.setItem(i, j, QTableWidgetItem(str(loan[i]['number'])))
            
            # ตารางจะพอดีกับหน้าจอแนวนอน
            self.tableWidget_6.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    
    def loan_cart(self):
        # รับค่ารหัสผู้ใช้และชื่อผู้ใช้จากกล่องข้อความ
        user_id = self.lineEdit_5.text()
        user_name = self.lineEdit_7.text()
        # ตรวจสอบว่ากรอกข้อมูลครบหรือไม่ และมีสินค้าในตะกร้าหรือไม่
        if user_id == '' or user_name == '' or self.cart == []:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Information")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        # ถ้ากรอกข้อมูลครบและมีสินค้าในตะกร้า
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Lend Cart")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Information)
            result = msg.exec_()
            # ถ้าผู้ใช้ตอบตกลง (Ok)
            if result ==  QMessageBox.StandardButton.Ok:
                # บันทึกการยืมสินค้าลงฐานข้อมูล
                self.db.loan_book(user_id, user_name, self.cart)
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Cart Lended.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.lineEdit_6.setText('')
                # เปลี่ยนแท็บไปที่แท็บที่ 1
                self.change_tab(1)
                # รีเซ็ตตะกร้าสินค้า
                self.cart = []
                self.tableWidget_5.setColumnCount(4)
                self.tableWidget_5.setRowCount(len(self.cart))
                self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
                self.label_11.setText('')
    
    # ฟังก์ชันการซื้อสินค้าในตะกร้า
    def sell_cart(self):
        user_id = self.lineEdit_5.text()
        user_name = self.lineEdit_7.text()
        # ตรวจสอบว่ากรอกข้อมูลครบหรือไม่ และมีสินค้าในตะกร้าหรือไม่
        if user_id == '' or user_name == '' or self.cart == []:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Information")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Sell Cart")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Information)
            result = msg.exec_()
            if result ==  QMessageBox.StandardButton.Ok:
                self.db.sell_book(user_id, user_name, self.cart)
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Cart Selled.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.lineEdit_6.setText('')
                self.change_tab(1)
                self.cart = []
                self.tableWidget_5.setColumnCount(4)
                self.tableWidget_5.setRowCount(len(self.cart))
                self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
                self.label_11.setText('')
    
    # ฟังก์ชัน empty_cart นี้ใช้สำหรับล้างสินค้าออกจากตะกร้า
    def empty_cart(self):
        msg = QMessageBox()
        msg.setWindowTitle("Empty Cart")
        msg.setText("Are you sure you want to do this?")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setIcon(QMessageBox.Icon.Warning)
        result = msg.exec_()
        if result ==  QMessageBox.StandardButton.Ok:
            self.cart = []
            self.tableWidget_5.setColumnCount(4)
            self.tableWidget_5.setRowCount(len(self.cart))
            self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
            # ล้างค่าใน label_11
            self.label_11.setText('')
    
    # ฟังก์ชัน refresh_cart ใช้สำหรับรีเฟรชสินค้าที่อยู่ในตะกร้า
    def refresh_cart(self):
        self.lineEdit_6.setText('')
        self.change_tab(1)
    
    # ฟังก์ชัน search_cart ใช้สำหรับค้นหาสินค้าที่อยู่ในตะกร้า
    def search_cart(self):
        user_input = self.lineEdit_6.text()
        if user_input != '':
            books = self.db.search_book(user_input)
            # กรณีไม่มีสินค้าในตะกร้า
            if len(books) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No book found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(books)
                self.tableWidget_3.setColumnCount(3)
                self.tableWidget_3.setRowCount(rowCount)
                self.tableWidget_3.setHorizontalHeaderLabels(['Id', 'Name', 'Writer'])
                if len(books) != 0:
                    for i in range(len(books)):
                        for j in range(3):
                            if j == 2:
                                self.tableWidget_3.setItem(i, j, QTableWidgetItem(books[i][j+1]))
                            else:
                                self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(books[i][j])))
    
    # ฟังก์ชัน add_to_cart ใช้สำหรับเพิ่มสินค้าลงในตะกร้า
    def add_to_cart(self):
        try:
            user_input_id = self.tableWidget_4.item(self.tableWidget_4.currentRow(),0).text()
            user_input_name = self.tableWidget_4.item(self.tableWidget_4.currentRow(),1).text()
            user_input_price = self.tableWidget_4.item(self.tableWidget_4.currentRow(),4).text()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            number = self.spinBox_3.text()
            self.cart.append({
                'id': user_input_id,
                'name': user_input_name,
                'price': user_input_price,
                'number': number,
            })
            self.tableWidget_5.setColumnCount(4)
            self.tableWidget_5.setRowCount(len(self.cart))
            self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
            if len(self.cart) != 0:
                for i in range(len(self.cart)):
                    self.tableWidget_5.setItem(i, 0, QTableWidgetItem(str(self.cart[i]['name'])))
                    self.tableWidget_5.setItem(i, 1, QTableWidgetItem(str(self.cart[i]['price'])))
                    self.tableWidget_5.setItem(i, 2, QTableWidgetItem(str(self.cart[i]['number'])))
                    t_price = int(self.cart[i]['number']) * float(self.cart[i]['price'])
                    self.tableWidget_5.setItem(i, 3, QTableWidgetItem(str(t_price)))
            
            # คำนวณ total cart 
            total = 0
            for i in range(len(self.cart)):
                total += int(self.cart[i]['number']) * float(self.cart[i]['price'])
            self.label_11.setText(str(total))
    
    # ลบรายการ
    def remove_book(self):
        if self.book_id_edit == None:
            pass
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Delete Book")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Warning)
            result = msg.exec_()
            if result ==  QMessageBox.StandardButton.Ok:
                self.db.del_book(self.book_id_edit)
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Book deleted successfully.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.book_id_edit = None
                self.lineEdit_9.setText('')
                self.lineEdit_11.setText('')
                self.lineEdit_10.setText('')
    
    # ตั้งค่ารายการ เพิ่มข้อมูลหนังสือ
    def edit_book_bot(self):
        if self.book_id_edit == None:
            pass
        else:
            name = self.lineEdit_9.text()
            publisher = self.lineEdit_11.text()
            writer = self.lineEdit_10.text()
            subject = self.comboBox_2.currentText()
            year = self.spinBox_6.text()
            published = self.spinBox_4.text()
            number = self.spinBox_5.text()
            price = self.doubleSpinBox_2.text()
            self.db.edit_book(self.book_id_edit, name, publisher, writer, subject, year, published, number, price)
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Book edited successfully.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec_()
            self.book_id_edit = None
            self.lineEdit_9.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_10.setText('')
    
    # รีเฟรชหน้าการตั้งค่า
    def refresh_edit(self):
        self.change_tab(4)
    
    # เพิ่มรายการการตั้งค่า
    def add_to_edit(self):
        try:
            user_input = self.tableWidget_3.item(self.tableWidget_3.currentRow(),0).text()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            book = self.db.select_by_id(user_input)
            self.book_id_edit = book[0][0]
            self.lineEdit_9.setText(book[0][1])
            self.lineEdit_11.setText(book[0][2])
            self.lineEdit_10.setText(book[0][3])
            self.comboBox_2.setCurrentIndex(self.comboBox_2.findText(book[0][4], QtCore.Qt.MatchFixedString))
            self.spinBox_6.setValue(int(book[0][5]))
            self.spinBox_4.setValue(int(book[0][6]))
            self.spinBox_5.setValue(int(book[0][7]))
            self.doubleSpinBox_2.setValue(float(book[0][8]))
            
    # ฟังก์ชัน search_edit นี้ใช้สำหรับค้นหาข้อมูลหนังสือและแสดงผลในตาราง 
    def search_edit(self):
        user_input = self.lineEdit_8.text()
        # ตรวจสอบว่ามีการป้อนข้อมูลหรือไม่
        if user_input != '':
            books = self.db.search_book(user_input)
            if len(books) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No book found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            # ถ้าพบข้อมูลหนังสือ
            else:
                rowCount = len(books)
                self.tableWidget_4.setColumnCount(5)
                self.tableWidget_4.setRowCount(rowCount)
                self.tableWidget_4.setHorizontalHeaderLabels(['Id', 'Name', 'Publisher', 'Writer', 'Price'])
                # วนลูปเพื่อแสดงข้อมูลหนังสือในตาราง
                if len(books) != 0:
                    for i in range(len(books)):
                        for j in range(5):
                            if j == 4:
                                self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j+4])))
                            else:
                                self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j])))
                
                # ตารางจะพอดีกับหน้าจอแนวนอน
                self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
                self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    # ฟังก์ชันรีเฟรชข้อมูลหนังสือ
    def refresh_book(self):
        self.lineEdit.setText('')
        
        print(self.tableWidget_2.item(self.tableWidget_2.currentRow(),0).text())
        self.change_tab(0)
    
    # ฟังก์ชันค้นหาข้อมูลหนังสือ
    def search_book(self):
        user_input = self.lineEdit.text()
        if user_input != '':
            books = self.db.search_book(user_input)
            if len(books) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No book found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(books)
                self.tableWidget_2.setColumnCount(8)
                self.tableWidget_2.setRowCount(rowCount)
                self.tableWidget_2.setHorizontalHeaderLabels(['Name', 'Publisher', 'Writer', 'Subject', 'Year', 'Published', 'Number', 'Price'])
                for i in range(len(books)):
                    for j in range(8):
                        self.tableWidget_2.setItem(i, j, QTableWidgetItem(books[i][j+1]))
                
                # ตารางจะพอดีกับหน้าจอแนวนอน
                self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
                self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    # ฟังก์ชันเปลี่ยนแท็บที่กำหนด 
    def change_tab(self, index):
        
        # เปลี่ยนไปยังแท็บที่ 0
        if index == 0:
            rowCount = self.db.count_book()
            books = self.db.select_all_book()
            self.tableWidget_2.setColumnCount(8)
            self.tableWidget_2.setRowCount(rowCount)
            self.tableWidget_2.setHorizontalHeaderLabels(['Name', 'Publisher', 'Writer', 'Subject', 'Year', 'Published', 'Number', 'Price'])
            
            # ตรวจสอบว่ามีข้อมูลหนังสือมากกว่า 0 รายการ
            if len(books) != 0:
                for i in range(len(books)):
                    for j in range(8):
                        self.tableWidget_2.setItem(i, j, QTableWidgetItem(books[i][j+1]))
            
            # ตารางจะพอดีกับหน้าจอแนวนอน
            self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # เปลี่ยนไปยังแท็บที่ 1
        if index == 1:
            rowCount = self.db.count_book()
            books = self.db.select_all_book()
            self.tableWidget_4.setColumnCount(5)
            self.tableWidget_4.setRowCount(rowCount)
            self.tableWidget_4.setHorizontalHeaderLabels(['Id', 'Name', 'Publisher', 'Writer', 'Price'])
            # ตรวจสอบว่ามีข้อมูลหนังสือมากกว่า 0 รายการ
            if len(books) != 0:
                for i in range(len(books)):
                    for j in range(5):
                        # กรณีคอลัมน์ที่ 4 (j == 4) ปรับข้อมูลเป็น string ก่อนแสดงผล
                        if j == 4:
                            self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j+4])))
                        # กรณีคอลัมน์อื่นๆ แสดงผลตามปกติ
                        else:
                            self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j])))
           
            # ตารางจะพอดีกับหน้าจอแนวนอน
            self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # เปลี่ยนไปยังแท็บที่ 2
        if index == 2:
            loan = self.db.get_all_loan()
            rowCount = len(loan)
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setRowCount(rowCount)
            self.tableWidget.setHorizontalHeaderLabels(['Id', 'Name', 'User Id', 'Date', 'Days Gone By'])
            if len(loan) != 0:
                for i in range(len(loan)):
                    for j in range(5):
                        if j == 4:
                            date_format = '%Y-%m-%d %H:%M:%S.%f'
                            a = datetime.strptime(loan[i][j+1], date_format)
                            b = datetime.strptime(str(datetime.now()), date_format)
                            delta = b - a
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(delta.days)))
                        if j == 3:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(loan[i][j+2]))
                        else:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(loan[i][j])))
            
            # ตารางจะพอดีกับหน้าจอแนวนอน
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # เปลี่ยนไปยังแท็บที่ 4
        if index == 4:
            rowCount = self.db.count_book()
            books = self.db.select_all_book()
            self.tableWidget_3.setColumnCount(3)
            self.tableWidget_3.setRowCount(rowCount)
            self.tableWidget_3.setHorizontalHeaderLabels(['Id', 'Name', 'Writer'])
            if len(books) != 0:
                for i in range(len(books)):
                    for j in range(3):
                        if j == 2:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem(books[i][j+1]))
                        else:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(books[i][j])))
            
            # ตารางจะพอดีกับหน้าจอแนวนอน
            self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    # ฟังก์ชันการเพิ่มข้อมูลหนังสือในตาราง
    def add_book(self):
        name = self.lineEdit_2.text()
        publiser = self.lineEdit_3.text()
        writer = self.lineEdit_4.text()
        subject = self.comboBox.currentText()
        year = self.dateEdit.text()
        published = str(self.spinBox.text())
        number = str(self.spinBox_2.text())
        price = str(self.doubleSpinBox.text())
        if name == '' or publiser == '' or writer == '':
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("You must set information.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            self.db.add_book(name, publiser, writer, subject, year, published, number, price)
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Book added successfully.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec_()
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
        
# สร้างอินสแตนซ์ของ QApplication
app = QApplication(sys.argv)

# สร้างอินสแตนซ์ของคลาส LibManage
window = LibManage()

# รันแอปพลิเคชัน
app.exec_()