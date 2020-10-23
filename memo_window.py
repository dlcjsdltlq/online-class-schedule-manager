from PyQt5 import QtWidgets, QtCore, uic
from util import resource_path

memo_form_class = uic.loadUiType(resource_path('./resources/ui/ui_memo_window.ui'))[0]

class MemoWindow(QtWidgets.QDialog, memo_form_class):
    memo_signal = QtCore.pyqtSignal(tuple)
    def __init__(self, target_widget, current_memo, style_font):
        super().__init__()
        self.setupUi(self)
        self.setFont(style_font)
        self.target_widget = target_widget
        self.text_edit_memo.setText(current_memo)
        self.btn_save_memo.clicked.connect(self.saveMemo)

    def saveMemo(self):
        text = self.text_edit_memo.toPlainText()
        self.memo_signal.emit((self.target_widget, text))
        self.close()
