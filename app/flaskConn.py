from flask import Flask, url_for, redirect, render_template, request
import time

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.static_folder = '../static'

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=["GET", "POST"])
def my_site():
    if request.method == "POST":
        msg = request.form.get("input-msg")
        return msg
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)