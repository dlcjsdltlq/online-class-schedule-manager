from PyQt5 import QtCore
import datetime
import time

class TimeThread(QtCore.QThread):
    time_signal = QtCore.pyqtSignal(tuple) #형식: [class_type, idx], class_type: 'yes', 'break', 'lunch', 'no'
    except_signal = QtCore.pyqtSignal(Exception)
    def run(self):
        try:
            lunch_start_t = (self.lunch_time[0]*60 + self.lunch_time[1])*60
            lunch_end_t = lunch_start_t + (self.running_time + self.break_time)*60
            first_t = (self.time_list[0][0]*60 + self.time_list[0][1])*60
            last_t = (self.time_list[-1][0]*60 + self.time_list[-1][1] + self.running_time)*60
            for idx in range(len(self.time_list)):
                start_t = (self.time_list[idx][0]*60 + self.time_list[idx][1])*60
                end_t = start_t + self.running_time*60     
                b_end_t = end_t + self.break_time*60
                while True:
                    now_t = datetime.datetime.now()
                    now_t = (now_t.hour*60 + now_t.minute)*60 + now_t.second
                    signal_data : tuple
                    if (now_t < first_t) | (now_t > last_t): #수업 시간이 아닐 경우
                        signal_data = ('no', None)
                    elif (start_t < now_t) & (now_t < end_t): #수업 시간일 경우
                        signal_data = ('yes', idx)
                    elif (end_t < now_t) & (now_t < b_end_t): #쉬는 시간일 경우
                        signal_data = ('break', idx)
                    elif (end_t == lunch_start_t) & ((lunch_start_t < now_t) & (now_t < lunch_end_t)): #점심 시간일 경우
                        signal_data = ('lunch', idx)
                    elif (now_t > b_end_t): #다음 시간이 시작했을 경우
                        break
                    self.time_signal.emit(signal_data)
                    time.sleep(2)
        except Exception as E:
            self.except_signal.emit(E)