from cmath import inf

board =  {}


# board example {(0, 0): ' ', (0, 1): ' ', (0, 2): ' ', (0, 3): ' ', 
#                (1, 0): ' ', (1, 1): ' ', (1, 2): ' ', (1, 3): ' ',
#                (2, 0): ' ', (2, 1): ' ', (2, 2): ' ', (2, 3): ' ',
#                (3, 0): ' ', (3, 1): ' ', (3, 2): ' ', (3, 3): ' ',  }

class GameParameters:
    def __init__(self, num_rows=0, num_cols=0, connect_to_win=0, piece1='X', piece2='O', valid_columns=set()):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.connect_to_win = connect_to_win
        self.piece1 = piece1
        self.piece2 = piece2
        self.valid_columns = valid_columns
    
    def make_board(self):
        
        self.num_rows = get_dimension_input('Choose number of rows between 1-10: ')
        self.num_cols = get_dimension_input('Choose number of columns between 1-10: ')
        self.connect_to_win = get_dimension_input('Choose number of stones to connect for a win between 1-10: ')
        self.num_rows = int(self.num_rows)
        self.num_cols = int(self.num_cols)
        self.connect_to_win = int(self.connect_to_win)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                board[i, j] = ' '

    def valid_columns_maker(self):
        for i in range(self.num_cols):
            self.valid_columns.add(str(i))

game = GameParameters()

def get_dimension_input(text):
  num = input(text)
  if num in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
    return int(num)
  print('Oops. Invalid input. Try again.')
  return get_dimension_input(text)
        
def print_board(board):
    num_cols = game.num_cols
    num_rows = game.num_rows
    rows = []
    row_break = ' ---' * num_cols
    for i in range(num_rows):
        row = '| '
        for j in range(num_cols):
            row += str(board[(i, j)]) + ' | '
        rows.append(row)
        rows.append(row_break)
    column_string = '| '
    counter = 0
    for i in range(num_cols):
        column_string += str(counter) + ' | '
        counter += 1
    print(column_string)
    print(row_break)
    for row in rows:
        print(row)

def user1_play():
    valid_columns = game.valid_columns
    num_rows = game.num_rows
    piece1 = game.piece1
    col = input('Choose your column: ')
    if col not in valid_columns:
        print('Oops thats not a valid column. Try again.')
        return user1_play()
    col = int(col)
    if board[0, col] != ' ':
        print('Oops. That column is full. Try again.')
        return user1_play()
    for i in range(num_rows-1, -1, -1):
        if board[i, col] == ' ':
            board[i, col] = piece1
            break

def user2_play():
    valid_columns = game.valid_columns
    piece2 = game.piece2
    num_rows = game.num_rows
    col = input('Choose your column: ')
    if col not in valid_columns:
        print('Oops thats not a valid column. Try again.')
        return user2_play()
    col = int(col)
    if board[0, col] != ' ':
        print('Oops. That column is full. Try again.')
        return user2_play()
    for i in range(num_rows-1, -1, -1):
        if board[i, col] == ' ':
            board[i, col] = piece2
            break

def ai_play():
    num_rows = game.num_rows
    num_cols = game.num_cols
    piece2 = game.piece2
    best_score = -inf
    best_play = None
    for j in range(num_cols):
        for i in range(num_rows-1, -1, -1):
            if board[i, j] == ' ':
                board[i, j] = piece2
                score = minimax(board, 6 , False, -inf, inf)
                board[i, j] = ' ' 
                if score > best_score:
                    best_score = score
                    best_play = (i, j)
                break
                
    
    board[best_play] = piece2
    return

def minimax(board, depth, isMaximizing, alpha, beta):
    num_rows = game.num_rows
    num_cols = game.num_cols
    piece1 = game.piece1
    piece2 = game.piece2
    if check_player_2_win() == True:
        return 1000
    if check_player_1_win() == True:
        return -1000
    if check_draw() == True:
        return 0
    if depth == 0:
        return eval_board(board)

    if isMaximizing:
        best_score = -inf
        flag = False
        for j in range(num_cols):
            if flag == True:
                break
            for i in range(num_rows-1, -1, -1):
                if board[i, j] == ' ':
                    board[i, j] = piece2
                    score = minimax(board, depth-1, False, alpha, beta)
                    board[i, j] = ' ' 
                    if score > best_score:
                        best_score = score
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        flag = True
                    break
        return best_score
                    

    else:
        best_score = inf
        flag = False
        for j in range(num_cols):
            if flag == True:
                break
            for i in range(num_rows-1, -1, -1):
                if board[i, j] == ' ':
                    board[i, j] = piece1
                    score = minimax(board, depth-1, True, alpha, beta)
                    board[i, j] = ' ' 
                    if score < best_score:
                        best_score = score
                    beta = min(beta, score)
                    if beta <= alpha:
                        flag = True
                    break
        return best_score

def eval_board(board):
    num_rows = game.num_rows
    num_cols = game.num_cols
    connect_to_win = game.connect_to_win
    piece1 = game.piece1
    piece2 = game.piece2
    board_score = 0
    # check verticals
    for j in range(num_cols):
        for i in range(num_rows - connect_to_win + 1):
            counter = 0
            while i + counter < num_rows and board[i + counter, j] == piece1:
                counter += 1
            if counter == connect_to_win - 1:
                board_score -= 1
    #check horizontals
    for i in range(num_rows):
        for j in range(num_cols - connect_to_win + 1):
            counter = 0
            while j + counter < num_cols and board[i, j+counter] == piece1:
                counter += 1
            if counter == connect_to_win - 1:
                board_score -= 1
    #check diagonals
    for i in range(num_rows - connect_to_win + 1):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i + counter < num_rows and j + counter < num_cols and board[i + counter, j + counter] == piece1:
                counter += 1
            if counter == connect_to_win - 1:
                board_score -= 1

    for i in range(num_rows - 1, (num_rows-1) - 1 - (num_rows - connect_to_win)):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i - counter > -1 and j + counter < num_cols and board[i - counter, j + counter] == piece1:
                counter += 1
            if counter == connect_to_win - 1:
                board_score -= 1
    

    # check verticals
    for j in range(num_cols):
        for i in range(num_rows - connect_to_win + 1):
            counter = 0
            while i + counter < num_rows and board[i + counter, j] == piece2:
                counter += 1
            if counter == connect_to_win - 1:
                board_score += 1
    #check horizontals
    for i in range(num_rows):
        for j in range(num_cols - connect_to_win + 1):
            counter = 0
            while j + counter < num_cols and board[i, j+counter] == piece2:
                counter += 1
            if counter == connect_to_win - 1:
                board_score += 1
    #check diagonals
    for i in range(num_rows - connect_to_win + 1):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i + counter < num_rows and j + counter < num_cols and board[i + counter, j + counter] == piece2:
                counter += 1
            if counter == connect_to_win - 1:
                board_score += 1

    for i in range(num_rows - 1, (num_rows-1) - 1 - (num_rows - connect_to_win)):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i - counter > -1 and j + counter < num_cols and board[i - counter, j + counter] == piece2:
                counter += 1
            if counter == connect_to_win-1:
                board_score += 1
    return board_score

def check_player_1_win():
    num_rows = game.num_rows
    num_cols = game.num_cols
    connect_to_win = game.connect_to_win
    piece1 = game.piece1
    # check verticals
    for j in range(num_cols):
        for i in range(num_rows - connect_to_win + 1):
            counter = 0
            while i + counter < num_rows and board[i + counter, j] == piece1:
                counter += 1
            if counter >= connect_to_win:
                return True
    #check horizontals
    for i in range(num_rows):
        for j in range(num_cols - connect_to_win + 1):
            counter = 0
            while j + counter < num_cols and board[i, j+counter] == piece1:
                counter += 1
            if counter >= connect_to_win:
                return True
    #check diagonals
    for i in range(num_rows - connect_to_win + 1):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i + counter < num_rows and j + counter < num_cols and board[i + counter, j + counter] == piece1:
                counter += 1
            if counter >= connect_to_win:
                return True

    for i in range(num_rows - 1, (num_rows-1) - 1 - (num_rows - connect_to_win), -1):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i - counter > -1 and j + counter < num_cols and board[i - counter, j + counter] == piece1:
                counter += 1
            if counter >= connect_to_win:
                return True
    
    return False

def check_player_2_win():
    num_rows = game.num_rows
    num_cols = game.num_cols
    connect_to_win = game.connect_to_win
    piece2 = game.piece2
    # check verticals
    for j in range(num_cols):
        for i in range(num_rows - connect_to_win + 1):
            counter = 0
            while i + counter < num_rows and board[i + counter, j] == piece2:
                counter += 1
            if counter >= connect_to_win:
                return True
    #check horizontals
    for i in range(num_rows):
        for j in range(num_cols - connect_to_win + 1):
            counter = 0
            while j + counter < num_cols and board[i, j+counter] == piece2:
                counter += 1
            if counter >= connect_to_win:
                return True
    #check diagonals
    for i in range(num_rows - connect_to_win + 1):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i + counter < num_rows and j + counter < num_cols and board[i + counter, j + counter] == piece2:
                counter += 1
            if counter >= connect_to_win:
                return True

    for i in range(num_rows - 1, (num_rows-1) - 1 - (num_rows - connect_to_win), -1):
        for j in range(num_cols - connect_to_win +1):
            counter = 0
            while i - counter > -1 and j + counter < num_cols and board[i - counter, j + counter] == piece2:
                counter += 1
            if counter >= connect_to_win:
                return True
    
    return False

def check_draw():
    for space in board:
        if board[space] == ' ':
            return False
    return True

def gameplay():
    game.make_board()
    game.valid_columns_maker()
    while check_draw() == False:
        
        print_board(board)
        user1_play()
        if check_player_1_win() == True:
            print_board(board)
            print('Player 1 wins!')
            exit()
        if check_draw() == True:
            print_board(board)
            print('Its a draw!')
            exit()
            
        print_board(board)
        user2_play()
        if check_player_2_win() == True:
            print_board(board)
            print('Player 2 wins!')
            exit()
        if check_draw() == True:
            print_board(board)
            print('Its a draw!')
            exit()
            

    print('Its a draw!')
    
def computer_gameplay():
    game.make_board()
    game.valid_columns_maker()
    while check_draw() == False:
        
        print_board(board)
        user1_play()
        if check_player_1_win() == True:
            print_board(board)
            print('Player 1 wins!')
            exit()
        if check_draw() == True:
            print_board(board)
            print('Its a draw!')
            exit()
            
        print_board(board)
        ai_play()
        if check_player_2_win() == True:
            print_board(board)
            print('Computer wins!')
            exit()
        if check_draw() == True:
            print_board(board)
            print('Its a draw!')
            exit()

def start_game():
    ver = input('Choose one or two player by entering 1 or 2: ')
    if ver not in ['1', '2']:
        print('Oops. Invalid input. Try again.')
        return start_game()
    if ver == '1':
        computer_gameplay()
    else:
        gameplay()

start_game()






    


