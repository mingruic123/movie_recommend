from flask import Flask, request, url_for, jsonify, render_template, redirect
import engine as engine
import moviedata as m
app = Flask(__name__)

@app.before_first_request
def readData():
    print('Loading data...')
    m.read_data()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Receive data from URL by GET operation"""
    if request.method == 'GET':
        title = request.args.get('title').lower()
        review = request.args.get('review')
        result = engine.user_recommendation(title, review)
        if result[1] == True:
            return jsonify(result[0])
        else:
            return result

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Receive data from HTML form by POST operation"""
    if request.method == 'GET':
        #input = request.form
        #title = input['name'].lower()
        title = request.args.get('name')
        print(title)
        result = engine.similar_movies(title, 10)
        if result[1] == True:
            return jsonify(result[0])
        else:
            return result


@app.route('/autoSuggest', methods=['POST'])
def auto_suggest():
    if request.method == 'POST':
        input = request.form
        title = input['similar_title'].lower()
        if input['choice'] == 'Yes':
            result = engine.similar_movies(title, 10)
            if result[1] == True:
                return jsonify(result[0])
            else:
                return result
        else:
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()
