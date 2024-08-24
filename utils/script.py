import pandas as pd
import sqlite3

#excel stuff
file_path = "cap1.xlsx"
df = pd.read_excel(file_path)

# setup_db
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def add_colleges():
    for index,row in df.iterrows():
        college_name = row['Institute Name']
        try:
            cursor.execute('INSERT INTO colleges (college_name) VALUES (?)', (college_name,))
            conn.commit()
            print(row['Institute Name'])
        except sqlite3.IntegrityError as e:
            print(f"Skipping {college_name}: {e}")

def add_courses():
    for index,row in df.iterrows():
        course_name = row['Course Name']
        try:
            cursor.execute('INSERT INTO courses (course_name) VALUES (?)', (course_name,))
            conn.commit()
            print(row['Course Name'])
        except sqlite3.IntegrityError as e:
            print(f"Skipping {course_name}: {e}")

def map_course_to_college():
    for index,row in df.iterrows():
        course_name = row['Course Name']
        college_name = row['Institute Name']
        try:
            cursor.execute('INSERT INTO collegemap (college_id,course_id) VALUES (?,?)', (college_name,course_name,))
            conn.commit()
            print(college_name,' ',course_name)
        except sqlite3.IntegrityError as e:
            print(f"Skipping {course_name}: {e}")

def populate_cutoff():
    for index,row in df.iterrows():
        college_name = row['Institute Name']
        cursor.execute("SELECT college_id from colleges where college_name = ?",(college_name,))
        college_id = cursor.fetchone()

        course_name = row['Course Name']
        cursor.execute("SELECT course_id from courses where course_name = ?",(course_name,))
        course_id = cursor.fetchone()
        
        seattype = row['Seat Alloted']
        Cutoff_rank = row['Merit Number']
        percentile = row['Score (MHTCET percentile)']

        #check if the entry exists
        cursor.execute('''
        select cutoff_id from Cutoffs where college_id = ? and course_id = ? and seattype = ?
        ''',(college_id[0] , course_id[0] , seattype))
        exists = cursor.fetchone()
        if exists:
            cursor.execute('''
            update Cutoffs
            set Cutoff_rank = ? , percentile = ? 
            where cutoff_id = ?
            ''',(Cutoff_rank , percentile , exists[0]))
        else:
            cursor.execute('''
            INSERT INTO Cutoffs (college_id , course_id , seattype , Cutoff_rank , percentile) values (?,?,?,?,?)
            ''',(college_id[0] , course_id[0] , seattype , Cutoff_rank , percentile))
        conn.commit()

def get_filtered_cutoffs(mn , mx , seats_list , courses_list):
    courseslists_placeholder = ','.join(['?'] * len(courses_list)) 
    seatlists_placeholder = ','.join(['?'] * len(seats_list)) 
    try:
        # Execute the query
        query =f'''
        SELECT 
            c.college_name, 
            co.seattype, 
            cr.course_name, 
            co.cutoff_rank,
            co.percentile
        FROM 
            Cutoffs co
        JOIN 
            colleges c ON co.college_id = c.college_id
        JOIN 
            courses cr ON co.course_id = cr.course_id
        WHERE 
            co.percentile BETWEEN ? AND ? 
            AND co.seattype IN ({seatlists_placeholder})
            AND cr.course_name IN ({courseslists_placeholder})
        '''
        param = [mn,mx] + seats_list + courses_list 
        cursor.execute(query , param)

        # Fetch all results
        results = cursor.fetchall()

        print(len(results))

        # Print or process results
        for row in results:
            #print(f"College: {row[0]}, Seat Type: {row[1]}, Course: {row[2]}, Cutoff Rank: {row[3]}")
            print(f"{row[0]} - {row[2]}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

# Call the function
seatlist = ['GOPENH','GOPENS']
courseslist = ['Mechanical Engineering']
get_filtered_cutoffs(93 , 97 , seatlist , courseslist)
conn.close()
