from flask import Flask,render_template,request
import os,sqlite3,csv

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    loc = os.path.join(APP_ROOT, 'static/')
    print(loc)

    if not os.path.isdir(loc):
        os.mkdir(loc)

    for file in request.files.getlist("file"):
        print (file)
        filename = file.filename
        dest_loc = "/".join([loc, filename])
        print(dest_loc)
        file.save(dest_loc)

    return render_template("success.html")


conn = sqlite3.connect('earthquake.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS earthquake( time1 datetime ,latitude float,longitude float,depth float,mag float,magtype varchar(100),nst int,gap flaot,dmin float,rms float, id varchar(100),place varchar(100),depthError float,magError float, magnst float, locationsource  varchar(100))")

reader = csv.reader(open('static/edata.csv', 'r') )
for row in reader:
    to_db = [row[0], row[1], row[2], row[3], row[4], row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15]]
    cur.execute("INSERT INTO earthquake (time1, latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,id,place,depthError,magError,magnst,locationsource) VALUES (?, ?, ?,? ,? ,?,?,?,?,?,?,?,?,?,?,?);", to_db)
conn.commit()


@app.route("/gap_range", methods=['POST'])
def gap_range():
    from_gap = request.form['from_gap']
    to_gap = request.form['to_gap']
    cur.execute("select count(*) from earthquake WHERE gap>= ? and gap <= ? ",(from_gap,to_gap,))
    inside= cur.fetchall()
    inside.append(inside)
    cur.execute("select count(*) from earthquake WHERE gap< ?", (from_gap,))
    below = cur.fetchall()
    inside.append(below)
    cur.execute("select count(*) from earthquake WHERE gap> ?", (to_gap,))
    above=cur.fetchall()
    inside.append(above)

    return render_template("gap.html",row=inside)


@app.route("/location", methods=['POST'])
def location():
    loc = request.form['loc']
    mag = request.form['mag']

    cur.execute("select time1,latitude,longitude from earthquake WHERE mag>= ? and locationsource =? ", (mag, loc,))
    locs = cur.fetchall()
    return render_template("location.html",row=locs)

if __name__ == '__main__':
    app.run()
