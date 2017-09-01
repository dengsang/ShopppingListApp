# Shopping List


The innovative -----shopping list app----- is an application that  -----allows users  to record and share things they want to spend money on ----- meeting the needs of -----keeping track of their shopping lists -----.

##Features

Users create accounts
Users can log in
Users create, view, update and delete shopping lists.
Users can add, update, view or delete items in a shopping list

## Add the Travis CI badge to the README

https://travis-ci.org/dengsang/ShopppingListApp.svg?branch=master

## Add coveralls badge to the README

## MARKDOWN embed

[![Coverage Status](https://coveralls.io/repos/github/dengsang/ShopppingListApp/badge.svg?branch=master)](https://coveralls.io/github/dengsang/ShopppingListApp?branch=master)

**Installation**

 $ git clone https://github.com/dengsang/ShopppingListApp.git``````

**Creating and  activate virtual environment**nt

Download and install python.exe file from URL:https://www.python.org/
Download get-pip.py, being careful to save it as a .py file rather than .txt
Run this from the command prompt:
    python get-pip.py
    pip install virtualenv
    pip install virtualenvwrapper-win
    mkvirtualenv env_name
Activating virtual environment:
    Using terminal or cmd to navigate to where you will app will be stored, then
    run the following command: workon env_name

_Install  all the dependencies_ $ pip install -r requirements.txt

**Run application**

$ python app.py


**Description**
index(): - renders the homepage of the application.

db(self, user_obj): - used to check if the app user already has an app account,
                    if not he/she is added to users list.
                    
user_login(self, user_obj): - used to check user credentials before login basically  app user authentication

users = [] - List data structure that holds the shopping app users data

items = [] - List data structure that stores the data of items in the shopping list.

add_list(self, item_obj): - Checks if an item is already in shopping list before adding it.
                            if its not there it adds item to the shopping list.

delete_item(self, item_obj): Checks if an item is the shopping list and it deletes it if its there.

signup():- it renders the signup page and allow the shopping shopping app users to create an account.

dashboard(): - It renders the dashboard for the application where a user can add items to the shopping list.
             - It displays the shopping items of the app user.
             - It has a button that renders the adding items to the shopping list form
             - A user can log out at this position.
             
login(): - It renders the login form.
         - It control the access to the main service of the  Shopping application. 
         - Redirect the user to the dashboard if the user provide the correct credentials.
