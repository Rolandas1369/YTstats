import mysql.connector

my_db = mysql.connector.connect(
    option_files='../mysql.cnf'
)

""" Mysql table creation, data insertation functions """

def create_tables(mydb):
    """ Creates table for data storage from API"""
    mydb._execute_query("CREATE TABLE video_data ("
                        " id INT AUTO_INCREMENT PRIMARY KEY, "
                        " channel_id VARCHAR(255) NOT NULL, "
                        " tags TEXT, "
                        " video_id VARCHAR(255) NOT NULL, "
                        " time TIMESTAMP, "
                        " video_views INT, "
                        " videos_views_median INT, "
                        " perf_diff INT"
                        ");")

def insert_data(data_dict, table_name, mycursor, mydb):
    """ Inserts data to MySQL, checks for duplicates before insertion """
    rows = ",".join(data_dict.keys())
    mycursor.execute("SELECT video_id FROM " + table_name + "")
    myresult = mycursor.fetchall()
    result = [x[0] for x in myresult]

    if data_dict['video_id'] in result:
        print('Video present do nothing', data_dict['video_id'])
    else:
        values = [i for i in data_dict.values()]
        args_number = "".join(len(data_dict) * '%s,')

        mysql_insert_query = """ INSERT INTO """ + table_name + \
        """ (""" + rows + """) VALUES (""" + args_number[:-1] + """)"""

        mycursor.execute(mysql_insert_query, values)
        mydb.commit()

create_tables(my_db)

# import statistics
# listA = [19, 46, 21, 18, 30]
# print(statistics.median(listA))
