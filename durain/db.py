import sqlite3
from typing import Text

# conn=sqlite3.connect('order.sqlite3')
# curs=conn.cursor()

# curs.execute("""
#     CREATE TABLE orders (
# 	name	text,
# 	phone	text,
# 	address	text,
# 	quantity	integer,
# 	quantity_unit	text,
# 	durain_type	text,
# 	delivery_time	text

# ) """)



# curs.execute("""
#   CREATE TABLE promotions (
# 	promotion	text,
# 	validity	text
# )""")


#get promotions from db
def get_promotions():
	conn=sqlite3.connect('order.sqlite3')
	curs=conn.cursor()
	promotions=list(curs.execute("SELECT * FROM promotions"))[0]
	promo=promotions[0]
	validity=promotions[1]

	conn.commit()
	conn.close()
	return (promo,validity)

	

# get durain details from db
def get_duarin_details_and_image_uri(durain_name):
	conn=sqlite3.connect('order.sqlite3')
	curs=conn.cursor()
	command="SELECT * FROM details WHERE durain_name='{}'".format(durain_name)
	item=list(curs.execute(command))[0]
	details=item[1]
	url=item[2]
	conn.commit()
	conn.close()
	return (details,url)




# inserts feedback into feedback table 
def insert_feedback(name,phone,feedback):
	conn=sqlite3.connect('order.sqlite3')
	curs=conn.cursor()
	values=(name,phone,feedback)
	command="INSERT INTO feedbacks VALUES (? ,? ,? )"
	curs.execute(command,values)
	conn.commit()
	conn.close()
	print("data inserted")




# inserts order in order db
def insert_order(name,phone,address,quantity,quantity_unit,duarin_type,delivery_time):
	conn=sqlite3.connect('order.sqlite3')
	curs=conn.cursor()
	values=(name,phone,address,quantity,quantity_unit,duarin_type,delivery_time)
	command="INSERT INTO orders VALUES (? ,? ,? ,? ,? ,? ,? )"
	curs.execute(command,values)
	conn.commit()
	conn.close()
	print("data inserted")



# curs.execute("SELECT * FROM orders WHERE name='faiz'")
# print(curs.fetchone())

# get_duarin_details_and_image_uri("RedPrawnorAngHae")
# insert_feedback("aiz","032212121","i hate")
