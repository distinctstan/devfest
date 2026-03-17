import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="devfestdb",
  host="mysql-63c54de-stantechsolutions20-433a.k.aivencloud.com",
  password="AVNS_0DGOppAMKgvy63mM3Cg",
  read_timeout=timeout,
  port=22971,
  user="avnadmin",
  write_timeout=timeout,
)
  
try:
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
  cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
  cursor.execute("SELECT * FROM mytest")
  print(cursor.fetchall())
finally:
  connection.close()