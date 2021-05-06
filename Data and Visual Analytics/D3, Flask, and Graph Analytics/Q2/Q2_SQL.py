########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')

        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "kbarthelson3"
        return gt_username

    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies(id integer, title text, score real);"
        ######################################################################

        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = """CREATE TABLE movie_cast(movie_id integer, cast_id integer,
        cast_name text, birthday text, popularity real);"""
        ######################################################################

        return self.execute_query(connection, part_ai_2_sql)

    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        try:
            with open(path,encoding = 'utf-8',errors='ignore') as csvfile:
                file = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
                for row in file:
                    sql = "INSERT INTO movies (id, title, score) VALUES (?,?,?);"
                    connection.execute(sql,(str(row[0]), str(row[1]).replace("'", "").replace("\"", ""), str(row[2])))
        except:
            with open(path,errors='ignore') as csvfile:
                file = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
                for row in file:
                    sql = "INSERT INTO movies (id, title, score) VALUES (?,?,?);"
                    connection.execute(sql,(str(row[0]), str(row[1]).replace("'", "").replace("\"", ""), str(row[2])))

        connection.commit()
       ######################################################################

        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        try:
            with open(path,encoding = 'utf-8',errors='ignore') as csvfile:
                file = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
                for row in file:
                    sql = "INSERT INTO movie_cast (movie_id, cast_id, cast_name, birthday, popularity) VALUES (?,?,?,?,?);"
                    connection.execute(sql,(str(row[0]),str(row[1]).replace("'", "").replace("\"", ""), str(row[2]),str(row[3]),str(row[4])))
        except:
            with open(path,errors='ignore') as csvfile:
                file = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
                for row in file:
                    sql = "INSERT INTO movie_cast (movie_id, cast_id, cast_name, birthday, popularity) VALUES (?,?,?,?,?);"
                    connection.execute(sql,(str(row[0]),str(row[1]).replace("'", "").replace("\"", ""), str(row[2]),str(row[3]),str(row[4])))

        connection.commit()
        ######################################################################

        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = """CREATE TABLE cast_bio AS SELECT DISTINCT
        mc.cast_id, mc.cast_name, mc.birthday, mc.popularity FROM movie_cast mc;"""
        # birthday is date or text?
        ######################################################################

        self.execute_query(connection, part_aiii_sql)

        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = ""
        ######################################################################

        self.execute_query(connection, part_aiii_insert_sql)

        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]


    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE INDEX movie_index ON movies(id);"
        #movie_index for the id column in movies table

        ######################################################################
        return self.execute_query(connection, part_b_1_sql)

    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index ON movie_cast(cast_id);"
        #ii. cast_index for the cast_id column in movie_cast table

        ######################################################################
        return self.execute_query(connection, part_b_2_sql)

    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE INDEX cast_bio_index ON cast_bio(cast_id);"
        #iii. cast_bio_index for the cast_id column in cast_bio table
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)

    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """SELECT printf("%.2f",100*sum(CAST(war AS FLOAT))/(CAST(count(id) AS FLOAT)))
        FROM (SELECT id, CASE WHEN (title LIKE '%war%' AND score > 50) THEN 1 ELSE 0 END AS war FROM movies)"""

        #  Calculate a proportion. Find the proportion of movies having a score > 50 and that has ‘war’ in
        # the name. Treat each row as a different movie. The proportion should only be based on the total number
        # of rows in the movie table. Format all decimals to two places using printf(). Do NOT use the
        # ROUND() function as it does not work the same on every OS.
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = """SELECT cast_name,count(cast_id) appearance_count FROM movie_cast
        WHERE popularity > 10
        GROUP BY cast_name
        ORDER BY appearance_count DESC, cast_name ASC LIMIT 5"""
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """SELECT m.title movie_title, printf("%.2f", m.score) movie_score, count (mc.cast_id) cast_count
        FROM movies m INNER JOIN movie_cast mc ON m.id = mc.movie_id
        GROUP BY m.title
        ORDER BY m.score DESC, count (mc.cast_id) ASC, m.title ASC LIMIT 5"""
        #Sort the results by score in descending order, then by number of cast
        # members in ascending order, then by movie name in alphabetical order
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()

    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """SELECT mc.cast_id, mc.cast_name, printf("%.2f", avg(m.score)) average_score
        FROM movies m INNER JOIN movie_cast mc ON m.id = mc.movie_id
        WHERE m.score >= 25
        GROUP BY mc.cast_id
        HAVING COUNT(mc.movie_id) >2
        ORDER BY average_score DESC, cast_name ASC LIMIT 10
        """
        # top ten cast members who have the highest average movie scores
        # Sort the output by average score in descending order,
        # then by cast_name in alphabetical order
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """CREATE VIEW good_collaboration AS
        SELECT DISTINCT a.cast_id cast_member_id1, b.cast_id cast_member_id2, count(a.movie_id) movie_count,
        AVG(m.score) average_movie_score
        FROM movie_cast a INNER JOIN movie_cast b ON a.movie_id = b.movie_id
        INNER JOIN movie m ON a.movie_id = m.id
        WHERE cast_member_id1 != cast_member_id2
        GROUP BY (cast_member_id1,cast_member_id2)
        HAVING count(movie_id) >= 3 AND average_movie_score >= 40;"""
        ######################################################################
        return self.execute_query(connection, part_g_sql)

    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """SELECT DISTINCT mc.cast_id, mc.cast_name,
        AVG(CAST(gc1.average_movie_score AS FLOAT)+CAST(gc2.average_movie_score AS FLOAT)) collaboration_score
        FROM movie_cast mc INNER JOIN good_collaboration gc1 ON gc1.cast_member_id1 = mc.cast_id
        INNER JOIN good_collaboration gc2 ON gc2.cast_member_id2 = mc.cast_id
        GROUP BY mc.cast_id
        ORDER BY AVG(CAST(gc1.average_movie_score AS FLOAT)+CAST(gc2.average_movie_score AS FLOAT)) DESC, cast_name ASC
        LIMIT 5
        """
        #Get the 5 cast members with the highest average scores from the good_collaboration view,
        # and call this score the collaboration_score. This score is the average
        # of the average_movie_score corresponding to each cast member,
        # including actors in cast_member_id1 as well as cast_member_id2
        # Sort your output by this score in descending order, then by cast_name alphabetically
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()

    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE movie_overview USING fts3 (id, overview);"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path,errors='ignore') as csvfile:
            file = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for row in file:
                sql = "INSERT INTO movie_overview (id, overview) VALUES (?,?);"
                connection.execute(sql,(str(row[0]),str(row[1]).replace("'", "").replace("\"", "").replace(r"/","")))

        connection.commit()
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = """SELECT COUNT (id) fight FROM movie_overview WHERE UPPER(overview) LIKE '% FIGHT %'  OR
        UPPER(overview) LIKE 'FIGHT %' OR UPPER(overview) LIKE '% FIGHT?%' OR UPPER(overview) LIKE '% FIGHT!%' OR
        UPPER(overview) LIKE '% FIGHT' OR UPPER(overview) LIKE '% FIGHT.%' OR
        UPPER(overview) LIKE 'FIGHT';"""
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]

    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = """SELECT COUNT(id) space_program FROM movie_overview
        WHERE movie_overview MATCH 'overview:space AND overview:program';"""
        # 5: space ([^\s]+){0,} ([^\s]+){0,} ([^\s]+){0,} ([^\s]+){0,} ([^\s]+){0,} program
        # 4: space ([^\s]+){0,} ([^\s]+){0,} ([^\s]+){0,} ([^\s]+){0,} program
        # 3: space ([^\s]+){0,} ([^\s]+){0,} ([^\s]+){0,} program
        # 2: space ([^\s]+){0,} ([^\s]+){0,} program
        # 1: space ([^\s]+){0,} program
        # 0: space program
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":

    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2.db")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")

    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
