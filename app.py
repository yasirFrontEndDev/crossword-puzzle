import os
import urllib
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

CODEWORD_SOLVER_REPO = "solver"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.cgi')
def index_cgi():
    return redirect(f'/results?{request.query_string.decode()}')

@app.route('/multi_patterns.cgi')
def multi_pattern_cgi():
    return redirect(f'/results?{request.query_string.decode()}')

@app.route('/multi_patterns')
def multi_patterns():
    return render_template('index.html', multi_patterns=True)

@app.route('/results')
def results():
    qs = urllib.parse.parse_qsl(request.query_string.decode())
    pattern1 = ""
    pattern2 = ""
    dictionary = "merged.txt"

    for k, v in qs:
        if k.startswith("l"):
            if v.isalnum() and len(v) == 1:
                pattern1 += v
            elif v in ['.', '?', ' ']:
                pattern1 += "."
            else:
                data = "<hr />Error - malformed input - please try again with only alphanumeric characters and spaces/full stops"
                return render_template('index.html', data=data)

        if k.startswith("m"):
            if v.isalnum() and len(v) == 1:
                pattern2 += v
            elif v in ['.', '?', ' ']:
                pattern2 += "."
            else:
                data = "<hr />Error - malformed input - please try again with only alphanumeric characters and spaces/full stops"
                return render_template('index.html', data=data)

        elif k == "dict":
            if v == "big":
                dictionary = "merged.txt"
            elif v == "original":
                dictionary = "old_dict.txt"
            elif v == "pocket":
                dictionary = "pocket.txt"

    if pattern2 != "":
        p = subprocess.Popen([f"{CODEWORD_SOLVER_REPO}/solver", "--dict", f"{CODEWORD_SOLVER_REPO}/dictionaries/{dictionary}", pattern1, pattern2], stdout=subprocess.PIPE)
        output = p.communicate()[0].decode()
        output = output[:500000].replace("\n", "<br />")

        data = f"<hr />Solutions for <b>{pattern1.upper()}</b>:<b>{pattern2.upper()}</b><br /><br / >{output}"

        return render_template('index.html', data=data, multi_patterns=True)
    else:
        p = subprocess.Popen([f"{CODEWORD_SOLVER_REPO}/solver", "--dict", f"{CODEWORD_SOLVER_REPO}/dictionaries/{dictionary}", pattern1], stdout=subprocess.PIPE)
        output = p.communicate()[0].decode()
        output = output[:500000].replace("\n", "<br />")

        data = f"<hr />Solutions for <b>{pattern1.upper()}</b><br /><br / >{output}"

        return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

