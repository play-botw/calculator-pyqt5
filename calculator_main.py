import sys
from PyQt5.QtWidgets import *
import PyQt5.QtGui
import math


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # layout_display와 layout_button을 생성
        layout_display = QGridLayout()
        layout_button = QGridLayout()

        # 숫자 입력과 답 출력을 위한 QLineEdit 위젯 생성
        self.display = QLineEdit("")

        # 숫자 입력을 실수 범위로 제한
        self.display.setValidator(PyQt5.QtGui.QDoubleValidator(self))

        # layout_display 레이아웃에 display 추가
        layout_display.addWidget(self.display)

        # 연산자와 피연산자를 저장할 변수 생성
        self.pre_operator = ""
        self.pre_operend = 0

        # 단항 연산자 버튼 생성
        button_inverse = QPushButton("1/x")
        button_power = QPushButton("x^2")
        button_root = QPushButton("√x")
        button_sign = QPushButton("±")

        # 단항 연산자 버튼을 클릭했을 때, 함수 호출
        button_inverse.clicked.connect(
            lambda state, operator="1/x": self.operate_unary(operator))
        button_power.clicked.connect(
            lambda state, operator="x^2": self.operate_unary(operator))
        button_root.clicked.connect(
            lambda state, operator="root(x)": self.operate_unary(operator))
        button_sign.clicked.connect(
            lambda state, operator="sign": self.operate_unary(operator))

        # 이항 연산자 버튼 생성
        button_add = QPushButton("＋")
        button_subtract = QPushButton("－")
        button_multiply = QPushButton("×")
        button_division = QPushButton("÷")
        button_modular = QPushButton("%")

        # 이항 연산자 버튼을 클릭했을 때, 함수 호출
        button_add.clicked.connect(
            lambda state, operator="+": self.operate_binary(operator))
        button_subtract.clicked.connect(
            lambda state, operator="-": self.operate_binary(operator))
        button_multiply.clicked.connect(
            lambda state, operator="*": self.operate_binary(operator))
        button_division.clicked.connect(
            lambda state, operator="/": self.operate_binary(operator))

        # 소수점 버튼 생성
        button_dot = QPushButton(".")

        # 소수점 버튼을 클릭했을 때, 시그널 설정
        button_dot.clicked.connect(
            lambda state, num=".": self.display_number(num))

        # 기능 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_clear_entry = QPushButton("CE")
        button_backspace = QPushButton("Backspace")

        # 기능 버튼을 클릭했을 때, 시그널 설정
        button_equal.clicked.connect(self.equal)
        button_clear.clicked.connect(self.clear)
        button_clear_entry.clicked.connect(self.clear_entry)
        button_backspace.clicked.connect(self.backspace)

        # layout_button 레이아웃에 각종 버튼 추가
        layout_button.addWidget(button_modular, 0, 0)
        layout_button.addWidget(button_clear_entry, 0, 1)
        layout_button.addWidget(button_clear, 0, 2)
        layout_button.addWidget(button_backspace, 0, 3)

        layout_button.addWidget(button_inverse, 1, 0)
        layout_button.addWidget(button_power, 1, 1)
        layout_button.addWidget(button_root, 1, 2)
        layout_button.addWidget(button_division, 1, 3)

        layout_button.addWidget(button_multiply, 2, 3)

        layout_button.addWidget(button_subtract, 3, 3)

        layout_button.addWidget(button_add, 4, 3)

        layout_button.addWidget(button_sign, 5, 0)
        layout_button.addWidget(button_dot, 5, 2)
        layout_button.addWidget(button_equal, 5, 3)

        # 숫자 버튼을 생성하고, layout_button 레이아웃에 추가
        # 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(
                lambda state, num=number: self.display_number(num))
            if number > 0:
                a, b = divmod(number-1, 3)
                layout_button.addWidget(number_button_dict[number], 4-a, b)
            elif number == 0:
                layout_button.addWidget(number_button_dict[number], 5, 1)

        # 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_display)
        main_layout.addLayout(layout_button)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def display_number(self, num):
        operend = self.display.text()
        operend += str(num)
        self.display.setText(operend)

    def operate_unary(self, operator):
        operend = float(self.display.text())
        if (operator == "1/x"):
            operend = 1/operend
        elif (operator == "x^2"):
            operend = math.pow(operend, 2)
        elif (operator == "root(x)"):
            operend = math.sqrt(operend)
        elif (operator == "sign"):
            operend = -(operend)
        self.display.setText(str(operend))

    def operate_binary(self, operator):
        operend = float(self.display.text())
        if (self.pre_operator == "+"):
            self.pre_operend = self.pre_operend + operend
        elif (self.pre_operator == "-"):
            self.pre_operend = self.pre_operend - operend
        elif (self.pre_operator == "*"):
            self.pre_operend = self.pre_operend * operend
        elif (self.pre_operator == "/"):
            self.pre_operend = self.pre_operend / operend
        elif (self.pre_operator == "%"):
            self.pre_operend = self.pre_operend % operend
        else:
            self.pre_operend = operend
        self.pre_operator = operator
        self.display.setText("")

    def equal(self):
        if (self.display.text() == ""):
            # 이항 연산자 버튼을 누른 후, 바로 = 버튼을 눌렀을 때,
            # 이항 연산자 버튼을 누르기 전에 입력한 값을 피연산자로 한 번 더 사용한다.
            operend = self.pre_operend
        else:
            operend = float(self.display.text())

        if (self.pre_operator == "+"):
            self.pre_operend = self.pre_operend + operend
        elif (self.pre_operator == "-"):
            self.pre_operend = self.pre_operend - operend
        elif (self.pre_operator == "*"):
            self.pre_operend = self.pre_operend * operend
        elif (self.pre_operator == "/"):
            self.pre_operend = self.pre_operend / operend
        elif (self.pre_operator == "%"):
            self.pre_operend = self.pre_operend % operend
        else:
            self.pre_operend = operend
        self.pre_operator = ""
        self.display.setText(str(self.pre_operend))

    def clear(self):
        self.display.setText("")
        self.pre_operator = ""
        self.pre_operend = 0

    def clear_entry(self):
        self.display.setText("")

    def backspace(self):
        operend = self.display.text()
        operend = operend[:-1]
        self.display.setText(operend)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
