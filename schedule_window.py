from PyQt5 import QtWidgets, QtCore, uic
from util import resource_path

schedule_form_class = uic.loadUiType(resource_path('./resources/ui/ui_schedule_window.ui'))[0]

class ScheduleWindow(QtWidgets.QDialog, schedule_form_class):
    schedule_signal = QtCore.pyqtSignal(tuple)
    def __init__(self, schedule_lists, time_dic, style_font):
        super().__init__()
        self.setupUi(self)
        self.day_string_list = ['mon', 'tue', 'wed', 'thu', 'fri']
        self.time_dic = time_dic
        self.schedule_lists = schedule_lists
        self.schedule_widgets = []
        self.line_edit_running_t.setText(str(self.time_dic['running_time']))
        self.line_edit_break_t.setText(str(self.time_dic['break_time']))
        self.line_edit_lunch_t.setText(':'.join(map(str, self.time_dic['lunch_time'])))
        self.setFont(style_font)
        for x in range(6):
            self.schedule_widgets.append([])
            for y in range(7):
                line_edit = QtWidgets.QLineEdit()
                line_edit.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
                if x == 0:
                    line_edit.setText(':'.join(map(str, self.time_dic['time'][y])))
                else:
                    line_edit.setText(schedule_lists[self.day_string_list[x-1]][y])
                line_edit.setFont(style_font)
                self.schedule_widgets[-1].append(line_edit)
                self.layout_schedule.addWidget(line_edit, y, x)
        self.btn_save.clicked.connect(self.saveData)

    def saveData(self):
        try:
            schedules = []
            for i in self.schedule_widgets[1:]:
                schedules.append([])
                for j in i:
                    schedules[-1].append(j.text())
            times = []
            for i in self.schedule_widgets[0]:
                t = list(map(int, i.text().split(':')))
                '''
                if len(t) != 2:
                    raise Exception
                '''
                times.append(t)

            running_t = int(self.line_edit_running_t.text())
            break_t = int(self.line_edit_break_t.text())
            lunch_t = list(map(int, self.line_edit_lunch_t.text().split(':')))
            if len(lunch_t) != 2:
                raise Exception
            #changeSchedule(self, times, schedules, running_t, break_t, lunch_t):
            self.schedule_signal.emit((times, schedules, running_t, break_t, lunch_t))
            self.close()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, '안내', '오류가 발생했습니다.\n알맞게 수정했는지 확인하십시오.')
