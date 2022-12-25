import datetime
import json
import traceback
from flask import Blueprint, render_template, session, url_for, request, flash
from werkzeug.utils import redirect
from ..db import DAO
from app.Common import Token, RESULT, __TIMEOUT__SEC__, __TIMEOUT__DAY__, __OFFSET__
from app.logger import logger
bp = Blueprint('main', __name__, url_prefix="/")

@bp.route("/")
def index():
    e ={}
    try:
        id = session['user_id']
        dao = DAO()
        e = dao.getEmployee(id)
    except:
        return redirect("/auth/main")

    return render_template('index.html', employee=e)

@bp.route("/admin")
def admin_index():
    try:
        id = session['user_id']
        print(id)
        dao = DAO()
        e = dao.getEmployee(id)
        if e.type != 1:
            return redirect("/")
        else:
            return render_template('admin_index.html')
    except:
        return redirect("/auth/main")
    
@bp.route("/admin/employee")
def pageEmployeeList():
    try:
        dao = DAO()
        keyword = request.args.get('keyword')
        if keyword is None:
            keyword = ''
        result = dao.getAllEmployee(keyword)
        return render_template('employee_list.html', employee=result)
    except Exception as e:
        logger.error(e)
        flash('정보를 불러 올 수 없습니다.')
        return redirect("/admin")

@bp.route("/admin/employee/info")
def pageEmployee():
    try:
        id = request.args.get('id')
        dao = DAO()
        r = dao.getEmployee(id)
        if r is None:
            raise Exception("pageEmployee Fail")
        return render_template('employee_info.html', employee = r)
    except Exception as e:
        logger.error(e)
        flash('정보를 불러 올 수 없습니다.')
        return redirect("/admin/employee")

@bp.route("/admin/employee/update", methods=["POST"])
def updateEmployee():
    try:
        user_id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        dao = DAO()
        r = dao.updateEmployee(name, user_id, email, position)
        if r is None:
            raise Exception('Update employee Fail')
        flash('수정이 완료되었습니다.')
        return redirect('/admin/employee')
    except Exception as e:
        logger.error(e)
        flash('수정 실패')
        return redirect(url_for('main.pageEmployee', id=user_id))
        
@bp.route("/admin/point")
def pagePointLogList():
    try:
        dao = DAO()
        start = request.args.get('start')
        end = request.args.get('end')
        keyword = request.args.get('keyword')
        page = request.args.get('page')
        print(start, end)
        if start is None:
            yyyymm = datetime.datetime.now().strftime("%Y%m")
            start = yyyymm + '01'
        if end is None:
            end = datetime.datetime.now().strftime("%Y%m%d")
        if page is None:
            page = 1
        if keyword is None:
            keyword = ''
        print(start, end)
        result = dao.getPointLog(start, end, page, __OFFSET__, keyword)
        return render_template('point_list.html', list=result, startDate=start, endDate=end)
    except Exception as e:
        logger.error(traceback.format_exc())
        flash(e)
        return redirect("/admin")


@bp.route("/admin/point/more")
def pagePointLogListMore():
    try:
        dao = DAO()
        start = request.args.get('start')
        end = request.args.get('end')
        keyword = request.args.get('keyword')
        page = request.args.get('page')
        if start is None:
            yyyymm = datetime.datetime.now().strftime("%Y%m")
            start = yyyymm + '01'
        if end is None:
            end = datetime.datetime.now().strftime("%Y%m%d")
        if page is None:
            page = 1
        else:
            page = int(page)
        if keyword is None:
            keyword = ''
        
        result = dao.getPointLog(start, end, page, __OFFSET__, keyword)
        data = (dict(r) for r in result)
        send_data = []
        for a in data:
            send_data.append(a)
        return json.dumps(send_data, default=str)
    except Exception as e:
        logger.error(traceback.format_exc())
        flash(e)
        return json.dumps({})

# 외부에서 포인트 제어하는 부분
@bp.route('/update/point', methods=["POST"])
def updatePoint():
    dao = DAO()
    result = RESULT()
    try:
        id = request.form['id']
        point = request.form['point']
        print(id, point)
        
        res = dao.updateEmployeePoint(id, point)
        if res is None:
            result.setError('E01')
            raise Exception("updateEmployeePoint error")

        res = dao.insertPointLog(id, point)
        if res is None:
            result.setError('E02')
            raise Exception("insertPointLog error")
        result.setRESULT('000')
        data = {
            'id':id,
            'point':point
        }
        result.setData(data)
        

    except Exception as e:
        logger.error(traceback.format_exc())
        e = str(e).replace('\'','')
        dao.insertLog(id, 'Update Point ERROR', 'ERROR')
        if len(dict(result.getError()).items()) == 0:
            result.setError('E00', e)
    finally:
        return json.dumps(result.getResult())

# 토큰 체크 후 포인트 업데이트
def updatePoint2(id, point, memo):
    dao = DAO()
    result = RESULT()
    try:
        
        print(id, point)
        
        res = dao.updateEmployeePoint(id, point)
        if res is None:
            result.setError('E01')
            raise Exception("updateEmployeePoint error")

        res = dao.insertPointLog(id, point, memo)
        if res is None:
            result.setError('E02')
            raise Exception("insertPointLog error")
        result.setRESULT('000')
        data = {
            'id':id,
            'point':point
        }
        result.setData(data)

    except Exception as e:
        logger.error(traceback.format_exc())
        e = str(e).replace('\'','')
        dao.insertLog(id, 'Update Point ERROR', 'ERROR')
        if len(dict(result.getError()).items()) == 0:
            result.setError('E00', e)
    finally:
        return result

# 토큰 생성
@bp.route('/token/make', methods=["POST"])
def makeToken():
    dao = DAO()
    result = RESULT()
    try:
        qrcode = request.form['qrcode']
        data = qrcode.split('$')
        id = data[0]
        time = data[1]
        qrtime = datetime.datetime(year=int(time[0:4]), month=int(time[4:6]), day=int(time[6:8]), hour=int(time[8:10]), minute=int(time[10:12]), second=int(time[12:]))
        if (datetime.datetime.now() - datetime.timedelta(seconds=__TIMEOUT__SEC__)) < qrtime:
            e = dao.getEmployee(id)
            if e.user_id is None:
                result.setError('E03', "User Id not exist")
                raise Exception("User Id not exist")
            else:
                result.setRESULT('000')
                token = Token(id, __TIMEOUT__DAY__)
                data = {
                    'token': token.getValue()
                }
                result.setData(data)
        else:
            result.setError('E04', "Time over")
            raise Exception("Time over")
    except Exception as e:
        print(traceback.format_exc())
        logger.error(traceback.format_exc())
        e = str(e).replace('\'','')
        dao.insertLog(id, e, 'ERROR')
        if len(dict(result.getError()).items()) == 0:
            result.setError('E00', e)
    finally:
        return json.dumps(result.getResult())
        

# 토큰 체크 - 거래에 앞서 가장 먼저 체크하는 부분
@bp.route('/token/check', methods=["POST"])
def checkToken():
    dao = DAO()
    result = RESULT()
    try:
        params = request.get_json()
        id = params['user_id']
        point = params['point']
        token = params['token']
        if "memo" in params:
            memo = params['memo']
        else:
            memo = ''
        data = str(token).split("$")
        if data[0] != id:
            result.setError('E05', "ID miss match")
            raise Exception("ID Miss Match")
        timeout = int(data[1]) # day
        time = data[2]
        tokenTime = datetime.datetime(year=int(time[0:4]), month=int(time[4:6]), day=int(time[6:8]), hour=int(time[8:10]), minute=int(time[10:12]), second=int(time[12:]))
        if (datetime.datetime.now() - datetime.timedelta(days=timeout)) < tokenTime:
            logger.info(f"{id} Token Check Success")
            dao.insertLog(id, 'Token Check Success', 'INFO')
            result = updatePoint2(id, point, memo)
        else:
            result.setError('E06', "Token Time out")
            raise Exception("Token Time out")

    except Exception as e:
        print(traceback.format_exc())
        logger.error(traceback.format_exc())
        e = str(e).replace('\'','')
        dao.insertLog(id, e, 'ERROR')
        if len(dict(result.getError()).items()) == 0:
            result.setError('E00', e)
    finally:
        return json.dumps(result.getResult())