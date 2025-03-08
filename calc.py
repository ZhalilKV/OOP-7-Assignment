from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.uic import loadUi


class Calculator:
    """Model: Handles calculator logic and state"""

    def __init__(self):
        self.expression = ""

    def add_to_expression(self, char):
        self.expression += str(char)

    def remove_last_character(self):
        self.expression = self.expression[:-1]

    def clear_expression(self):
        self.expression = ""

    def calculate(self):
        try:
            result = eval(self.expression)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"
        except:
            return "Error: Invalid expression"

    def get_expression(self):
        return self.expression


class CalculatorWindow(QMainWindow):
    """Controller: Manages UI interactions and model communication"""

    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.new_input = False
        self.init_ui()
        self.connect_buttons()

    def init_ui(self):
        loadUi('calc.ui', self)
        self.display.setReadOnly(True)

    def connect_buttons(self):
        # Connect all calculator buttons to handler
        for btn in self.findChildren(QPushButton):
            if btn.objectName().startswith('btn_'):
                btn.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        char = self.sender().text()

        if char == '=':
            self.handle_calculate()
        elif char == 'C':
            self.handle_clear()
        else:
            if self.new_input:
                if char.isdigit():
                    self.calculator.clear_expression()
                    self.new_input = False
                elif char in '+-*/':
                    self.new_input = False

            self.calculator.add_to_expression(char)
            self.display.setText(self.calculator.get_expression())

    def handle_clear(self):
        self.calculator.clear_expression()
        self.display.clear()
        self.new_input = False

    def handle_calculate(self):
        result = self.calculator.calculate()

        if isinstance(result, str):  # Error message
            self.display.setText(result)
            self.calculator.clear_expression()
            self.new_input = True
        else:
            self.display.setText(str(result))
            self.calculator.expression = str(result)
            self.new_input = True