# This program is an machine learning experiment training a program to play the game of tic-tac-toe
# Based on an excercise from Machine Learning by Thomas Mitchell (1997)
# By: Jacob Rockland
#
# ' ' represents an unfilled square
# 'X' represents an X
# 'O' represents an O

import random
import learningsystem

def train(iterations = 10000, mode = 'fixed'):
    game = learningsystem.ExperimentGenerator()
    learner = learningsystem.PerformanceSystem(game,'X')
    trainer = learningsystem.PerformanceSystem(game,'O')

    learner_wins = 0
    trainer_wins = 0
    total_games = 0

    for i in range(iterations):
        game = learningsystem.ExperimentGenerator()
        learner.setGame(game)
        trainer.setGame(game)
        start_turn = random.randint(0,1)
        if start_turn == 1:
            player_turn = 'X'
        else:
            player_turn = 'O'
        # print(player_turn + " is playing first.")
        while (game.getWinner() is None) and (game.numEmptySquares() > 0):
            if player_turn == 'X':
                learner.chooseMove()
                player_turn = 'O'
            else:
                if mode == 'fixed':
                    trainer.chooseFixed()
                else:
                    trainer.chooseRandom()
                player_turn = 'X'

        winner = game.getWinner()
        # game.printBoard()
        # if winner is None:
        #     print("Draw!")
        # else:
        #     print(winner + " won!\n")
        if winner == 'X':
            learner_wins += 1
        elif winner == 'O':
            trainer_wins += 1
        total_games += 1
        print("Games Played: " + str(total_games))
        print("% Games Won: " + str(learner_wins / float(total_games) * 100))
        print("% Games Lost: " + str(trainer_wins / float(total_games) * 100))
        print("% Cats Games: " + str((total_games - learner_wins - trainer_wins) / float(total_games) * 100) + "\n")

        critic = learningsystem.Critic(learner)
        generalizer = learningsystem.Generalizer(learner)
        training_examples = critic.getTrainingExamples()
        learner.setHypothesis(generalizer.updateHypothesis(game.getHistory(),training_examples))
    return learner, learner_wins, trainer_wins, total_games

def main():
    iterations = int(input("Enter number of training games to play: "))
    print("Training computer...\n")
    # computer, learner_wins, trainer_wins, total_games = train(iterations,"random")
    computer, learner_wins, trainer_wins, total_games = train(iterations,"fixed")

    print("Games Played: " + str(total_games))
    print("% Games Won: " + str(learner_wins / float(total_games) * 100))
    print("% Games Lost: " + str(trainer_wins / float(total_games) * 100))
    print("% Cats Games: " + str((total_games - learner_wins - trainer_wins) / float(total_games) * 100) + "\n")

    while True:
        game = learningsystem.ExperimentGenerator()
        computer.setGame(game)
        start_turn = random.randint(0,1)
        if start_turn == 1:
            player_turn = 'X'
        else:
            player_turn = 'O'
        print(player_turn + " is playing first.")
        while (game.getWinner() is None) and (game.numEmptySquares() > 0):
            game.printBoard()
            if player_turn == 'X':
                computer.chooseMove()
                player_turn = 'O'
            else:
                x = int(input("Enter x coordinate [0,2]: "))
                y = int(input("Enter y coordinate: [0,2]: "))
                legal_move = game.makeMove(x,y,'O')
                if not legal_move:
                    print("Illegal move.")
                else:
                    player_turn = 'X'
        winner = game.getWinner()
        game.printBoard()
        if winner is None:
            print("Draw!")
        else:
            print(winner + " won!\n")
        if winner == 'X':
            learner_wins += 1
        elif winner == 'O':
            trainer_wins += 1
        total_games += 1
        print("Games Played: " + str(total_games))
        print("% Games Won: " + str(learner_wins / float(total_games) * 100))
        print("% Games Lost: " + str(trainer_wins / float(total_games) * 100))
        print("% Cats Games: " + str((total_games - learner_wins - trainer_wins) / float(total_games) * 100) + "\n")

        critic = learningsystem.Critic(computer)
        generalizer = learningsystem.Generalizer(computer)
        training_examples = critic.getTrainingExamples()
        computer.setHypothesis(generalizer.updateHypothesis(game.getHistory(),training_examples))

if __name__ == "__main__":
    main()
