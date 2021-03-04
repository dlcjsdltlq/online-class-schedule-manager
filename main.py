from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QFileDialog
from manage_file import ManageFile
from memo_window import MemoWindow
from schedule_window import ScheduleWindow
from time_thread import TimeThread
from packaging import version
from plyer import notification
from util import resource_path
from util import getMemoAndOpenBrowser
from util import openBrowser
import requests
import datetime
import shutil
import sys
import os

main_form_class = uic.loadUiType(resource_path('./resources/ui/ui_main_window.ui'))[0]
schedule_sample_json = resource_path('./resources/json/schedule_sample.json')
logo_ico = resource_path('./resources/icon/logo.ico')

DEFAULT_FILE_PATH = 'C:\\OnlineClassScheduleManager'
DEFAULT_FILE_NAME = 'schedule.json'

CUR_VER = '1.2.1'
LATEST_VER = requests.get('https://raw.githubusercontent.com/dlcjsdltlq/online-class-schedule-manager/master/version.json').json()['version']

class MainWindow(QtWidgets.QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.checkVersion()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(logo_ico))
        self.style_font = QFont('Malgun Gothic')
        self.setFont(self.style_font)
        self.text_browser_memo.setFont(self.style_font)
        self.file_name : str #시간표 json 파일 이름
        self.schedule_dic : dict #시간표 데이터
        self.time_dic : dict #시간 일정 데이터
        self.memo_dialog : MemoWindow
        self.time_thread : TimeThread
        self.current_txt = None
        self.day_korean_string_list = ['월', '화', '수', '목', '금', '토', '일'] #숫자 인덱스 -> 한글 변환
        self.day_string_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] #숫자 인덱스 -> 영어 변환
        self.today_korean = self.day_korean_string_list[datetime.datetime.today().weekday()] #오늘 요일 한글
        self.today = self.day_string_list[datetime.datetime.today().weekday()] #오늘 요일 영어
        self.action_schedule_change.triggered.connect(self.openScheduleEditer) #시간표 변경 메뉴 실행
        self.action_open_file.triggered.connect(self.getFileFromUserPath) #시간표 불러우기 메뉴 실행
        self.text_browser_memo.anchorClicked.connect(self.anchorClicked) #텍스트 브라우저에서 url 클릭 이벤트
        self.period_schedule_widget_list = {'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': []} #각 과목별 버튼
        self.toggle_list = [False]*7 #토글된 버튼 리스트: True일 경우 초록색, False일 경우 빨간색
        self.day_schedule_widget_layout_list = [ #각 요일별 레이아웃
            self.schedule_mon, 
            self.schedule_tue, 
            self.schedule_wed, 
            self.schedule_thu, 
            self.schedule_fri, 
            ]
        self.file_manage_class = ManageFile()
        self.getFileFromDefaultPath()
        self.readSchedule()
        self.makeAndDrawWidgets()
        self.getPeriod()

    def checkVersion(self):
        if version.parse(LATEST_VER) > version.parse(CUR_VER):
            result = QtWidgets.QMessageBox.warning(self, '알림', '새 업데이트가 확인되었습니다\n다운로드 하시겠습니까?', QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
            if result == QtWidgets.QMessageBox.Apply:
                openBrowser('https://github.com/dlcjsdltlq/online-class-schedule-manager/releases/download/{0}/online-class-schedule-manager.v{0}.zip'.format(LATEST_VER))
                sys.exit(0)
            else:
                pass

    def getFileFromUserPath(self):
        user_file_name = QFileDialog.getOpenFileName(self, '파일 열기', './', "JSON Files (*.json)")[0]
        if user_file_name:
            if self.file_manage_class.validateJson(user_file_name):
                result = QtWidgets.QMessageBox.warning(self, '알림', '기존 파일을 대체하시겠습니까?', QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
                if result == QtWidgets.QMessageBox.Apply:
                    shutil.copy(user_file_name, DEFAULT_FILE_PATH + '//' + DEFAULT_FILE_NAME)
                    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
                else:
                    QtWidgets.QMessageBox.information(self, '알림', '취소되었습니다.', QtWidgets.QMessageBox.Apply)
            else:
                QtWidgets.QMessageBox.warning(self, '알림', '유효하지 않은 시간표 파일입니다.', QtWidgets.QMessageBox.Apply)

    def getFileFromDefaultPath(self): #기본 경로에서 파일 가져오기
        self.file_name = DEFAULT_FILE_PATH + '\\' + DEFAULT_FILE_NAME
        if (not os.path.isdir(DEFAULT_FILE_PATH)):
            os.mkdir(DEFAULT_FILE_PATH)
        if (not os.path.exists(self.file_name)):
            result = QtWidgets.QMessageBox.warning(self, '알림', '시간표가 존재하지 않습니다.\n생성하시겠습니까?', QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
            if result == QtWidgets.QMessageBox.Apply:
                self.file_manage_class.writeJson(self.file_name, self.file_manage_class.readJson(schedule_sample_json))
            elif result == QtWidgets.QMessageBox.Cancel:
                sys.exit(0)
        else:
            if not self.file_manage_class.validateJson(self.file_name):
                result = QtWidgets.QMessageBox.warning(self, '알림', '유효하지 않은 시간표 파일입니다.\n재생성하시겠습니까?', QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
                if result == QtWidgets.QMessageBox.Apply:
                    self.file_manage_class.writeJson(self.file_name, self.file_manage_class.readJson(schedule_sample_json))
                elif result == QtWidgets.QMessageBox.Cancel:
                    sys.exit(0)

    def makeAndDrawWidgets(self): #과목별 버튼 생성 및 그리기
        idx_day = 0
        self.label_today.setText(f'오늘은 {self.today_korean}요일입니다')
        for day in self.period_schedule_widget_list:
            idx_period = 0
            for i in range(7):
                self.period_schedule_widget_list[day].append(QtWidgets.QPushButton())
                widget = self.period_schedule_widget_list[day][i]
                widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                widget.clicked.connect(self.toggleButton)
                widget.setText(self.schedule_dic[day][idx_period])
                widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                widget.customContextMenuRequested.connect(self.modifyMemo)
                widget.setFont(self.style_font)
                if (day != self.today) or (self.schedule_dic[day][idx_period] == ''):
                    widget.setDisabled(True)
                    widget.setStyleSheet('QPushButton {font-size: 16px;}')
                else:
                    widget.setStyleSheet('QPushButton {color: red; font-size: 16px;}')
                self.day_schedule_widget_layout_list[idx_day].addWidget(widget)
                idx_period += 1
            idx_day += 1

    def toggleButton(self): #버튼 토글
        toggle_dic = {True: 'QPushButton {color: red; font-size: 16px;}', False: 'QPushButton {color: green; font-size: 16px;}'}
        widget = self.sender()
        idx = self.period_schedule_widget_list[self.today].index(widget)
        widget.setStyleSheet(toggle_dic[self.toggle_list[idx]])
        self.toggle_list[idx] = not self.toggle_list[idx]

    def anchorClicked(self, url):
        text = str(url.toString())
        openBrowser(text)

    def modifyMemo(self): #과목별 메모
        idx = self.period_schedule_widget_list[self.today].index(self.sender())
        try:
            current_memo = self.file_manage_class.readMemo(self.file_name)[self.schedule_dic[self.today][idx]]
        except KeyError:
            current_memo = ''
        self.memo_dialog = MemoWindow(target_widget=self.sender(), current_memo=current_memo, style_font=self.style_font)
        self.memo_dialog.memo_signal.connect(self.saveMemo)
        self.memo_dialog.show()

    @QtCore.pyqtSlot(tuple)
    def saveMemo(self, memo_data): #메모 저장하기
        target_widget = memo_data[0]
        memo = memo_data[1]
        idx = self.period_schedule_widget_list[self.today].index(target_widget)
        subject = self.schedule_dic[self.today][idx]
        self.file_manage_class.updateMemo(self.file_name, [subject, memo])

    @QtCore.pyqtSlot(tuple)
    def changeSchedule(self, all_data): #시간표 변경하기
        #all_data = (times, schedule_dic, running_t, break_t, lunch_t)
        times = all_data[0]; schedule_dic = all_data[1]; running_t = all_data[2]; break_t = all_data[3]; lunch_t = all_data[4]
        for day_idx in range(5):
            for period_idx in range(7):
                schedule_data = (self.day_string_list[day_idx], period_idx, schedule_dic[day_idx][period_idx])
                self.file_manage_class.updateSchedule(self.file_name, schedule_data)
        self.file_manage_class.updateTime(self.file_name, ['time', times])
        self.file_manage_class.updateTime(self.file_name, ['lunch_time', lunch_t])
        self.file_manage_class.updateTime(self.file_name, ['break_time', break_t])
        self.file_manage_class.updateTime(self.file_name, ['running_time', running_t])
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

    def openScheduleEditer(self): #시간표 수정 창 열기
        self.schedule_window = ScheduleWindow(self.schedule_dic, self.time_dic, self.style_font)  
        self.schedule_window.schedule_signal.connect(self.changeSchedule)
        self.schedule_window.show()

    def readSchedule(self): #시간표 읽어들이기
        self.schedule_dic = self.file_manage_class.readSchedule(self.file_name)

    @QtCore.pyqtSlot(Exception)
    def getTimeThreadExcept(self, e): #시간표 오류 예외 처리
        QtWidgets.QMessageBox.warning(self, '알림', '오류가 발생했습니다.\n시간표가 옳은지 확인하십시오.')
        self.openScheduleEditer()

    @QtCore.pyqtSlot(tuple) #current_period = (class_type, idx), class_type: 'yes' | 'break' | 'lunch' | 'no'
    def changePeriod(self, current_period): #현재 교시 표시
        label_text = ''; memo = ''; next_memo = ''
        if current_period[0] == 'yes':
            label_text = f'지금은 {current_period[1]+1}교시 {self.schedule_dic[self.today][current_period[1]]} 시간입니다.'
            try:
                memo = self.file_manage_class.readMemo(self.file_name)[self.schedule_dic[self.today][current_period[1]]] + '\n'
            except: pass
        elif current_period[0] == 'break':
            label_text = '지금은 쉬는 시간입니다'
        elif current_period[0] == 'lunch':
            label_text = '지금은 점심 시간입니다'
        elif current_period[0] == 'before':
            label_text = '지금은 수업 시간 전입니다'
        elif current_period[0] == 'after':
            label_text = '수업이 끝났습니다'
        try:
            next_memo = self.file_manage_class.readMemo(self.file_name)[self.schedule_dic[self.today][current_period[1]+1]]
        except: pass
        else:
            memo += '<hr><strong style="text-align: center">다음 교시 메모</strong><hr>' + next_memo
        is_open = False
        if label_text != self.current_txt:
            notification.notify('알림', label_text, app_icon=logo_ico, app_name='온라인 수업 일정 도우미')
            is_open = True
        memo = getMemoAndOpenBrowser(memo, is_open, current_period[0])
        self.current_txt = label_text
        self.label_current_time.setText(label_text)
        self.text_browser_memo.setHtml(memo)

    def getPeriod(self): #시간 체크 스레드 실행
        self.time_dic = self.file_manage_class.readTime(self.file_name)
        self.time_thread = TimeThread()
        self.time_thread.time_list = self.time_dic['time']
        self.time_thread.lunch_time = self.time_dic['lunch_time']
        self.time_thread.break_time = self.time_dic['break_time']
        self.time_thread.running_time = self.time_dic['running_time']
        self.time_thread.start()
        self.time_thread.time_signal.connect(self.changePeriod)
        self.time_thread.except_signal.connect(self.getTimeThreadExcept)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '종료', '프로그램을 종료하시겠습니까?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()