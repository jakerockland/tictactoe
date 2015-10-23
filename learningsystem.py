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
# x5: number of instances of possibilities with 1 X and two empty spaces
# x6: number of instances of possibilities with 1 O and two empty spaces
# x7: number of X's on board
# x8: number of O's on board

import copy
import random

class ExperimentGenerator:
    def __init__(self):
        self.board = self.newGame()
        self.history = [copy.deepcopy(self.board)]

    def newGame(self):
        board = [ [' ',' ',' '],
                  [' ',' ',' '],
                  [' ',' ',' '] ]
        return board

    def getBoard(self):
        return self.board

    def setBoard(self,board):
        self.board = board
        self.history.append(copy.deepcopy(self.board))

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

    def getPossibilities(self, board = None):
        if board is None:
            board = self.board
        possibilities = []
        for row in board:
            possibilities.append(row)
        for x in range(3):
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

    def makeMove(self,x,y,token):
        if (y in range(3)) and (x in range(3)) and (self.board[y][x] == ' '):
            self.board[y][x] = token
            self.history.append(copy.deepcopy(self.board))
            return True
        else:
            return False

    def getXSuccessors(self):
        successors = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    successor = copy.deepcopy(self.board)
                    successor[i][j] = 'X'
                    successors.append(successor)
        return successors

    def getOSuccessors(self):
        successors = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    successor = copy.deepcopy(self.board)
                    successor[i][j] = 'O'
                    successors.append(successor)
        return successors

    def printBoard(self,board = None):
        if board is None:
            board = self.board
        print('\n' + board[0][0] + '|' + board[0][1] + '|' + board[0][2])
        print('-----\n' + board[1][0] + '|' + board[1][1] + '|' + board[1][2])
        print('-----\n' + board[2][0] + '|' + board[2][1] + '|' + board[2][2] + '\n')

class PerformanceSystem:
    def __init__(self,game,mode = 'X',hypothesis = [0.0] * 9):
        self.game = game
        self.hypothesis = hypothesis
        self.mode = mode
        self.update_constant = 0.1

    def getUpdateConstant(self):
        return self.update_constant

    def setUpdateConstant(self, constant):
        self.update_constant = update_constant

    def getGame(self):
        return self.game

    def setGame(self,game):
        self.game = game

    def getMode(self):
        return self.mode

    def setMode(self,mode):
        self.mode = mode

    def getHypothesis(self):
        return self.hypothesis

    def setHypothesis(self, hypothesis):
        self.hypothesis = hypothesis

    def getFeatures(self, board = None):
        if board is None:
            board = self.game.getBoard()
        possibilities = self.game.getPossibilities()
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0
        x5 = 0
        x6 = 0
        x7 = 0
        x8 = 0
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
            elif X_count == 1 and O_count == 0:
                x5 += 1
            elif O_count == 1 and X_count == 0:
                x6 += 1
            x7 = X_count
            x8 = O_count
        return x1,x2,x3,x4,x5,x6,x7,x8

    def performEvaluation(self, board = None):
        if board is None:
            board = self.game.getBoard()
        x1,x2,x3,x4,x5,x6,x7,x8 = self.getFeatures(board)
        w0,w1,w2,w3,w4,w5,w6,w7,w8 = self.hypothesis
        return w0 + w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5 + w6*x6 + w7*x7 + w8*x8

    def chooseMove(self):
        if self.mode == 'X':
            successors = self.game.getXSuccessors()
        else:
            successors = self.game.getOSuccessors()
        best_successor = successors[0]
        best_value = self.performEvaluation(best_successor)
        for successor in successors:
            value = self.performEvaluation(successor)
            if value > best_value:
                best_value = value
                best_successor = successor
        self.game.setBoard(best_successor)

    def chooseRandom(self):
        if self.mode == 'X':
            successors = self.game.getXSuccessors()
        else:
            successors = self.game.getOSuccessors()
        self.game.setBoard(successors[random.randint(0,len(successors)-1)])

class Critic:
    def __init__(self,performance_system):
        self.performance_system = performance_system
        self.game = performance_system.getGame()

    def getTrainingExamples(self):
        history = self.game.getHistory()
        training_examples = []
        for i in range(len(history)):
            mode = self.performance_system.getMode()
            winner = self.game.getWinner(history[i])
            empty_squares = self.game.numEmptySquares(history[i])
            board_features = self.performance_system.getFeatures(history[i])
            if winner == mode:
                training_examples.append([board_features,100])
            elif winner is None:
                if empty_squares == 0:
                    training_examples.append([board_features,0])
                else:
                    if i+2 >= len(history):
                        if self.game.getWinner(history[len(history)-1]) is None:
                            training_examples.append([board_features,0])
                        else:
                            training_examples.append([board_features,-100])
                    else:
                        training_examples.append([board_features,self.performance_system.performEvaluation(history[i+2])])
            else:
                training_examples.append([board_features,-100])
        return training_examples

class Generalizer:
    def __init__(self,performance_system):
        self.performance_system = performance_system
        self.update_constant = performance_system.getUpdateConstant()
        self.hypothesis = self.performance_system.getHypothesis()

    def updateHypothesis(self,history,training_examples):
        for i in range(len(history)):
            w0,w1,w2,w3,w4,w5,w6,w7,w8 = self.hypothesis
            v_eval = self.performance_system.performEvaluation(history[i])
            x1,x2,x3,x4,x5,x6,x7,x8 = training_examples[i][0]
            v_train = training_examples[i][1]
            w0 = w0 + self.update_constant*(v_train - v_eval)
            w1 = w1 + self.update_constant*(v_train - v_eval)*x1
            w2 = w2 + self.update_constant*(v_train - v_eval)*x2
            w3 = w3 + self.update_constant*(v_train - v_eval)*x3
            w4 = w4 + self.update_constant*(v_train - v_eval)*x4
            w5 = w5 + self.update_constant*(v_train - v_eval)*x5
            w6 = w6 + self.update_constant*(v_train - v_eval)*x6
            w7 = w7 + self.update_constant*(v_train - v_eval)*x7
            w8 = w8 + self.update_constant*(v_train - v_eval)*x8
            return w0,w1,w2,w3,w4,w5,w6,w7,w8
