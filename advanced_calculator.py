import tkinter as tk
import math
import os

LARGE_FONT_STYLE = ('Arial', 40, 'bold')
MEDIUM_FONT_STYLE = ('Arial', 25, 'bold')
SMALL_FONT_STYLE = ('Arial', 16)
SMALL_FONT_STYLE_BOLD = ('Arial', 16, 'bold')
DIGITS_FONT_STYLE = ('Arial', 24, 'bold')
DEFAULT_FONT_STYLE = ('Arial', 20)

OFF_WHITE = '#F8FAFF'
WHITE = '#FFFFFF'
LIGHT_BLUE = '#CCEDFF'
LIGHT_GRAY = '#F5F5F5'
BLACK = '#000000'
LABEL_COLOR = '#25265E'


class AdvancedCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('375x667')
        self.window.title('Advanced Calculator')
        self.window.resizable(0, 0)

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_expression = ''
        self.current_expression = ''
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (2, 1), 8: (2, 2), 9: (2, 3),
            4: (3, 1), 5: (3, 2), 6: (3, 3),
            1: (4, 1), 2: (4, 2), 3: (4, 3),
            '.': (5, 1), 0: (5, 2)
        }
        self.create_digit_buttons()
        self.operators = {
            '/': '\u00F7', '*': '\u00D7', '-': '-', '+': '+'
        }
        self.create_operator_buttons()
        self.create_special_buttons()
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(5, weight=1)
        self.buttons_frame.rowconfigure(6, weight=1)
        self.additional_buttons = {
            'tan': (1, 1),
            'cos': (1, 2),
            'sin': (1, 3)
        }
        self.create_additional_buttons()
        for x in range(1, 5):
            self.buttons_frame.columnconfigure(x, weight=1)
            self.buttons_frame.rowconfigure(x, weight=1)
        self.trigonometric_flag = False
        self.converter = {
            'converter': (6, 1)
        }
        self.bind_keys()
        self.create_converter_button()
        self.default_screen()

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill='both')
        return frame

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.W, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda l=digit: self.get_digit(l))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_operator_buttons(self):
        i = 1
        for operator, symbol in self.operators.items():
            button = tk.Button(self.buttons_frame, text=str(symbol), bg=WHITE, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda l=operator: self.get_operator(l))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_del_button()
        self.create_log_button()
        self.create_equals_button()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text='clear', bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_del_button(self):
        button = tk.Button(self.buttons_frame, text='del', bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.del_func)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def create_log_button(self):
        button = tk.Button(self.buttons_frame, text='log', bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.trigonometric)
        button.grid(row=0, column=3, columnspan=2, sticky=tk.NSEW)

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text='=', bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=5, column=3, columnspan=2, sticky=tk.NSEW)

    def create_additional_buttons(self):
        for name, grid_value in self.additional_buttons.items():
            button = tk.Button(self.buttons_frame, text=str(name), bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda l=name: self.trigonometric(l))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_converter_button(self):
        for name, grid_value in self.converter.items():
            button = tk.Button(self.buttons_frame, text=str(name), bg=BLACK, fg=WHITE, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=self.converter_func)
            button.grid(row=grid_value[0], column=grid_value[1], columnspan=4, sticky=tk.NSEW)

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        if len(self.current_expression) <= 11:
            self.label.config(font=LARGE_FONT_STYLE)
        elif 12 <= len(self.current_expression) < 17:
            self.label.config(font=MEDIUM_FONT_STYLE)
        elif len(self.current_expression) > 17:
            self.label.config(font=SMALL_FONT_STYLE_BOLD)
        else:
            self.label.config(font=SMALL_FONT_STYLE_BOLD)
            self.label.config(text=self.current_expression[:30])
        self.label.config(text=self.current_expression)

    def clear(self):
        self.total_expression = ''
        self.current_expression = ''
        self.update_total_label()
        self.update_label()
        self.trigonometric_flag = False
        self.default_screen()

    def del_func(self):
        str_length = len(self.current_expression)
        self.current_expression = self.current_expression[:str_length - 1]
        self.update_label()

    def get_digit(self, value):
        if self.current_expression == '0':
            self.current_expression = ''
            self.update_label()
        self.current_expression += str(value)
        self.update_label()

    def get_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ''
        self.update_total_label()
        self.update_label()

    def trigonometric(self, name='log'):
        global trigonometric_func
        trigonometric_func = name
        self.trigonometric_flag = True
        self.total_expression = ''
        self.total_expression = name + ' '
        self.update_total_label()
        self.current_expression = ''
        self.update_label()

    def evaluate(self):
        try:
            if self.trigonometric_flag:
                num = float(self.current_expression)
                if trigonometric_func == 'tan':
                    result = math.tan(num * math.pi / 180)
                    self.total_expression += self.current_expression
                    self.update_total_label()
                    self.current_expression = str(result)
                    self.update_label()
                elif trigonometric_func == 'cos':
                    result = math.cos(num * math.pi / 180)
                    self.total_expression += self.current_expression
                    self.update_total_label()
                    self.current_expression = str(result)
                    self.update_label()
                elif trigonometric_func == 'sin':
                    result = math.sin(num * math.pi / 180)
                    self.total_expression += self.current_expression
                    self.update_total_label()
                    self.current_expression = str(result)
                    self.update_label()
                elif trigonometric_func == 'log':
                    result = math.log10(num)
                    self.total_expression += self.current_expression
                    self.update_total_label()
                    self.current_expression = str(result)
                    self.update_label()
            else:
                self.total_expression += self.current_expression
                self.update_total_label()
                self.current_expression = str(eval(self.total_expression))
                self.update_label()
                self.total_expression = ''
        except Exception:
            self.current_expression = 'Error!!'
        finally:
            self.update_label()

    def bind_keys(self):
        self.window.bind('<Return>', lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.get_digit(digit))
        for key in self.operators:
            self.window.bind(str(key), lambda event, operator=key: self.get_operator(operator))

    def converter_func(self):
        self.window.destroy()
        os.system('python3 converter_with_UI.py')

    def default_screen(self):
        self.current_expression = '0'
        self.update_label()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = AdvancedCalculator()
    calc.run()
