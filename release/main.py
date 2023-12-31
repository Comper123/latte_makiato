import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QTableWidgetItem, 
    QWidget, 
    QMessageBox
)
import sqlite3
import io


edit_template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>303</width>
    <height>262</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QWidget" name="gridLayoutWidget">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>10</y>
     <width>281</width>
     <height>201</height>
    </rect>
   </property>
   <layout class="QGridLayout" name="gridLayout">
    <item row="4" column="0">
     <widget class="QLabel" name="label_5">
      <property name="text">
       <string>цена</string>
      </property>
     </widget>
    </item>
    <item row="3" column="1">
     <widget class="QPlainTextEdit" name="description"/>
    </item>
    <item row="2" column="0">
     <widget class="QLabel" name="label_3">
      <property name="text">
       <string>молотый / в зернах</string>
      </property>
     </widget>
    </item>
    <item row="1" column="1">
     <widget class="QPlainTextEdit" name="status"/>
    </item>
    <item row="3" column="0">
     <widget class="QLabel" name="label_4">
      <property name="text">
       <string>описание вкуса</string>
      </property>
     </widget>
    </item>
    <item row="0" column="0">
     <widget class="QLabel" name="label">
      <property name="text">
       <string>название сорта</string>
      </property>
     </widget>
    </item>
    <item row="2" column="1">
     <widget class="QPlainTextEdit" name="moloti"/>
    </item>
    <item row="1" column="0">
     <widget class="QLabel" name="label_2">
      <property name="text">
       <string>степень обжарки</string>
      </property>
     </widget>
    </item>
    <item row="0" column="1">
     <widget class="QPlainTextEdit" name="name"/>
    </item>
    <item row="5" column="0">
     <widget class="QLabel" name="label_6">
      <property name="text">
       <string>объем упаковки</string>
      </property>
     </widget>
    </item>
    <item row="4" column="1">
     <widget class="QPlainTextEdit" name="price"/>
    </item>
    <item row="5" column="1">
     <widget class="QPlainTextEdit" name="volume"/>
    </item>
   </layout>
  </widget>
  <widget class="QPushButton" name="button">
   <property name="geometry">
    <rect>
     <x>180</x>
     <y>220</y>
     <width>111</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>PushButton</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


main_template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>610</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Coffee</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>60</y>
      <width>781</width>
      <height>511</height>
     </rect>
    </property>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>551</width>
      <height>31</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <item>
      <widget class="QPushButton" name="addbtn">
       <property name="text">
        <string>Добавить кофе</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="editBtn">
       <property name="text">
        <string>Редактировать кофе</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="deleteBtn">
       <property name="text">
        <string>Удалить кофе</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class AddCoffeeForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.main_window = False
        self.coffeeID = False
        self.initUI()
        self.show()
    
    def initUI(self):
        pass
    
    def setID(self, ID):
        self.coffeeID = ID

    def set_main(self, window):
        self.main_window = window   

    # Метод проверяющий на изменение кофе
    def get_editing_verdict(self):
        if self.name.toPlainText() and \
           self.status.toPlainText() and \
           self.moloti.toPlainText() and \
           self.description.toPlainText() and \
           self.price.toPlainText() and \
           self.volume.toPlainText():
            return True
        else:
            return False
    
    def update_values(self):
        query = """SELECT * from coffee WHERE id == """ + self.coffeeID
        data = self.main_window.do_query(query)[0]
        self.name.setPlainText(data[1])
        self.status.setPlainText(str(data[2]))
        self.moloti.setPlainText(data[3])
        self.description.setPlainText(data[4])
        self.price.setPlainText(str(data[5]))
        self.volume.setPlainText(str(data[6]))

    def create_coffee(self):
        if self.get_editing_verdict():
            name = self.name.toPlainText()
            status = self.status.toPlainText()
            moloti = self.moloti.toPlainText()
            description = self.description.toPlainText()
            price = self.price.toPlainText()
            volume = self.volume.toPlainText()
            # Делаем запрос к бд и вносим изменения
            query = f"""
            INSERT into coffee
            ('название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки')
            VALUES ('{name}', {status}, '{moloti}', '{description}', {price}, {volume})
            """
            self.main_window.do_query(query)
            self.main_window.update_table(self.main_window.do_query())
            self.close()
        
    def edit_coffee(self):
        if self.get_editing_verdict():
            name = self.name.toPlainText()
            status = self.status.toPlainText()
            moloti = self.moloti.toPlainText()
            description = self.description.toPlainText()
            price = self.price.toPlainText()
            volume = self.volume.toPlainText()
            # Формируем запрос
            query = f"""
            UPDATE coffee
            SET 'название сорта' = '{name}', 
            'степень обжарки' = {status}, 
            'молотый/в зернах' = '{moloti}', 
            'описание вкуса' = '{description}',
            'цена' = {price},
            'объем упаковки' = {volume}
            WHERE ID = {self.coffeeID}
            """
            # Изменяем в бд фильм
            self.main_window.do_query(query)
            # Обновляем таблицу после применения изменений в бд с помощью метода главног класса
            self.main_window.update_table(self.main_window.do_query())
            self.close()
            

class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(main_template)
        uic.loadUi(f, self)
        self.InitUI()
    
    def InitUI(self):
        self.update_table(self.do_query())
        self.addbtn.clicked.connect(self.addCoffee)
        self.editBtn.clicked.connect(self.editCoffee)
        self.deleteBtn.clicked.connect(self.deleteCoffee)
    
    def do_query(self, query="SELECT * from coffee"):
        res = ''
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        if 'SELECT' in query:
            res = cur.execute(query).fetchall()
        else:
            cur.execute(query)
            con.commit()
        con.close()
        if res:
            return res

    def update_table(self, data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        labels = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса',
                  'цена', 'объем упаковки']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        for row in range(len(data)):
            for column in range(len(data[0])):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

    def addCoffee(self):
        # При нажатии на кнопку инициализируем обьект клааса создания кофе
        self.add_coffee_widget = AddCoffeeForm()
        # Устанавливаем объект основного класса
        self.add_coffee_widget.set_main(self)
        # Добавляем название нашему окну
        self.add_coffee_widget.setWindowTitle("Добавить кофе")
        # Задаем название кнопке в окне
        self.add_coffee_widget.button.setText("Добавить")
        # Подключаем функцию добавления кофе
        self.add_coffee_widget.button.clicked.connect(self.add_coffee_widget.create_coffee)

    def editCoffee(self):
        row = self.tableWidget.currentRow()
        ID = self.tableWidget.item(row, 0).text
        print(ID)
        if ID is not None:
            Id = ID.text()
            # Инициализимруем объект класса окна изменения кофе
            self.edit_coffee_widget = AddCoffeeForm()
            # Задаем название нашему окну
            self.edit_coffee_widget.setWindowTitle("Редактировать кофе")
            # Изменяем значение надписи кнопки
            self.edit_coffee_widget.button.setText("Редактировать")
            # Устанавливаем объект основного класса
            self.edit_coffee_widget.set_main(self)
            # устанавливаем id того кофе который редактируем
            self.edit_coffee_widget.setID(Id)
            # Обновляем значения окна так как мы редактируем существующий кофе
            self.edit_coffee_widget.update_values()
            # Подключаем функцию редактирования кофе
            self.edit_coffee_widget.button.clicked.connect(self.edit_coffee_widget.edit_coffee)
    
    def deleteCoffee(self):
        if self.tableWidget.selectedIndexes():
            # ID выбранных ячеек
            rows = [i.row() for i in self.tableWidget.selectedIndexes()]
            selected_id = list(set(map(int, [self.tableWidget.item(index, 0).text() for index in rows])))
            ids = ", ".join(map(str, sorted(selected_id)))
            question = QMessageBox.question(
                self, 
                "Удалить выбранные сорта кофе?", 
                "Действительно удалить элементы с id " + ids, 
                QMessageBox.Yes | QMessageBox.No
            )
            # Если выбрали действительно удалить кофе делаем запрос к бд
            if question == QMessageBox.Yes:
                query = f"""
                DELETE from coffee
                WHERE ID in ({ids})
                """
                self.do_query(query)
                # Обновляем таблицу кофе
                self.update_table(self.do_query())
            else:
                return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    espresso = Espresso()
    espresso.show()
    sys.exit(app.exec())