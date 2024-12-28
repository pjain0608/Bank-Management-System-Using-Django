# Banking System with Money Transfer Feature

**Overview**

This project is a comprehensive web-based banking system developed using Django, HTML, CSS, and MySQL. It allows users to perform essential banking operations, including balance inquiry, account creation, deposit, withdrawal, and a robust money transfer feature. The money transfer functionality supports transfers via account number, mobile number, or email.

The system emphasizes user-friendly interfaces and secure data handling, making it suitable for learning, demonstration, or as a foundation for real-world banking applications.

# Features

1. **Account Management**
-  **Open Account** : Users can create a new account by providing essential details like aadhar number, name, email, mobile number, and an account number.
-  **Account Balance Inquiry** : Users can check the balance of their accounts by entering their account number and PIN.
-  **PIN Generation** - User have to generate PIN for banking operations

2. **Transactions**
-  **Deposit Money** : Allows users to credit funds to their accounts securely.
-  **Withdraw Money** : Enables users to debit funds from their accounts, ensuring that withdrawal does not exceed the account balance.

3. **Money Transfer**
-  **Transfer via Account Number**: Users can transfer money directly to another account by specifying the receiver's account number.
-  **Transfer via Mobile Number**: Users can transfer money using the receiver's registered mobile number.
-  **Transfer via Email**: Users can also initiate transfers by entering the receiver's email address

# Tech Stack Used

-  Backend Framework: Django (Python)
-  Frontend: HTML5, CSS3
-  Database: MySQL
-  Email Integration: SMTP for transaction notifications

# How it works
1. **Money Transfer Process**
-  The user selects the type of transfer (Account, Mobile, or Email).
-  Inputs details such as sender account number, PIN, amount, and receiver details.
-  The system validates the sender's account, PIN, and balance.
-  Upon validation, the amount is securely debited from the sender’s account and credited to the receiver’s account.
-  A confirmation email is sent to the receiver.

2. **Security Features**
-  PIN validation is implemented using an encrypted and decrypted mechanism to ensure user safety.
-  CSRF tokens are used in forms to prevent cross-site request forgery.
-  Validations are performed on inputs to minimize user errors and vulnerabilities.


# Project Structure
Project_Bank/ <br>
│ <br>
├── banking_app/ <br>
│   ├── migrations/ <br>
│   ├── templates/ <br>
│   │   ├── base.html <br>
│   │   ├── transfer.html <br>
│   ├── static/ <br>
│   │   ├── css/ <br>
│   │   │   ├── style.css <br>
│   ├── models.py <br>
│   ├── views.py <br>
│   ├── urls.py <br>
│ <br>
├── BankingSystem/ <br>
│   ├── settings.py <br>
│   ├── urls.py <br>
│ <br>
├── db.sqlite3 (or MySQL database configuration) <br>
├── manage.py <br>

# Future Enhancements

-  Add user authentication for enhanced security.
-  Include transaction history and account statements.
-  Implement a dashboard for users to manage accounts and view analytics.

# UI View
![Screenshot (28)](https://github.com/user-attachments/assets/2afe1269-39bd-428a-a276-aaca4fb876c7)
![Screenshot (29)](https://github.com/user-attachments/assets/2c0ece97-7752-43c2-a1c6-3862baf03845)
![Screenshot (30)](https://github.com/user-attachments/assets/c50072e3-d3c5-4d49-a5d7-93bac7c825a7)
![Screenshot (31)](https://github.com/user-attachments/assets/88310441-8de0-46bb-a621-2cd7db03de30)
![Screenshot (32)](https://github.com/user-attachments/assets/afaaebe5-21b7-48f8-be0e-567767ab5757)
![Screenshot (33)](https://github.com/user-attachments/assets/e54ce47d-78de-4917-8c86-a48a175af73c)
![Screenshot (34)](https://github.com/user-attachments/assets/4675f14f-ad60-48e6-81f6-1b537fda9c82)
![Screenshot (35)](https://github.com/user-attachments/assets/ac451a73-b13b-46d4-8c31-d7acb8cb8760)
