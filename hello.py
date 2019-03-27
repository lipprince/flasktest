#!/usr/bin/python
# _*_ coding: utf-8 _*_

from flask import Flask, request, session, render_template, redirect, url_for, abort, make_response
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world!'


# @app.route 를 통해 URL 패턴 라우팅 가능
@app.route('/main')
def main():
    return 'main page'


# <> 로 패턴 변수 처리
# 로깅 테스트, app.logger 사용
@app.route('/user/<username>')
def showUserProfile(username):
    app.logger.debug('RETRIEVE DATA - Check Complete')
    app.logger.warn('RETRIEVE DATA - Warning... User Not Found')
    app.logger.error('RETRIEVE DATA - ERR! User unauthentication')
    return 'USER: %s' % username


@app.route('/user/id/<int:userId>')
def showUserProfileById(userId):
    return 'USER ID: %d' % userId


# 로그인과 세션 생성
# methods 를 통해 REST Action Type 지정
@app.route('/account/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # POST 요청의 파라메터를 가져오려면 request.form() 사용하하면 됨.
        userId = request.form['id']
        wp = request.form['wp']

        if len(userId) == 0 or len(wp) == 0:
            return userId + ', ' + wp + ' 로그인 정보가 올바르지 않습니다.'

        session['logFlag'] = True
        session['userId'] = userId
        return session['userId'] + '님 어서오세요.'
    # 지정되지 않은 Action Type 이면 405 에러 반환 됨.
    else:
        return '올바르지 않은 요청입니다.'


# 세션 키 생성, 로그인과 같이 세션을 맺어야 하는 경우 반드시 필요하고, 키를 생성하지 않으면 500에러 반환 됨.
app.secret_key = 'sample_secret_key'


# 로그인 정보 가져오기
@app.route('/user', methods=['GET'])
def getUser():
    if session.get('logFlag') != True:
        return '잘못 된 접근입니다.'

    # userId = session['userId']
    # return '[GET][USER] USER ID: {0}'.format(userId)
    if 'userId' in session:
        return '[GET][USER] USER ID: {0}'.format(session['userId'])
    # abort 로 특정 에러를 발생시킬 수 있다.
    else:
        abort(400)


# 로그아웃
@app.route('/account/logout', methods=['POST', 'GET'])
def logout():
    session['logFlag'] = False
    session.pop('userId', None)
    return redirect(url_for('main'))


# 에러처리
@app.errorhandler(400)
def uncaughtError():
    return '잘못 된 사용입니다.'


# 응답처리
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


# redirect 로 POST 데이터를 보내기 위해서는 url_for() 사용 시 상태 코드값을 같이 보내야 한다.
@app.route('/login', methods=['POST', 'GET'])
def login_direct():
    if request.method == 'POST':
        return redirect(url_for('login'), code=307)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    # app.debug = True
    app.run(debug=True)

