from flask import Flask, redirect, request
from app.db import DAO
from .views import main_views, auth_views, test_views
from app.logger import logger
from apscheduler.schedulers.background import BackgroundScheduler
import traceback

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super key'
    dao = DAO()

    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(test_views.bp)

    schedule = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
    schedule.add_job(point_reset,'cron', day=1, hour=6, minute=0)
    schedule.start()

    @app.errorhandler(404)
    def page_not_found(error):
        logger.error(error)
        return '<h1>페이지를 찾을 수 없습니다.</h1>'

    @app.before_request
    def before_request():
        logger.info(f'[{request.method}][{request.url}]')
    

    return app


def point_reset():
    dao = DAO()
    try:
        logger.info('=====POINT RESET START=====')
        employee_list = dao.getAllEmployee('')
        dao.pointReset()
        for employee in employee_list:
            dao.insertPointLog(employee.user_id, -30000, '월 초 포인트 리셋')
        logger.info('=====POINT RESET SUCCESS=====')
    except Exception as e:
        logger.error("=====POINT RESET ERROR=====")
        logger.error(traceback.format_exc())
        dao.insertLog('admin', '포인트 초기화 오류', 'ERROR')
    



