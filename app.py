from flask import Flask 
from flask import request
from flask import jsonify
from flask import render_template
from flask import make_response
from flask import session
from flask import redirect , url_for
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)

app.secret_key = 'fa59ff82e20efce0d3f9f1ba2657d5d0'

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  #remove the same site cookie warning on firefox
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/")
def index():
    session['cutoff_data'] = []
    return render_template('page.html')

@app.route("/process", methods=['POST'])
def process():
    data = request.get_json()
    min_percentile = data.get('mn')
    max_percentile = data.get('mx')
    seat_types = data.get('seattype')
    courses = data.get('courses')

    print(f'''
    -------------------------------------------
    NEW HIT at {datetime.now().time()} 
    DETAILS
    Min Percentile: {min_percentile}
    Max Percentile: {max_percentile}
    Seat Types: {seat_types}
    Courses: {courses}
    -------------------------------------------
    ''')
    cutoffdata = get_filtered_cutoffs(min_percentile , max_percentile , seat_types , courses)

    session['cutoff_data'] = cutoffdata

    return redirect(url_for('result'))

@app.route("/result")
def result():
    cutoffdata = session.get('cutoff_data',[])
    return render_template('result.html', data=cutoffdata)

def get_filtered_cutoffs(mn , mx , seats_list , courses_list):

    college_list = []

    conn = sqlite3.connect('/home/tervicke/CET_college_search/data.db')
    cursor = conn.cursor()

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
            college_data = {
                "college_name":row[0],
                "seattype":row[1],
                "course_name":row[2],
                "cutoff_percentile":row[4],
            }
            college_list.append(college_data)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

    return college_list

if __name__ == '__main__':
    app.run(debug=True)
