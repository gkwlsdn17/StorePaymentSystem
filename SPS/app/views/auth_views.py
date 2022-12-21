import bcrypt
from flask import Blueprint, render_template, url_for, request, flash, session
from werkzeug.utils import redirect
from ..db import DAO
from app.logger import logger
bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/main')
def main():
    return render_template('auth_main.html')

@bp.route('/signin', methods=['POST'])
def login():
    id = request.form['id']
    pw = request.form['pw']

    dao = DAO()
    user = dao.getEmployee(id)
    if user is not None:
        if user.user_id == id and bcrypt.checkpw(pw.encode('utf-8'), user.user_password.encode('utf-8')):
            session['user_id'] = id
            if user.type == 1:
                logger.info(f'{id} Login Success')
                dao.insertLog(id, f'{id} Login Success', 'INFO')
                return redirect("/admin")
            else:
                return redirect('/')

    flash("Login Fail")
    logger.info(f'{id} Login Fail')
    dao.insertLog(id, f'{id} Login Fail', 'INFO')
    return redirect('/auth/main')

@bp.route('/signout')
def logout():
    session.pop('user_id', None)
    return redirect('/auth/main')

@bp.route('/signup', methods=['GET'])
def pageSignUp():
    return render_template('employee_insert.html')

@bp.route('/signup', methods=['POST'])
def signup():
    try:
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']

        password = (bcrypt.hashpw(pw.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
        dao = DAO()
        res = dao.insertEmployee(name, id, password, email, position)
        
        if res is None:
            raise Exception('Employee Insert Fail')
        
        dao.insertLog(id, f'{id} Sign up success', 'INFO')
        flash("회원가입 성공")
        return redirect('/admin/employee')
    except Exception as e:
        logger.error(e)
        dao.insertLog(id, e, 'ERROR')
        flash("회원가입 실패")
        return redirect('/admin/employee')