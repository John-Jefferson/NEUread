# 📚 NEUread

NEUread is a desktop-based **library management and book borrowing system** developed for **New Era University (NEU)**. The system integrates **RFID-based authentication** with a **GUI application** to streamline book searching, borrowing, and transaction approval within the library.

The project is designed to improve efficiency, reduce manual errors, and provide a more secure and organized library experience for both students and administrators.

---

## 🚀 Features

### 🔍 Book Search

* Search books by **title, author, or category**
* Displays detailed book information
* Shows **availability status** in real time

### 🪪 RFID-Based Authentication

* **Admin RFID Scan** for transaction approval
* **User RFID Scan** for borrowing confirmation
* Ensures secure and authorized book transactions

### 👩‍💼 Admin Controls

* Approves or denies borrowing requests
* Monitors book availability
* Manages transaction flow

### 🖥️ User-Friendly Interface

* Built using **CustomTkinter**
* Clean and intuitive layout
* Designed for fast and easy navigation

---

## 🛠️ Technologies Used

* **Python** – Core programming language
* **CustomTkinter** – Graphical User Interface (GUI)
* **RFID Scanner (USB-based)** – User and admin authentication
* **Database (e.g., SQLite / MySQL)** – Book and user data storage

---

## 🔄 System Workflow

1. **Book Search** – User searches for a book in the system
2. **Admin RFID Scan** – Admin approves the transaction
3. **User RFID Scan** – Student confirms borrowing
4. **Transaction Recorded** – Book status is updated

## 📌 Requirements

* Python 3.9 or higher
* USB RFID Scanner
* Required Python libraries:

  * customtkinter
  * tkinter
  * sqlite3 / mysql-connector (depending on DB)

---

## ▶️ How to Run

1. Clone or download the project
2. Install required dependencies
3. Connect the RFID scanner via USB
4. Run the main application file:

```bash
python main.py
```

---

## 🎯 Purpose of the Project

NEUread was developed to:

* Modernize NEU’s library system
* Reduce manual book tracking
* Enhance security using RFID technology
* Improve user experience for students and librarians

---



## 👨‍🎓 Author

**John Jefferson Leonardo**
Grade 12 Student – New Era University

---

## 📄 License

This project is developed for educational purposes. All rights reserved.
