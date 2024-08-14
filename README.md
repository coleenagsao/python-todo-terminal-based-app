# TaskCLI: A CLI-based Todo App V1

## Description
TaskCLI is a terminal-based task listing application where user can create their own tasks with its corresponding deadlines and description. They are also given the option to assign such to a category of their own liking. User can create, edit, delete, and view all tasks and categories. User can also mark task as done, and add it to a category. By default, task upon creation are not assigned to a category.

## Technologies Used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![mySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

## Installation
To install the required packages, run the following command in your terminal:
- Python: `sudo apt install python3`
- Server: `sudo apt-get install -y mssql-server`
- Connector: `pip install mysql-connector-python`

  
## Usage
1. Open `main.py`
2. Inside the maria_db connection, change the password to the password of your root. The application shall access the taskrecordmanager user as a root. 

``` 
    mariadb_connection = mariadb.connect(
    host="localhost",
    user="root",                            
    password="<insert_your_pass_here>")
```
3. You are set to run the Python Program. Use `py main.py` to run.

## Execution Notes
- **Add, Edit Task**. the format of year, date, month must be yyyy, mm, dd, respectively. Prompts for month and day shall be displayed accordingly if not followed.
- **Edit Task**. Only the deadline will be editable. Other attributes such as name and description will no longer be subject to change.

## Screenshots

## Authors
- Agsao, Coleen Therese
- Dollesin, Samantha Shane
- Malahito, John Edver

## Additional Notes: 
This is the final project for CMSC 127 (Database) in UPLB.
  