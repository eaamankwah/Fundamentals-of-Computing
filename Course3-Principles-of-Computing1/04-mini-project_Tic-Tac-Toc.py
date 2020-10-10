"""
    Monte Carlo Tic-Tac-Toe
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change thier names.
#NTRIALS = 1    # Number of trials to run
#increase NTRIALS to improve accuracy in choosing good moves
NTRIALS = 5    # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    """
        This function takes a current board and the next player to
        move. The function should play a game starting with the
        given player by making random moves, alternating between
        players. The function should return when the game is over.
        The modified board will contain the state of the game, so
        the function does not return anything. In other words, the
        function should modify the board input.
        """
    while (board.check_win() == None):
        square = random.choice(board.get_empty_squares())
        board.move(square[0], square[1], player)
        if (board.check_win() == None):
            player = provided.switch_player(player)
    return None


def mc_update_scores(scores, board, player):
    """
        This function takes a grid of scores (a list of lists) with
        the same dimensions as the Tic-Tac-Toe board, a board from
        a completed game, and which player the machine player is.
        The function should score the completed board and update
        the scores grid. As the function updates the scores grid
        directly, it does not return anything.
        """
    winner = board.check_win()
    if winner == player:
        player_score = SCORE_CURRENT
        other_player_score = -SCORE_OTHER
    elif winner == provided.switch_player(player):
        player_score = -SCORE_CURRENT
        other_player_score = SCORE_OTHER
    else:
        player_score = 0
        other_player_score = 0
    
    dimension = board.get_dim()
    for row in range(dimension):
        for col in range(dimension):
            status = board.square(row, col)
            if status == player:
                scores[row][col] += player_score
            elif status == provided.switch_player(player):
                scores[row][col] += other_player_score
            else:
                scores[row][col] += 0
    return None


def get_best_move(board, scores):
    """
        This function takes a current board and a grid of scores.
        The function should find all of the empty squares with the
        maximum score and randomly return one of them as a (row,
        column) tuple. It is an error to call this function with a
        board that has no empty squares (there is no possible next
        move), so your function may do whatever it wants in that
        case. The case where the board is full will not be tested.
        """
    empty_squares = board.get_empty_squares()
    score_list = []
    scores_squares = {}
    maximum_score_empty_squares = []
    
    if empty_squares == []:
        return "No possible move left"
    
    for row,col in empty_squares:
        score = scores[row][col]
        score_list.append(score)
        scores_squares[(row,col)] = score

    maximum = max(score_list)
    for square,value in scores_squares.items():
        if value == maximum:
            maximum_score_empty_squares.append(square)

return random.choice(maximum_score_empty_squares)


def mc_move(board, player, trials):
    """
        This function takes a current board, which player the machine
        player is, and the number of trials to run. The function should
        use the Monte Carlo simulation described above to return a move
        for the machine player in the form of a (row, column) tuple. Be
        sure to use the other functions you have written!
        """
    dimension = board.get_dim()
    scores = [[0 for dummy in range(dimension)] for dummy in range(dimension)]
    
    for dummy in range(trials):
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(scores, board_copy, player)
    
    return get_best_move(board, scores)

# Test game with the console or the GUI Uncomment whichever
# you prefer. Both should be commented out when you submit
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

# # Testing code
# test_game = provided.TTTBoard(3)
# test_dim = test_game.get_dim()
# test_scores = [[0 for emptycol in range(test_dim)]
# for emptyrow in range(test_dim)]

# # test mc_trial()
# mc_trial(test_game, provided.PLAYERX)
# print str(test_game)
# print "Winner:", test_game.check_win(), "\n"

# # test mc_update_scores
# mc_update_scores(test_scores, test_game, provided.PLAYERX)
# print "Scores:"
# for row in test_scores:
# print row

# # test mc_get_best_move
# test_scores = [[-2.0, -1.0, -1.0],
# [-1.0, 2.0, -2.0],
# [2.0, 3.0, -2.0]]
# move = get_best_move(test_game, test_scores)
# print str(test_game)

# # test mc_move()
# mc_move(test_game, provided.PLAYERX, NTRIALS)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
