#VEHICLE PENALTY MANAGEMENT
import os
import mysql.connector
import datetime

now = datetime.datetime.now()
mydb = mysql.connector.connect(host="localhost", user="root", password="root")
mycursor = mydb.cursor()
sql = "CREATE database if not exists challan;"
mycursor.execute(sql)


def challan_mgmt():
    while True:
        print("\t\t\t 1. Add New challan")
        print("\t\t\t 2. List challan")
        print("\t\t\t 3. Update challan")
        print("\t\t\t 4. Delete challan")
        print("\t\t\t 5. Back (Main Menu)")
        p = int(input("\t\t Enter Your Choice :"))
        if p == 1:
            add_challan()
        if p == 2:
            search_challan()
        if p == 3:
            update_challan()
        if p == 4:
            delete_challan()
        if p == 5:
            break

def payment_mgmt():
    while True:
        print("\t\t\t 1. Add Payment")
        print("\t\t\t 2. List Payment")
        print("\t\t\t 3. List Month wise")
        print("\t\t\t 4. Back (Main Menu)")
        o = int(input("\t\t Enter Your Choice :"))
        if o == 1:
            add_payment()
        if o == 2:
            list_payment()
        if o == 3:
            month= int(input("Enter month number (1-12)"))
            list_month(month)
        if o == 4:
            break

def create_database():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    
    print("Creating CHALLAN table")
    sql = "CREATE TABLE if not exists challan(cid int(4) PRIMARY KEY,personname char(30) NOT NULL,penaltyamount float(8,2),vehiclenumber char(60));"
    mycursor.execute(sql)
    print("CHALLAN table created")
    print("Creating PAYMENT table")
    sql = "CREATE TABLE if not exists payment(paymentdate DATE,cid int(4) references challan(cid), paymentamount float(8,2));"
    mycursor.execute(sql)
    print("PAYMENT table created")
   


def list_database():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root",database="challan")
    mycursor = mydb.cursor()
    sql = "show tables;"
    mycursor.execute(sql)
    for i in mycursor:
        print(i)

        
def payment_updation(c,p):
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    sql = "UPDATE challan SET penaltyamount= penaltyamount- %s WHERE cid=%s;"
    val = (p,c)
    mycursor.execute(sql,val)
    mydb.commit()
    
def add_payment():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    now = datetime.datetime.now()
    sql = "INSERT INTO payment (paymentdate, cid, paymentamount) values (%s,%s,%s)"
    oid = now.year+now.month+now.day+now.hour+now.minute+now.second
    cid = int(input("Enter challan id : "))
    paymentamount = float(input("Enter payment amount: "))
    val = ( now, cid, paymentamount)
    mycursor.execute(sql, val)
    mydb.commit()
    payment_updation(cid,paymentamount)
    

def list_payment():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    sql = "SELECT * from payment"
    mycursor.execute(sql)
    print("\t  PAYMENT DETAILS")
    print("-"*35)
    print("paymentdate	cid	paymentamount")
    print("-" * 35)
    for i in mycursor:
        print(i[0], "\t", i[1], "\t", i[2])
    print("-" *35 )



def db_mgmt( ):
    while True:
        print("\t\t\t 1. Database creation")
        print("\t\t\t 2. List Database")
        print("\t\t\t 3. Back (Main Menu)")
        p = int(input("\t\t Enter Your Choice :"))
        if p == 1:
            create_database()
        if p == 2:
            list_database()
        if p == 3:
             break

def add_challan():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root",database="challan")
    mycursor = mydb.cursor()
    sql = "INSERT INTO challan(cid,personname,penaltyamount,vehiclenumber) values (%s,%s,%s,%s)"
    cid = int(input("\t\t Enter challan id :"))
    search = "SELECT count(*) FROM challan WHERE cid=%s;"
    val = (cid,)
    mycursor.execute(search,val)
    for x in mycursor:
        cnt = x[0]
    if cnt == 0:
        personname = input("\t\t Enter person name :")
        penaltyamount = int(input("\t\t Enter penalty amount :"))
        vehiclenumber = input("\t\t Enter vehicle number:")
        val = (cid,personname,penaltyamount,vehiclenumber)
        mycursor.execute(sql,val)
        mydb.commit()
    else:
        print("\t\t challan already exist")
        

def update_challan():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    cid = int(input("Enter the challan id :"))
    penaltyamount = int(input("Enter the penaltyamount :"))
    sql = "UPDATE challan SET penaltyamount=penaltyamount+%s WHERE cid=%s;"
    val = (penaltyamount,cid)
    mycursor.execute(sql,val)
    mydb.commit()
    print("\t\t Challan details updated")
 
def delete_challan():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor=mydb.cursor()
    cid = int(input("Enter the challan id :"))
    sql = "DELETE FROM challan WHERE cid = %s;"
    val = (cid,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount,"record(s) deleted");

def search_challan():
    while True:
        print("\t\t\t 1. List all penalties")
        print("\t\t\t 2. List challan id wise")
        print("\t\t\t 3. Back (Main Menu)")
        s = int(input("\t\t Enter Your Choice :"))
        if s == 1:
            list_penalty()
        if s == 2:
            cid=int(input(" Enter challan id :"))
            list_cid(cid)
        if s == 3:
            break

def list_penalty():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root",database="challan")
    mycursor = mydb.cursor()
    sql = "SELECT * from challan"
    mycursor.execute(sql)
    print("\t\t\t\t CHALLAN DETAILS")
    print("\t\t", "-" * 47)
    print("\t\t cid	person_name	penalty_amount  vehiclenumber")
    print("\t\t", "-" * 47)
    for i in mycursor:
        print("\t\t", i[0], "\t",i[1], "\t""\t",i[2], "\t", i[3])
    print("\t\t", "-" * 47)

def list_cid(cid):
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    sql = "SELECT * from challan WHERE cid=%s"
    val = (cid,)
    mycursor.execute(sql, val)
    print("\t\t\t\t CHALLAN DETAILS")
    print("\t\t", "-" * 47)
    print("\t\t cid	person_name	penalty_amount  vehiclenumber ")
    print("\t\t", "-" * 47)
    for i in mycursor:
        print("\t\t", i[0], "\t", i[1], "\t""\t", i[2], "\t", i[3])
    print("\t\t", "-" * 47)



def list_month(m):
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="challan")
    mycursor = mydb.cursor()
    print(m)
    sql="SELECT * from payment WHERE MONTH(paymentdate)=%s;"
    val = (m,)
    mycursor.execute(sql, val)
    clrscr()
    print("\t PAYMENT DETAILS")
    print("-"*37)
    print("month         pid       paymentdate")
    print("-"*37)
    for i in mycursor:
        print(i[0], "\t", i[1], "\t", i[2])
    print("-" * 37) 


 
def clrscr():
          print("\n"*5)

while True:
    clrscr()
    print("\t\t\t VEHICLE PENALTY MANAGEMENT")
    print("\t\t\t **************************\n")
    print("\t\t 1. CHALLAN MANAGEMENT")
    print("\t\t 2. PAYMENT MANAGEMENT")
    print("\t\t 3. DATABASE SETUP")
    print("\t\t 4. EXIT\n")
    n = int(input("Enter your choice :"))
    if n == 1:
        challan_mgmt()
    if n == 2:
        os.system('cls')
        payment_mgmt()
    if n == 3:
        db_mgmt()
    if n == 4:
        break
