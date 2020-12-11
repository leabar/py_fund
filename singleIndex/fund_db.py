"""
数据库连接
"""
#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "564268Lb", "db_fund")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# INSERT | DELETE | UPDATE
def edit(sql):
	try:
		# 执行sql语句
		cursor.execute(sql)
		# 提交到数据库执行
		db.commit()

		return cursor.rowcount
	except:
		# 如果发生错误则回滚
		db.rollback()

		print("执行失败")

	# 关闭数据库链接
	db.close()


# SELECT
def select(sql):
	try:
		# 执行sql语句
		cursor.execute(sql)
		# 获取所有记录列表
		resutls = cursor.fetchall()

		return resutls
	except:
		print("执行失败")

	# 关闭数据库链接
	db.close()




# # insert ==============================================================

# # 【一条】
# sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
# val = ("RUNOOB", "https://www.runoob.com")
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "记录插入成功")
# print("1条记录插入成功，ID: ", mycursor.lastrowid)		# 在数据记录插入后，获取该记录的 ID


# # 【多条】
# sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
# val = [
#   ('Google', 'https://www.google.com'),
#   ('Github', 'https://www.github.com'),
#   ('Taobao', 'https://www.taobao.com'),
#   ('stackoverflow', 'https://www.stackoverflow.com/')
# ]
# mycursor.executemany(sql, val)	
# mydb.commit()
# print(mycursor.rowcount, "记录插入成功。")


# # delete ==============================================================
# sql = "delete from site where id = 1"
# mycursor.execute(sql)
# mydb.commit()
# print(mycursor.rowcount, " 条记录删除")

# # 占位符
# sql = "delete from site where name = s%"
# na = ("stackoverflow", )
# mycursor.execute(sql, na)
# mydb.commit()
# print(mycursor.rowcount, " 条记录删除")


# # upadte ==============================================================
# sql = "update site set name = 'china' where id = 1"
# mycursor.execute(sql)
# mydb.commit()
# print(mycursor.rowcount, " 条记录被修改")

# # 占位符
# sql = "update site set name = s% where id = d%"
# val = ("china", 1)
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, " 条记录被修改")


# # select ==============================================================
# mycursor.execute("select * from 58pic_user order by id desc limit 10")
# result = mycursor.fetchall()
# for x in result:
# 	print(x)

# resultOne = mycursor.fetchone()
# print(resultOne)

# # 占位符
# sql = "SELECT * FROM sites WHERE name = %s"
# na = ("RUNOOB", )
# mycursor.execute(sql, na)
# result = mycursor.fetchall()












