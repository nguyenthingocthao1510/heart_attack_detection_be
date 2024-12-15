import pymysql

hostname = 'byidr5v6nlhpekvrv8og-mysql.services.clever-cloud.com'
user = 'ubidznrunxwyuqke'
password = 'SMC7p0rv3J09jZ4ThuU1'
database = 'byidr5v6nlhpekvrv8og'

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    db=database,
)
