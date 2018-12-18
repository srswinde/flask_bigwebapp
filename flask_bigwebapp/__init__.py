from flask import Flask
app = Flask(__name__)

from flask_basicauth import BasicAuth
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.csrf import CSRFProtect
from flask import request, abort
import subprocess
from flask import render_template
import json
import uuid
from scottSock import scottSock
from mtnopslogger.biglog import boltwoodSQL, ngtelemSQL
from flask import jsonify
from flask_cors import CORS
import sys

if len(sys.argv) ==2 :
    config_path = sys.argv[1]
else:
    config_path = "/home/scott/.mtnops/flask_bigwebapp.json"


with open(config_path) as fd:
    config = json.load(fd)

app.config['BASIC_AUTH_USERNAME'] = config["auth_username"]
app.config['BASIC_AUTH_PASSWORD'] = config["auth_password"]
app.config["SECRET_KEY"] = str(uuid.uuid1())
basic_auth = BasicAuth( app )
cors = CORS(app, resources={r"/latest.json": {"origins": "*"}})

devlist = {
        "boltwood":boltwoodSQL,
        "ngtelem":ngtelemSQL

        }

class reboot(FlaskForm):
    submit = SubmitField( 'Reboot bigpop' )

class shutdown(FlaskForm):
    submit = SubmitField( 'Shutdown bigpop' )

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/drives.html')
def drives():
    return render_template("bigdrives.html")

@app.route("/latest.json")
def latest_json():
    s=scottSock("10.30.1.2", 5000)
    resp=s.converse(b'\n').decode("utf-8")
    return jsonify(json.loads(resp))


@app.route("/recent/data/<table>.<ftype>", methods=["GET"])
def recent_data(table, ftype):
    if table not in devlist.keys():
        abort(404)

    if ftype not in ("csv", "html"):
        ftype = "html"

    dev = devlist[table]

    try:
        minsago=float(request.args.get("minsago"))
    except Exception as err:
        print(err)
        minsago=30
    dt=dev.recent(minsago=minsago)
    
    if ftype == "csv":
        strdata = dt.to_csv()
    elif ftype == "html":
        strdata = dt.to_html()
    return strdata


@app.route("/info")
def log_description():
    output = {}
    for devname, dev in devlist.items():
        output[devname] = dev().ColumnDescription

    return json.dumps(output)

@app.route('/power/<dowhat>', methods=["GET", "POST"] )
@basic_auth.required
def reboot_bigpop( dowhat ):
    if dowhat == "reboot":
        form=reboot()
    elif dowhat == "shutdown":
        form = shutdown()
    else:
        abort(404)
    if request.method == "POST":

        if dowhat == "reboot":
            
            try:
                resp = subprocess.check_output(["sudo", "/usr/local/bin/shutdown_script.sh"] )
            
            except Exception as err:
                return str(err)

            return "Shuttign down bigpop in 1 minute"

        elif dowhat == "shutdown":
            try:
                resp = subprocess.check_output(["sudo", "/usr/local/bin/shutdown_script.sh"] )
            except Exception as err:
                return str(err)

            return "Shutting bigpop down in 1 minute"   

    return render_template("reboot.html", form=form)


#@app.route('/shutdown')
@basic_auth.required
def shutdown_bigpop():
    resp = subprocess.check_output(["sudo", "/usr/local/bin/shutdown_script.sh"] )


if __name__ == "__main__":
    app.run( host="0.0.0.0", port=8888, debug=True )
