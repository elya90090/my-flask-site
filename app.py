from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    data = load_data()
    if request.method == 'POST':
        page = request.form['page']
        name = request.form['name']
        desc = request.form['desc']
        link = request.form['link']
        if page not in data:
            data[page] = []
        data[page].append({
            'id': len(data[page]) + 1,
            'name': name,
            'desc': desc,
            'link': link
        })
        save_data(data)
        return redirect(url_for('admin'))
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
