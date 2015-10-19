# This program is an machine learning experiment training a program to play the game of tic-tac-toe
# Based on an excercise from Machine Learning by Thomas Mitchell (1997)
# By: Jacob Rockland
#
# ' ' represents an unfilled square
# 'X' represents an X
# 'O' represents an O
#
# x1: number of instances of possibilities with 2 X's and an empty space
# x2: number of instances of possibilities with 2 O's and an empty space
# x3: number of instances of possibilities with 3 X's (game over)
# x4: number of instances of possibilities with 3 O's (game over)
# x5: number of empty squares

import copy
import random

class ExperimentGenerator:
    def __init__(self):
        self.board = self.newBoard()
        self.history = [copy.deepcopy(self.board)]

    def newBoard(self):
    board = [ [' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' '] ]
    return board

    def getBoard(self):
        return self.board

    def setBoard(self,board):
        self.board = board
        self.history.append(copy.deepcopy(self.board))

    def printBoard(self,board = None):
        if board is None:
            board = self.board
        print('\n' + board[0][0] + '|' + board[0][1] + '|' + board[0][2])
        print('-----' + board[1][0] + '|' + board[1][1] + '|' + board[1][2])
        print('-----' + board[2][0] + '|' + board[2][1] + '|' + board[2][2] + '\n')

    def getHistory(self):
        return self.history

    def numEmptySquares(self, board = None):
        if board is None:
            board = self.board
        num = 0
        for row in board:
            for square in row:
                if square == ' ':
                    num += 1
        return num

    def getWinner(self, board = None):
        if board is None:
            board = self.board
        possibilities = self.getPossibilities()
        for possibility in possibilities:
            X_count = 0
            O_count = 0
            for square in possibility:
                if square == 'X':
                    X_count += 1
                elif square == 'O':
                    O_count += 1
            if X_count == 3:
                return 'X'
            elif O_count == 3:
                return 'O'
        return None

    def getFeatures(self, board = None):
        if board is None:
            board = self.board
        possibilities = self.getPossibilities()
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0
        x5 = self.numEmptySquares()
        for possibility in possibilities:
            X_count = 0
            O_count = 0
            for square in possibility:
                if square == 'X':
                    X_count += 1
                elif square == 'O':
                    O_count += 1
            if X_count == 2 and O_count == 0:
                x1 += 1
            elif X_count == 0 and O_count == 2:
                x2 += 1
            elif X_count == 3:
                x3 += 1
            elif O_count == 3:
                x4 += 1
        return x1,x2,x3,x4,x5

    def getPossibilities(self, board = None):
        if board is None:
            board = self.board
        possibilities = []
        for row in board:
            possibilities.append(row)
        for x in range(0,3):
            column = []
            column.append(board[0][x])
            column.append(board[1][x])
            column.append(board[2][x])
            possibilities.append(column)
        diagonal_1 = []
        diagonal_1.append(board[2][0])
        diagonal_1.append(board[1][1])
        diagonal_1.append(board[0][2])
        possibilities.append(diagonal_1)
        diagonal_2 = []
        diagonal_2.append(board[0][0])
        diagonal_2.append(board[1][1])
        diagonal_2.append(board[2][2])
        possibilities.append(diagonal_2)
        return possibilities

    def getXSuccessors(self):
        successors = []
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == ' ':
                    successor = copy.deepcopy(self.board)
                    successor[i][j] = 'X'
                    successors.append(successor)
        return successors

    def getOSuccessors(self):
        successors = []
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == ' ':
                    successor = copy.deepcopy(self.board)
                    successor[i][j] = 'O'
                    successors.append(successor)
        return successors

    def makeMove(self,x,y,token,add_history = False):
        self.board[y][x] = token
        if add_history:
            self.history.append(copy.deepcopy(self.board))
