import sys
from PyQt5.QtWidgets import *


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_button = QGridLayout()
        layout_display = QGridLayout()

        # 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        display = QLineEdit("")

        # layout_display 레이아웃에 수식, 답 위젯을 추가
        layout_display.addWidget(display)

        # 사칙연상 버튼 생성
        button_add = QPushButton("＋")
        button_subtract = QPushButton("－")
        button_multiply = QPushButton("×")
        button_division = QPushButton("÷")
        button_modular = QPushButton("%")
        button_inverse = QPushButton("1/x")
        button_power = QPushButton("x^2")
        button_root = QPushButton("√x")

        # 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_add.clicked.connect(
            lambda state, operator="+": self.button_operator_clicked(operator))
        button_subtract.clicked.connect(
            lambda state, operator="-": self.button_operator_clicked(operator))
        button_multiply.clicked.connect(
            lambda state, operator="*": self.button_operator_clicked(operator))
        button_division.clicked.connect(
            lambda state, operator="/": self.button_operator_clicked(operator))

        # =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_clear_entry = QPushButton("CE")
        button_backspace = QPushButton("Backspace")

        # =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        # 각종 연산버튼을 layout_button 레이아웃에 추가
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

        layout_button.addWidget(button_equal, 5, 3)

        # 숫자 버튼 생성하고, layout_button 레이아웃에 추가
        # 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num=number:
                                                       self.number_button_clicked(num))
            if number > 0:
                a, b = divmod(number-1, 3)
                layout_button.addWidget(number_button_dict[number], 4-a, b)
            elif number == 0:
                layout_button.addWidget(number_button_dict[number], 5, 1)

        # 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(
            lambda state, num=".": self.number_button_clicked(num))
        layout_button.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(
            lambda state, num="00": self.number_button_clicked(num))
        layout_button.addWidget(button_double_zero, 3, 0)

        # 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_display)
        main_layout.addLayout(layout_button)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        entry = self.entry.text()
        entry += str(num)
        self.entry.setText(entry)

    def button_operator_clicked(self, operator):
        entry = self.entry.text()
        entry += operator
        self.entry.setText(entry)

    def button_equal_clicked(self):
        entry = self.entry.text()
        solution = eval(entry)
        self.solution.setText(str(solution))

    def button_clear_clicked(self):
        self.entry.setText("")
        self.solution.setText("")

    def button_backspace_clicked(self):
        entry = self.entry.text()
        entry = entry[:-1]
        self.entry.setText(entry)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
