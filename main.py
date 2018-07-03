from flask import Flask,render_template,request
import urllib
import subprocess
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/traffic", methods=['POST'])
def traffic():

    # url = "http://quiz8-env.3ftfvmwv4e.us-east-2.elasticbeanstalk.com/"
    for i in range(0,200):
        # subprocess.urllib.urlopen("http://quiz8-env.3ftfvmwv4e.us-east-2.elasticbeanstalk.com/")
        urllib.urlopen("http://quiz8-env.3ftfvmwv4e.us-east-2.elasticbeanstalk.com/")
        # subprocess.Popen("http://quiz8-env.3ftfvmwv4e.us-east-2.elasticbeanstalk.com/", shell=True)
        # subprocess.Popen(['python3', '-u', '-m', "http://quiz8-env.3ftfvmwv4e.us-east-2.elasticbeanstalk.com/"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return render_template("traffic.html")


if __name__ == '__main__':
    app.run()
