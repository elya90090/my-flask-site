from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)

DATA_FILE = 'data.json'
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return "<h2>سایت راه‌اندازی شد ✅</h2>"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        item = {
            'page': request.form['page'],
            'name': request.form['name'],
            'desc': request.form['desc'],
            'link': request.form['link']
        }
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append(item)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return redirect('/admin')
    return render_template('admin.html')
