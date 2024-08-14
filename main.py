import mysql.connector as mariadb
import datetime

# establish connection to root
mariadb_connection = mariadb.connect(
    host="localhost",
    user="root",
    password="password"
)
mycursor = mariadb_connection.cursor(buffered=True)

# create database if it does not already exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS taskmanager")

# use newly created database
mycursor.execute("USE taskmanager")

# create table "category"
mycursor.execute("CREATE TABLE IF NOT EXISTS category (categoryid INT(3) AUTO_INCREMENT, categoryname VARCHAR(30) NOT NULL, categorydescription VARCHAR(50), CONSTRAINT category_categoryid_pk PRIMARY KEY (categoryid))")

# create table "task"
mycursor.execute("CREATE TABLE IF NOT EXISTS task (taskid INT(3) AUTO_INCREMENT, taskname VARCHAR(30) NOT NULL, taskdescription VARCHAR(50), status ENUM('Done', 'Not Done') DEFAULT 'Not Done', deadline DATE, categoryid INT(3), CONSTRAINT task_taskid_pk PRIMARY KEY(taskid), CONSTRAINT task_categoryid_fk FOREIGN KEY(categoryid) REFERENCES category(categoryid))")

# Menu 
def mainMenu():
	print('''\n*********** TASKLY MAIN MENU ***************
Task Options
    [1] Add a task
    [2] Edit task
    [3] Delete task
    [4] View all tasks
    [5] Mark task as 'Done'
Category Options
    [6] Add category
    [7] Edit category
    [8] Delete category
    [9] View all categories
    [10] Add a task to category
Others
    [0] Exit''')

	global selection

def addTask(): #function that asks user for task name, description, and its deadline. Status will be 'Not Done' as a default
    print("\n*************** ADD A TASK ****************")
    
    name = input("Name : ")                                     #ask user for task name and its description
    description = input("Description : ")
    
    print("Deadline:")                                          #ask user for deadline year, month, and day
    while(True):
        try:
            year = int(input("Enter a year (yyyy): "))
            while(True):
                month = int(input("Enter a month (mm): "))
                if(month > 0 and month <= 12 ): break           #checks if month is in proper format
                else: print("Invalid month number!")
            while(True):
                day = int(input("Enter the day (dd): "))        #check if input is in correct day range depending on month
                if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
                    if(day > 0 and day <= 31): break
                    else: print("Invalid day input!")
                elif(month == 4 or month == 6 or month == 9 or month == 11):
                    if(day > 0 and day <= 30): break
                    else: print("Invalid day input!")
                else:
                    if((year%4) == 0):                            #loop year
                        if(day > 0 and day <= 29): break
                        else: print("Invalid day input!")
                    else:
                        if(day > 0 and day <= 28): break
                        else: print("Invalid day input!")
            break
        except Exception:
            print("Invalid Date Input")
    
    deadline = datetime.date(year,month,day)
    sql_statement = 'INSERT INTO task (taskname,taskdescription,status,deadline,categoryid) VALUES (%s,%s,"Not Done",%s,NULL)'
    val = (name,description,deadline)
    mycursor.execute(sql_statement,val)
    mariadb_connection.commit()

def editTask(): #function that lets user edit the deadline of the task
    print("\n*************** EDIT A TASK ****************")
    mycursor.execute("SELECT * FROM task LIMIT 1")
    if not mycursor.fetchone():                                             # check if table 'task' is empty before proceeding
        print("\nThere are no tasks to edit. Try creating one first.\n")    # if it is, display a prompt informing the user that they do not have any task
    else:   
        print("Tasks:")                                                     # otherwise, print a list of all the tasks available for editing, showing its task id and task name             
        mycursor.execute("SELECT * FROM task") 
        for i in mycursor:
            print("["+str((i[0]))+"] "+ i[1])
        mycursor.fetchall()

        while(True):
            try:
                id = int(input("Enter the ID : "))                          # ask the user to input the ID of the tas they want to edit
                break
            except Exception:                                               # in the event that the user inputs a character instead of an integer, catch that error and ask for input again
                print("Invalid Choice!")
                
        checker = False                                                     # check whether the ID input is actually in the list of available tasks
        mycursor.execute("SELECT * FROM task")
        for x in mycursor:
            if(x[0] == id):
                checker = True
                break
        mycursor.fetchall()

        if(checker):                                                         # if it is and the input is valid, proceed with the editing
            print("-- Edit Deadline --")
            while(True):
                try:                                                         
                    year = int(input("Enter a year (yyyy): "))               # ask for the year of the new deadline
                    while(True):
                        month = int(input("Enter a month (mm): "))           # ask for the month of the new deadline
                        if(month > 0 and month <= 12 ): break                # input should be within integers 1-12
                        else: print("Invalid month number!")
                    while(True):
                        day = int(input("Enter the day (dd): "))             # ask for the day of the new deadline  
                        if(month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):       # the day input should be within the actual range of dates available depending on the month input
                            if(day > 0 and day <= 31): break
                            else: print("Invalid day input!")
                        elif(month == 4 or month == 6 or month == 9 or month == 11):
                            if(day > 0 and day <= 30): break
                            else: print("Invalid day input!")
                        else:
                            if((year%4) == 0):
                                if(day > 0 and day <= 29): break
                                else: print("Invalid day input!")
                            else:
                                if(day > 0 and day <= 28): break
                                else: print("Invalid day input!")
                    break
                except Exception:                                             # if at any moment, the user inputs a character instead of an integer, inform them that the input is invalid and ask for the date again starting from the year input.
                    print("Invalid Date Input")

            deadline = datetime.date(year,month,day)                          
            sql_statement = "UPDATE task SET deadline=%s WHERE taskid=%s"
            val = (deadline,id)
            mycursor.execute(sql_statement,val)                               # update the task and set the deadline = the new deadline
            mariadb_connection.commit()                                       # commit changes
        else:
            print("\nInvalid Input id!\nPlease try again\n")                  # else if the ID was not found, inform the user and ask for input until valid
            editTask()

def deleteTask(): #function that allows the user to delete a task given the task ID
    print("\n*************** DELETE A TASK ****************")

    mycursor.execute("SELECT * FROM task LIMIT 1")
    if not mycursor.fetchone():                                                 # check whether table 'task' is empty before proceeding
        print("\nThere are no tasks to delete. Try creating one first.\n")      # if it is, print a prompt informing the user that they do not have tasks to delete
    else:  
        while (1):
            print("Tasks:")                                                     # else, print a list of tasks that they have, showing the task ID and the task name
            mycursor.execute("SELECT * FROM task")
            for row in mycursor:
                print("["+str((row[0]))+"] "+ row[1])                                                     
              
            while(True):
                try:
                    delete = int(input("Enter choice: "))                       # ask the user to choose which task to delete by entering the task ID
                    break
                except Exception:
                    print("Invalid Choice")   
            
            found = False
            mycursor.execute("SELECT * FROM task")
            for row in mycursor:                                                # check whether the ID input is actually in the available list of tasks to delete
                if delete == row[0]: found = True
            if found == True: break                                             # if it is found and the input is valid, proceed with the deletion
            else: print("\nInvalid Input ID!\nPlease try again\n")              # else if the ID was not found, print a prompt telling the user that their input is invalid and ask for input again until they enter a valid one
        mycursor.execute("DELETE FROM task WHERE taskid = "+ str(delete))       # using the same user input for the query, we proceed with the deletion
        mariadb_connection.commit()                                             # commit changes
        print("\nTask "+str(delete)+" successfully deleted.")                   # display a prompt informing the user that the task has been deleted successfully

def viewAllTask(): #function that displays all the current tasks inputted by user
    print("\n********************* TASKS ********************")
    mycursor.execute("SELECT * FROM task")
    for row in mycursor:
        print("[" + str(row[0]) + "] "  + row[1] + " | " + row[2] + " | " + row[3] + " | " + str(row[4]) + " | " + str(row[5]))

def markTask(): #function that asks user for id of task to be marked as done
    print("\n*************A** MARK TASK AS DONE ****************")
    mycursor.execute("SELECT * FROM task LIMIT 1")
    if not mycursor.fetchone():
        print("\nThere are no tasks to mark as done. Try creating one first.\n")
    else:
        print("Tasks:")                                             #display tasks in the system
        mycursor.execute("SELECT * FROM task")
        for row in mycursor:
            print("[" + str(row[0]) + "] "  + row[1] + " - " + row[3])
        mycursor.fetchall()
        
        while(True):
            try:
                id = int(input("\nEnter task id of item you want to mark as done: "))
                break
            except Exception:
                print("Invalid Choice") 
        
        checker = False                                               #initialize checker and status
        status = ""
        
        mycursor.execute("SELECT * FROM task")                        #check if task id exists
        for x in mycursor:
            if(x[0] == id):                                           #if yes, checker = true and status is saved
                checker = True
                status = x[3]
                break
        mycursor.fetchall()

        if(checker):                                                   #if task id found, check if status is not done
                if (status == "Not Done"):                             #if not done, update status as done
                    mycursor.execute("UPDATE task SET status=\'Done\' WHERE taskid=" + str(id)) 
                    mariadb_connection.commit()
                    print("\nThe task is successfully marked as done!")
                else:                                                  #if already marked done, a prompt shall appear
                    print("\nThe task is already marked as done before!")
        else:                                                         #if task id not found, display choices again
            print("\nInvalid Input ID!\nPlease try again\n")
            markTask()

def addCategory(): #function that lets user add category
    print("\n*************** ADD CATEGORY ***************")
    category_name = input("Category Name: ")
    category_desc = input("Category Description: ")

    #insert into the category table
    mycursor.execute("INSERT INTO category (categoryname, categorydescription) VALUES (%s, %s)", (category_name, category_desc))
    mariadb_connection.commit()

    print("\nSuccessfully added category " + category_name +"!\n")

def editCategory(): #function that allows the user to edit the category name of a chosen category
    print("************** EDIT CATEGORY **************\n")

    mycursor.execute("SELECT * FROM category LIMIT 1")
    if not mycursor.fetchone():                                                     # check whether table 'category' is empty before proceeding                  
        print("\nThere are no categories to edit. Try creating one first.\n")       # if it is, display a prompt informing the user that they dont have any categories to edit
    else:
        print("Categories:")                                                        # else, show the user a list of all the categories available for editing
        mycursor.execute("SELECT * FROM category")
        for i in mycursor:
           print("["+str((i[0]))+"] "+ i[1])
        mycursor.fetchall()
        
        while(True):                                                                
            try:
                id = int(input("Enter the ID : "))                                  # ask the user to input the ID of the category they want to edit
                break
            except Exception:                                                       # in the event that the user inputs a character instead of an integer, catch that error and ask for input again
                print("Invalid ID")
        
        checker = False                                                             # check whether the ID input is actually in the list of available categories
        mycursor.execute("SELECT * FROM category")
        for x in mycursor:
            if(x[0] == id):
                checker = True
                break
        mycursor.fetchall()

        if(checker):                                                                # if it is and the input is valid, proceed with the editing
            print("----- Edit Category name -----")
            category_name = input("Category Name : ")                               # ask for new category name 
            sql_statement = "UPDATE category SET categoryname=%s WHERE categoryid=%s"
            val = (category_name,id)
            mycursor.execute(sql_statement,val)                                     # update the category and set categoryname = the input
            mariadb_connection.commit()                                             # commit changes
        else:
            print("\nInvalid Input id!\nPlease try again\n")                        # else if the ID was not found, inform the user and ask for input until valid
            editCategory()

def deleteCategory(): #function that allows the user to delete a certain category given the categoryID
    print("************** DELETE A CATEGORY **************")

    mycursor.execute("SELECT * FROM category LIMIT 1")
    if not mycursor.fetchone():                                                             # check whether table 'category' is empty                          
        print("\nThere are no categories to delete. Try creating one first.\n")             # if it is, print a prompt informing the user that they do not have categories to delete
    else:
        while (1):
            print("Categories:")                                                            # else, print a list of categories that they have, showing the category ID and the category name
            mycursor.execute("SELECT * FROM category")
            for row in mycursor:
                print("["+str((row[0]))+"] "+ row[1])            
            while(True):
                try:
                    delete = int(input("Enter category ID of item you want to delete: "))   # ask the user to choose which category to delete by entering the category ID
                    break
                except Exception:
                    print("Invalid Choice!")                                                # in the event that the user tries to input a character instead of an integer, catch that error and ask for another input
            found = False
            mycursor.execute("SELECT * FROM category")
            for row in mycursor:                                                            # check whether the ID input is actually in the available list of categories to delete
                if delete == row[0]: found = True
            if found == True: break                                                         # if it is found and the input is valid, proceed with the deletion
            else: print("\nInvalid Input ID!\nPlease try again\n")                          # else, print a prompt telling the user that their input is invalid and ask for input again until they enter a valid one

        mycursor.execute("UPDATE task SET categoryid = NULL WHERE categoryid= "+ str(delete))       # set the categoryid of the tasks in the category to delete to NULL
        mycursor.execute("DELETE FROM category WHERE categoryid = "+ str(delete))           # using the same user input for the query, proceed with the deletion
        mariadb_connection.commit()                                                         # commit changes
        print("Category "+str(delete)+" successfully deleted.\n")                           # display a prompt informing the user that the task has been deleted successfully

def viewAllCategory(): #function that displays all categories existing
    print("\n*************** CATEGORIES ****************")
    mycursor.execute("SELECT * FROM category")
    for row in mycursor:
        print("[" + str(row[0]) + "] " + row[1] + " (" + row[2] + ")")      # display in format [id] category name (description)f viewAllCategory():

def addTasktoCategory(): #function that updates the category of a task chowsen
    print("\n************** ADD TASK TO YOUR CATEGORY ****************")
    mycursor.execute("SELECT * FROM task LIMIT 1")
    if not mycursor.fetchone():                                       #checks if there is an existing task/s first
        print("\nYou have no tasks. Try creating one first.\n")
    else:                                                             #if there is, check if there are existing category/ies
        mycursor.execute("SELECT * FROM category LIMIT 1")
        if not mycursor.fetchone():
            print("\nThere are currently no categories to add tasks to. Try creating one first.\n")
        else:                                                        #if there are tasks and categories
            print("Tasks:")                                          #display all tasks existing
            mycursor.execute("SELECT * FROM task")
            for i in mycursor:
                print("["+str((i[0]))+"] "+ i[1])
            mycursor.fetchall()
            
            while(True):    
                try:                                                #try-catch assures the input is an integer
                    task_id = int(input("Enter the Task ID : "))    #ask user of the task ID of task they want to edit
                    break
                except Exception:
                    print("Invalid Input")
            
            checker_taskid = False                                  #initializes variable as first to signal if task exists
            mycursor.execute("SELECT * FROM task")
            for x in mycursor:
                if(x[0] == task_id):                                #if tasks exist, checker_task id is true
                    checker_taskid = True                           
                    break
            mycursor.fetchall()

            if(checker_taskid):                              #if checker_task is true, adding to category will be the next step
                print("Task id found")
                while(True):
                    print("Categories:")                    #print all categories
                    mycursor.execute("SELECT * FROM category")
                    for i in mycursor:
                        print("["+str((i[0]))+"] "+ i[1])
                    mycursor.fetchall()

                    while(True):
                        try:
                            category_id = int(input("Enter the Category ID : ")) #ask user for the category id of task
                            break
                        except Exception:
                            print("Invalid Input")

                    checker_categoryid = False                      #check if category id exists
                    
                    mycursor.execute("SELECT * FROM category")
                    for x in mycursor:
                        if(x[0] == category_id):
                            checker_categoryid = True               #if existing, update the category id and task id
                            break
                    mycursor.fetchall()
                    if(checker_categoryid):
                        sql_statement = "UPDATE task SET categoryid=%s WHERE taskid=%s"
                        val = (category_id,task_id)
                        mycursor.execute(sql_statement,val)
                        mariadb_connection.commit()
                        print("\nSuccessfully added Task to Category!\n")
                        break
                    else: 
                        print("Category ID not found!")
            else:
                print("\nTask id not found\nPlease try again!\n")
                addTasktoCategory()

while True:
    mainMenu()
    while(True):
        try:
            selection = int(input("\nEnter your choice : "))
            break
        except Exception:
            print("Invalid Choice")
    if(selection == 0):
        print("Thank you! Bye")
        mariadb_connection.close()
        mycursor.close()
        break
    elif(selection == 1):
        addTask()
    elif(selection == 2):
        editTask()
    elif(selection == 3):
        deleteTask()
    elif(selection == 4):
        viewAllTask()
    elif(selection == 5):
        markTask()
    elif(selection == 6):
        addCategory()
    elif(selection == 7):
        editCategory()
    elif(selection == 8):
        deleteCategory()
    elif(selection == 9):
        viewAllCategory()
    elif(selection == 10):
        addTasktoCategory()
    else:
        print("Invalid input! Try again!")