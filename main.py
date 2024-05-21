# Imports
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QDateEdit, QLineEdit
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np

from sys import exit

# Main class
class FitTrack(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.button_click()
        self.load_table()

    # Settings
    def settings(self):
        self.setWindowTitle("FitTrack")
        self.resize(800, 600)

    # init UI
    def initUI(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setDisplayFormat("yyyy-MM-dd")

        self.kal_box = QLineEdit()
        self.kal_box.setPlaceholderText("Calories burned")

        self.distance_box = QLineEdit()
        self.distance_box.setPlaceholderText("Enter Distance")

        self.description = QLineEdit()
        self.description.setPlaceholderText("Enter Description")

        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.submit_button = QPushButton("Submit")
        self.dark_button = QCheckBox("Dark Mode")
        self.light_button = QCheckBox("Light Mode")
        self.reset_button = QPushButton("Reset")
        self.clear_button = QPushButton("Clear")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Calories", "Distance", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Design our layout
        self.master_layout = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.sub_row1 = QHBoxLayout()
        self.sub_row2 = QHBoxLayout()
        self.sub_row3 = QHBoxLayout()
        self.sub_row4 = QHBoxLayout()

        self.sub_row1.addWidget(QLabel("Date:"))
        self.sub_row1.addWidget(self.date_box)

        self.sub_row2.addWidget(QLabel("Calories:"))
        self.sub_row2.addWidget(self.kal_box)

        self.sub_row3.addWidget(QLabel("Distance:"))
        self.sub_row3.addWidget(self.distance_box)

        self.sub_row4.addWidget(QLabel("Description:"))
        self.sub_row4.addWidget(self.description)

        self.col1.addLayout(self.sub_row1)
        self.col1.addLayout(self.sub_row2)
        self.col1.addLayout(self.sub_row3)
        self.col1.addLayout(self.sub_row4)
        self.col1.addWidget(self.dark_button)
        self.col1.addWidget(self.light_button)

        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()

        btn_row1.addWidget(self.add_button)
        btn_row1.addWidget(self.delete_button)
        btn_row2.addWidget(self.submit_button)
        btn_row2.addWidget(self.reset_button)
        btn_row2.addWidget(self.clear_button)

        self.col1.addLayout(btn_row1)
        self.col1.addLayout(btn_row2)

        self.col2.addWidget(self.canvas)
        self.col2.addWidget(self.table)

        self.master_layout.addLayout(self.col1, 30)
        self.master_layout.addLayout(self.col2, 70)
        self.setLayout(self.master_layout)
        
        self.apply_styles()
        self.load_table()

    # Events
    def button_click(self):
        self.add_button.clicked.connect(self.add_workout)
        self.delete_button.clicked.connect(self.delete_workout)
        self.submit_button.clicked.connect(self.calculate_calories)
        self.dark_button.stateChanged.connect(self.toggle_dark_mode)
        self.reset_button.clicked.connect(self.reset)
        self.clear_button.clicked.connect(self.clear)

    # Plot Graph
    def calculate_calories(self):
      distances = []
      calories = []
      query = QSqlQuery("SELECT distance, calories FROM fittrack ORDER BY calories ASC")
      while query.next():
        distances.append(query.value(0))
        calories.append(query.value(1))
        
      if not calories:
         QMessageBox.warning(self, "FitTrack", "No data available for calculation.")
         return

      try:
        min_calories = min(calories)
        max_calories = max(calories)
        
        if min_calories == max_calories:
            normalized_calories = [1] * len(calories)  # All values are the same, assign 1 to avoid division by zero
        else:
            normalized_calories = [(x - min_calories) / (max_calories - min_calories) for x in calories]

        plt.style.use("ggplot")
        ax = self.figure.subplots()
        scatter = ax.scatter(distances, calories, s=[100 * n for n in normalized_calories], c=normalized_calories, alpha=0.5, label="Data Points", cmap="viridis")

        ax.set_title("Calories burned vs Distance")
        ax.set_xlabel("Distance")
        ax.set_ylabel("Calories")
        ax.legend()
        self.figure.colorbar(scatter, ax=ax, label='Normalized Calories')
        self.canvas.draw()

      except ValueError as e:
        QMessageBox.warning(self, "FitTrack", f"Error: {e}")

    def apply_styles(self):
        self.setStyleSheet(""" 
                           
                           QWidget {
                            background-color: #b8c9e1;
                            color: #000;
                            }
                            
                            QPushButton {
                            background-color: #007bff;
                            color: #fff;
                            border-radius: 5px;
                            padding: 5px;
                            }
                            
                            QPushButton:hover {
                            background-color: #0056b3;
                            }
                            
                            QCheckBox {
                            color: #000;
                            }
                            
                            QTableWidget {
                            background-color: #fff;
                            color: #000;
                            }
                            
                            QTableWidget::item {
                            padding: 5px;
                            }
                            
                            QTableWidget::item:selected {
                            background-color: #007bff;
                            color: #fff;
                            }
                            
                            QHeaderView::section {
                            background-color: #007bff;
                            color: #fff;
                            padding: 5px;
                            }
                            
                            QHeaderView::section:checked {
                            background-color: #0056b3;
                            }
                            
                            QHeaderView::section:checked:disabled {
                            background-color: #007bff;
                            }
                            
                            QHeaderView::section:checked:hover {
                            background-color: #0056b3;
                            }
                            
                            QHeaderView::section:horizontal {
                            border: 0px;
                            }
                            
                            QHeaderView::section:vertical {
                            border: 0px;
                            }
                            
                            QHeaderView::section:horizontal:disabled {
                            border: 0px;
                            }
                            
                            QHeaderView::section:vertical:disabled {
                            border: 0px;
                            }
                            
                            QHeaderView::section:horizontal:hover {
                            background-color: #0056b3;
                            }
                            
                            QHeaderView::section:vertical:hover {
                            background-color: #0056b3;
                            }
                            
                            QHeaderView::section:horizontal:checked {
                            background-color: #007bff;
                            }
                            
                            QHeaderView::section:vertical:checked {
                            background-color: #007bff;
                            }
                            
                            QHeaderView::section:horizontal:checked:hover {
                            background-color: #0056b3;
                            }
                            
                            QHeaderView::section:vertical:checked:hover {
                            background-color: #0056b3;
                            }
                            
                            QTableWidgetItem {
                            padding: 5px;
                            }
                            
                            QDateEdit {
                            padding: 5px;
                            }
                            
                            QLineEdit {
                            padding: 5px;
                            }
                            
                            QCheckBox {
                            padding: 5px;
                            }
                            
                            QCheckBox::indicator {
                            width: 20px;
                            height: 20px;
                            }
                            
                            QCheckBox::indicator:checked {
                            background-color: #007bff;
                            }
                            
                           """)
        figure_color = "#b8c9e1"
        self.figure.patch.set_facecolor(figure_color)
        self.canvas.setStyleSheet(f"background-color: {figure_color};")
        
        
        
    # Load tables
    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery()
        query.exec_("SELECT * FROM fittrack ORDER BY date DESC")
        row_position = 0
        while query.next():
            id = query.value(0)
            date = query.value(1)
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(date)))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(calories)))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(distance)))
            self.table.setItem(row_position, 4, QTableWidgetItem(str(description)))
            row_position += 1

    # Add Tables
    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.text()
        distance = self.distance_box.text()
        description = self.description.text()

        if not calories or not distance or not description:
            QMessageBox.warning(self, "FitTrack", "Please fill in all fields")
            return

        query = QSqlQuery()
        query.prepare("INSERT INTO fittrack (date, calories, distance, description) VALUES (?, ?, ?, ?)")
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)

        if not query.exec_():
            QMessageBox.critical(self, "FitTrack", "Error: %s" % query.lastError().databaseText())
        else:
            self.load_table()

        self.date_box.setDate(QDate.currentDate())
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()
        self.load_table()

    # Delete Tables
    def delete_workout(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "FitTrack", "Please select a row to delete")
            return

        id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "FitTrack", "Are you sure you want to delete this workout?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM fittrack WHERE id = ?")
        query.addBindValue(id)
        
        if not query.exec_():
            QMessageBox.critical(self, "FitTrack", "Error: %s" % query.lastError().databaseText())
        else:
            self.load_table()
            
        self.load_table()
        
    
    # Submit Tables
    def submit_workout(self):
        pass

  
    # click event
  
    # Dark mode
    
    def toggle_dark_mode(self):
        self.apply_styles()
  
    # Light mode
    
    def toggle_light_mode(self):
        pass
    
    
    # Reset
    
    def reset(self):
        self.date_box.setDate(QDate.currentDate())
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()
        self.figure.clear()
        self.canvas.draw()
        
        
    
    # Clear
    
    def clear(self):
        self.table.setRowCount(0)
        query = QSqlQuery()
        query.exec_("DELETE FROM fittrack")
        self.load_table()
        
        
  
  
# Initialize my DB
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("fittrack.db")
if not db.open():
    QMessageBox.critical(None, "FitTrack", "Database Error: %s" % db.lastError().databaseText())
    exit(2)
    
query = QSqlQuery ()
query.exec_("""
            CREATE TABLE IF NOT EXISTS fittrack (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            calories INTEGER NOT NULL,
            distance REAL NOT NULL,
            description TEXT NOT NULL
            )
            
            
            """)
    



if __name__ == "__main__":
    app = QApplication([])
    main = FitTrack()
    main.show()
    app.exec_()
    exit()
    
  