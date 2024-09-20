Vougue_Vista

Project Overview
Vougue_Vista is a general-purpose e-commerce platform designed to offer a seamless shopping experience for both male and female fashion wears. Users can browse products, create an account, and order items with the option to pay on delivery. The platform is designed to be simple yet robust, leveraging modern web technologies for both frontend and backend development.

Technologies Used

Frontend:
HTML5: Structure and layout of the web pages.
CSS3: Styling and responsive design to ensure a seamless user experience across devices.
Backend:

Python (Flask): Flask is used for routing and handling server-side logic. It provides the flexibility and scalability needed for handling user requests and processing orders.
Flask-Login: Handles user authentication (sign-up, login, session management, etc.).
Jinja: A templating engine used to render dynamic data on the frontend by integrating with Flask.

Database:
SQLite: A lightweight relational database used to store structured data such as users, products, and orders.
SQLAlchemy: A powerful Object-Relational Mapping (ORM) tool for Python that simplifies interaction with the database, making it easy to perform CRUD operations.

Key Features

User Authentication:

Users can sign up for an account.
Login and session management through Flask-Login.
Passwords are securely hashed before storage.
Product Browsing:

Users can browse a wide selection of fashion items for both men and women.
Products are categorized for easy navigation.
Order Management:

Users can add items to their shopping cart.
Pay-on-delivery option available for all orders.
Orders are tracked and stored in the database for easy management by the admin.
Admin Panel:

Admins can add or remove products, update inventory, and manage user orders.
Ensures that the platform is up-to-date with the latest fashion offerings.
Responsive Design:

The platform is fully responsive, ensuring accessibility across different devices such as mobile phones, tablets, and desktops.