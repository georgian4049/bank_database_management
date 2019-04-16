from __future__ import print_function
import pymysql
from prettytable import PrettyTable
import datetime

t=PrettyTable()
con = pymysql.connect('localhost','root','','bank')
cur=con.cursor()
def lines():
	for i in range(0,200):
		print("-",end="")
		if(i is "\n"):
			exit()
	print()	



def signup():
	count=0
	first_name=input("enter first name\n")
	last_name=input("enter last name\n")
	dob=input("enter dob\n")
	address=input("enter address\n")
	email=input("enter email\n")
	acct_type=input("enter account type\n")
	contact_no=int(input("enter contact no\n"))

	dob_split=dob.split('-')
	password=''
	for a in dob_split:
		password=password+a
	account_no=password+str(contact_no)	
	cur.execute("SELECT `acct_no` from `user` where `acct_no`=(%s)",(account_no))
	con.commit()
	count=cur.fetchall()
	if(len(count)!=0):
		print("account already exist")
		print(count)
	else:
		if(acct_type=='current'):
			amt=float(input("enter the amount to be deposited>5000\t:\t"))
			while(amt<5000):
				print("\nvalue is lesser than 5000")
				amt=float(input("enter the amount to be deposited>5000\t:\t"))
		elif(acct_type=="savings" or acct_type=="saving"):
			acct_type="savings"
			amt=float(input("\nenter the amount to be deposited. u can deposit later also :)\n"))		
		else:
			print("there is no such kind of account  type")
			
		cur.execute('INSERT INTO `user` (`first_name`,`last_name`,`dob`,`address`,`email`,`acct_no`,`password`,`account_type`,`contact_no`,`balance`,`date`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(first_name,last_name,dob,address,email,account_no,password,acct_type,contact_no,amt,datetime.datetime.now(),'open') )
		cur.execute('INSERT INTO `transaction` (`from`,`to`,`date`,`deposit`) VALUES (%s,%s,%s,%s)',(account_no,account_no,datetime.datetime.now(),amt) )
		con.commit()
		print("\naccount created successfully. Ur account no is\t:\t ",account_no)
	

def login():
	print("welcome back\n")
	account_no=input("enter account_no\n")
	
	cur.execute("SELECT * from `user` where `acct_no` =(%s)",(account_no))
	con.commit()
	data=cur.fetchall()
	password=input("enter password\n")
	if(data[0][0]!=account_no):
		print("wrong account no")
		for i in range(0,80):
			print("-")
			exit()

	elif(data[0][1]!=password):
		print("wrong password")
	if((data[0][0]==account_no and data[0][1]==password) and data[0][11]=="open"):
		home(account_no)
	else:
		print("account closed")
		for i in range(0,80):
			print("-",end="")
		print()	
		exit()

	

def home(a):
	account_no=a
	print("welcome back")
	cur.execute("SELECT * from `user` where `acct_no` =(%s)",(account_no))
	con.commit()
	data=cur.fetchall()

	while(1):
		opt=int(input("1. change password\n 2.deposit money \n 3. withdraw money\n 4. transfer money\n 5. print passbook \n 6. account closure\n 7. change address \n 8. customer logout \n "))
		if(opt==1):
			new_password=input("\nenter new password\t:\t")
			cnf_password=input("\nconfirm password\t:\t")
			while(new_password!=cnf_password):
				print("new and confirm passwords are different\n")
				new_password=input("\nenter new password\t:\t")
				cnf_password=input("\nconfirm password\t:\t")
				
			cur.execute("UPDATE `user` set `password`=(%s) where `acct_no` =(%s)",(new_password,account_no))
			con.commit()
			print("password updated successfully")
		elif(opt==7):
			new_address=int(input("\nenter new address"))		
			cur.execute("UPDATE `user` set `address`=(%s) where `acct_no` =(%s)",(new_address,account_no))
			con.commit()
			print("address updated successfully")	
		elif(opt==2):
			deposit=int(input("enter the money to be deposited\t:",end=""))
			while(deposit<=0):
				print("this sum cannot be deposited")
				deposit=int(input("enter the money to be deposited\t:",end=""))
			new_bal=data[0][9]+deposit	
			cur.execute("UPDATE `user` set `balance`=(%s) where `acct_no` =(%s)",(new_bal,account_no))
			cur.execute('INSERT INTO `transaction` (`from`,`to`,`date`,`deposit`) VALUES (%s,%s,%s,%s)',(account_no,account_no,datetime.datetime.now(),deposit) )
			con.commit()
			print("\t\tmoney deposited\t:",deposit)
			print("\t\tcurrent balance\t:",new_bal)
			print()
		elif(opt==3):
			withdraw=int(input("enter the money to be withdrawl\t:",end=""))
			while(withdraw<=0):
				print("this sum cannot be withdrawl")
				withdraw=int(input("enter the money to be withdrawl\t:",end=""))
			new_bal=data[0][9]-withdraw
			if(new_bal<5000 and data[0][6]=="current"):
				print("\tthis withdrawl cannot be done as it will cross minimum limit\n")
				print("\t your current balance is ",data[0][9])
				home(account_no)
			cur.execute("UPDATE `user` set `balance`=(%s) where `acct_no` =(%s)",(new_bal,account_no))
			cur.execute('INSERT INTO `transaction` (`from`,`to`,`date`,`withdrawl`) VALUES (%s,%s,%s,%s)',(account_no,account_no,datetime.datetime.now(),withdraw) )
			con.commit()	
		elif(opt==4):
			to=int(input("enter the account where money to be sent\n"))
			cur.execute("SELECT `first_name`,`last_name` from `user` where `acct_no` =(%s)",(to))
			con.commit()
			name=cur.fetchall()
			if(len(data)==0):
				print("no such account exist. please check it. thank you \n")
			else:
				transferred=int(input("enter the money to be transferred"))
				while(transferred<=0):
					print("this sum cannot be transferred")
					transferred=int(input("enter the money to be transferred"))
				while(transferred<=0):
					print("this sum cannot be transferred")
					transferred=int(input("enter the money to be transferred"))	
				
				while((data[0][9]-transferred)<0):
					print("u cannot transfer this amount . ur account balance is ",data[0][9])	
				new_bal=data[0][9]-transferred	
				cur.execute("UPDATE `user` set `balance`=(%s) where `acct_no` =(%s)",(new_bal,account_no))
				cur.execute('INSERT INTO `transaction` (`from`,`to`,`date`,`withdrawl`) VALUES (%s,%s,%s,%s)',(account_no,to,datetime.datetime.now(),transferred))
				con.commit()
				print("you transferred Rs.",transferred,"to",name[0][0]+" "+name[0][1],"\n" )
				print("your new updated balance is \t",new_bal,"\n","thank you")


		elif(opt==5):
			bal_updating=0
			print("\t\tPrinting Passbook")
			print()
			print("\t\tTotal balance : ",data[0][9])
			cur.execute("SELECT * from `transaction` where `from`=(%s) or `to`=(%s)",(account_no,account_no))
			con.commit()
			data=cur.fetchall()
			count=0
			t = PrettyTable(['Sender','Receiver','Date - Time','Credit','Debit'])
			for i in data:		
				count+=1		

				t.add_row([i[1],i[2],i[3],i[4],i[5]])	
			print(t)	

		elif(opt==6):
			op=int(input("do u really want to close account. type y for yes and n for no"))
			if(op=="y"):
				cur.execute("UPDATE `user` SET `status`='close' where `acct_no`=(%s)",(account_no))
				print("\nAccount closed")
			else:
				print("you opted for no . Thank you")	 
				exit()
		elif(opt==8):
			
			print("Thanks for banking with us. See u next time.")
			lines()
			exit()


			
			
def adminlogin():
	username=input("enter username\t:\t")
	cur.execute("SELECT `username`,`password` from `admin` WHERE `username`=(%s)",(username))
	con.commit()
	admin_fetch=cur.fetchall()

	if(len(admin_fetch)==0):
		print("\nno such admin. Try again\t:\t ")
		exit()
	password=input("\nenter password\t:\t")
	while(admin_fetch[0][1]!=password):
		print("\nTry Again")
		password=input("\nenter correct password\t:\t")
	while(1):
		ch=int(input("enter your choice\n 1. check all the accounts \n 2. check all the closed accounts \n 3. logout\n "))	
		if(ch==1):
			cur.execute("SELECT * from `user`")
			con.commit()
			user_data=cur.fetchall()
		
			t = PrettyTable(['Account_no','Name','DOB','Address','Account Type','Balance','Date','Status'])
			for i in user_data:
				name=i[2]+" "+i[3]
				t.add_row([i[0],name,i[4],i[5],i[6],i[9],i[10],i[11]])
			print(t)	

		elif(ch==2):
			cur.execute("SELECT * from `user` where `status`='close'")
			con.commit()
			user_data=cur.fetchall()
		
			t = PrettyTable(['Account_no','Name','DOB','Address','Account Type','Balance','Date','Status'])
			for i in user_data:
				name=i[2]+" "+i[3]
				t.add_row([i[0],name,i[4],i[5],i[6],i[9],i[10],i[11]])
			print(t)	
		elif(ch==3):
			print("\t\t\t\tthank you :)")
			exit()		
		else:
			print("\t\t\t\tinvalid choice ")	
	
		


					




			
				
 


	



while(1):
	print("1.sign up \n2.log in \n3.admin login \n4.exit")
	option=int(input("enter your choice\n"))
	print("")
	if(option==1):
		signup()
	elif(option==2):
		login()
	elif(option==3):
		adminlogin()
	else:
		print("thanks for choosing us. bye")
		exit()		
