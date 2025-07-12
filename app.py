from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os

app = Flask(__name__)
app.secret_key = 'change-me'

DATA_FILE = 'data.json'
VOTE_FILE = 'votes.json'
LOCALES_DIR = 'locales'

# Ensure files exist
for file_name, default in [(DATA_FILE, []), (VOTE_FILE, {})]:
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=2)

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_votes():
    with open(VOTE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_votes(votes):
    with open(VOTE_FILE, 'w', encoding='utf-8') as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)

def get_translation():
    lang = session.get('lang', 'fa')
    path = os.path.join(LOCALES_DIR, f'{lang}.json')
    if not os.path.exists(path):
        path = os.path.join(LOCALES_DIR, 'fa.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/setlang/<lang>')
def set_lang(lang):
    if lang in ['fa', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or '/')

@app.route('/')
def index():
    t = get_translation()
    return render_template('index.html', t=t)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    t = get_translation()
    if request.method == 'POST':
        data = load_data()
        data.append({
            'page': request.form['page'],
            'name': request.form['name'],
            'desc': request.form['desc'],
            'link': request.form['link']
        })
        save_data(data)
        return redirect(url_for('items_view'))
    return render_template('admin.html', t=t)

@app.route('/items')
def items_view():
    t = get_translation()
    data = load_data()
    votes = load_votes()
    # Calculate average ratings
    for idx, item in enumerate(data):
        key = str(idx)
        vr = votes.get(key, [])
        item['rating'] = round(sum(vr)/len(vr),1) if vr else 0
        item['count'] = len(vr)
        item['id'] = idx
    return render_template('items.html', items=data, t=t)

@app.route('/vote', methods=['POST'])
def vote():
    key = request.json.get('item_id')
    rating = int(request.json.get('rating'))
    votes = load_votes()
    votes.setdefault(str(key), []).append(rating)
    save_votes(votes)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
