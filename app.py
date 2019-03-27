from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return render_template('post.html')
    elif request.method == 'POST':
        value = request.form['test']
        return render_template('default.html')


@app.route('/post', methods=['POST'])
def post():
    value = request.form['test']
    return value


@app.route('/template')
def template():
    return render_template(
        'index.html',
        title='Flask template test',
        my_str='Hello Flask',
        my_list=[x + 1 for x in range(30)]
    )


if __name__ == '__main__':
    app.run(debug=True)
