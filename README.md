# Task Record System Version 1.0

### Project Description
- Task Record System is a terminal-based task listing application where user can create their own tasks with its corresponding deadlines and description. They are also given the option to assign such to a category of their own liking. 
- User can create, edit, delete, and view all tasks and categories. User can also mark task as done, and add it to a category. By default, task upon creation are not assigned to a category.

### Technologies Used
- Python
- SQL

### Setting Up
1. Install Python: `sudo apt install python3`
2. Install Server: `sudo apt-get install -y mssql-server`
2. Install Connector: `pip install mysql-connector-python`

  
### Running
1. Open `main.py`
2. Inside the maria_db connection, change the password to the password of your root. The application shall access the taskrecordmanager user as a root. 

``` 
    mariadb_connection = mariadb.connect(
    host="localhost",
    user="root",                            
    password="<insert_your_pass_here>")
```
3. You are set to run the Python Program. Use `py main.py` to run.

### Execution Notes
- **Add, Edit Task**. the format of year, date, month must be yyyy, mm, dd, respectively. Prompts for month and day shall be displayed accordingly if not followed.
- **Edit Task**. Only the deadline will be editable. Other attributes such as name and description will no longer be subject to change.

### Additional Notes (CMSC 127 - ST2L): 
- This is the final project for CMSC 127 (Database).
- Authors:
  - Agsao, Coleen Therese
  - Dollesin, Samantha Shane
  - Malahito, John Edver