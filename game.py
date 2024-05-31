import sys
import random
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from functools import partial

board_state = [''] * 9
move_counter = 0
game_won = False
game_buttons = []
is_dragging = False

def init():
    global main_window, layout_vertical, layout_grid, main_widget, game_buttons, result_label
    main_window = QtWidgets.QMainWindow()
    main_window.setAttribute(Qt.WA_TranslucentBackground, True)

    main_widget = QtWidgets.QWidget()
    layout_vertical = QtWidgets.QVBoxLayout()
    layout_vertical.setAlignment(QtCore.Qt.AlignTop)
    main_widget.setLayout(layout_vertical)
    main_window.setCentralWidget(main_widget)

    layout_grid = QtWidgets.QGridLayout()
    layout_grid.setContentsMargins(20, 20, 20, 20)
    layout_vertical.addLayout(layout_grid)

    result_label = QtWidgets.QLabel(main_widget)
    result_label.setAlignment(QtCore.Qt.AlignCenter)
    result_label.setStyleSheet("color: white; font-size: 16px;")
    layout_vertical.addWidget(result_label)

    restart_button = QtWidgets.QPushButton("RESTART")
    restart_button.setFixedSize(100, 40)
    restart_button.clicked.connect(restart_game)
    restart_button.setStyleSheet("color: white; border: 2px solid white; font-size: 15px;")

    layout_vertical.addSpacing(10)
    layout_horizontal = QtWidgets.QHBoxLayout()
    layout_horizontal.addWidget(restart_button)
    layout_vertical.addLayout(layout_horizontal)

    for index in range(9):
        btn = QtWidgets.QPushButton()
        btn.setFixedSize(80, 80)
        btn.setStyleSheet("QPushButton {background-color: white; font-size: 25px; color: black;}")
        layout_grid.addWidget(btn, index // 3, index % 3)
        btn.clicked.connect(partial(handle_move, btn, index))
        game_buttons.append(btn)


def handle_move(btn, index):
    global move_counter
    if board_state[index] == '':
        board_state[index] = 'X'
        btn.setText("X")
        btn.setEnabled(False)
        move_counter += 1

        if evaluate_game('X'):
            return

        if move_counter < 9:
            make_next_move()

def make_next_move():
    global move_counter
    index = find_next_move()
    if index is not None:
        board_state[index] = 'O'
        btn = game_buttons[index]
        btn.setText("O")
        btn.setEnabled(False)
        move_counter += 1
        evaluate_game('O')

def find_next_move():
    for index in range(9):
        if board_state[index] == '':
            board_state[index] = 'O'
            if check_winner('O'):
                return index
            board_state[index] = ''

    for index in range(9):
        if board_state[index] == '':
            board_state[index] = 'X'
            if check_winner('X'):
                board_state[index] = ''
                return index
            board_state[index] = ''

    empty_indexes = [idx for idx in range(9) if board_state[idx] == '']
    selected_index = random.choice(empty_indexes)
    print(selected_index)
    
    return selected_index

def evaluate_game(player):
    if move_counter > 4 and check_winner(player):
        end_game(player)
        return True

    if move_counter == 9 and not game_won:
        result_label.setText("Game Drawn!")
        disable_all_buttons()
        return True

    return False

def check_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board_state[i] == player for i in condition):
            return True
    return False

def end_game(player):
    global game_won
    result_label.setText(f"{player} Wins!")
    disable_all_buttons()
    game_won = True

def enable_all_buttons():
    for btn in game_buttons:
        btn.setEnabled(True)

def disable_all_buttons():
    for btn in game_buttons:
        btn.setEnabled(False)

def restart_game():
    global board_state, move_counter, game_won

    result_label.setText("")

    board_state = [''] * 9
    move_counter = 0
    game_won = False
    
    for btn in game_buttons:
        btn.setText("")
    
    enable_all_buttons()

if __name__ == '__main__':
    global app
    app = QtWidgets.QApplication(sys.argv)
    
    init()

    main_window.show()
    sys.exit(app.exec_())
