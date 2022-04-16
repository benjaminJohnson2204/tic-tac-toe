import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window_width = 500
window_height = 500

border_thickness = 10
tile_width = (window_width - 4 * border_thickness) // 3
tile_height = (window_height - 4 * border_thickness) // 3
border_color = BLACK
background_color = WHITE
clock = pygame.time.Clock()
frame_rate = 30

x_mark = pygame.image.load('X_Mark.png')
x_mark = pygame.transform.scale(x_mark, (tile_width, tile_height))


class Board:
    def __init__(self):
        self.won = False
        self.full = False
        self.pieces = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.x_winning_move = None
        self.o_winning_move = None

    def add_x(self, row, column):
        self.pieces[row][column] = 1

    def add_o(self, row, column):
        self.pieces[row][column] = 2

    def check_for_win(self):
        winner = 0
        for i in range(3):
            if self.pieces[i][i] != 0 and (self.pieces[i][0] == self.pieces[i][1] == self.pieces[i][2] or
                                           self.pieces[0][i] == self.pieces[1][i] == self.pieces[2][i]):
                winner = self.pieces[i][i]
                break
        if self.pieces[0][0] == self.pieces[1][1] == self.pieces[2][2] or self.pieces[0][2] == self.pieces[1][1] == self.pieces[2][0]:
            winner = self.pieces[1][1]
        if winner == 0:
            return 0
        else:
            self.won = True
            return winner

    def check_if_full(self):
        result = True
        for i in range(3):
            if 0 in self.pieces[i]:
                result = False
        self.full = result

    def x_can_win(self):
        negative_diagonal_check = []
        for i in range(3):
            if 0 in self.pieces[i] and self.pieces[i].count(1) == 2:
                self.x_winning_move = [i, self.pieces[i].index(0)]
                return True
            check = [self.pieces[j][i] for j in range(3)]
            if 0 in check and check.count(1) == 2:
                self.x_winning_move = [check.index(0), i]
                return True
            negative_diagonal_check.append(self.pieces[i][i])
        if 0 in negative_diagonal_check and negative_diagonal_check.count(1) == 2:
            self.x_winning_move = [negative_diagonal_check.index(0), negative_diagonal_check.index(0)]
            return True
        positive_diagonal_check = [self.pieces[0][2], self.pieces[1][1], self.pieces[2][0]]
        if 0 in positive_diagonal_check and positive_diagonal_check.count(1) == 2:
            self.x_winning_move = [positive_diagonal_check.index(0), 2 - positive_diagonal_check.index(0)]
            return True
        self.x_winning_move = None
        return False

    def o_can_win(self):
        negative_diagonal_check = []
        for i in range(3):
            if 0 in self.pieces[i] and self.pieces[i].count(2) == 2:
                self.o_winning_move = [i, self.pieces[i].index(0)]
                return True
            check = [self.pieces[j][i] for j in range(3)]
            if 0 in check and check.count(2) == 2:
                self.o_winning_move = [check.index(0), i]
                return True
            negative_diagonal_check.append(self.pieces[i][i])
        if 0 in negative_diagonal_check and negative_diagonal_check.count(2) == 2:
            self.o_winning_move = [negative_diagonal_check.index(0), negative_diagonal_check.index(0)]
            return True
        positive_diagonal_check = [self.pieces[0][2], self.pieces[1][1], self.pieces[2][0]]
        if 0 in positive_diagonal_check and positive_diagonal_check.count(2) == 2:
            self.o_winning_move = [positive_diagonal_check.index(0), 2 - positive_diagonal_check.index(0)]
            return True
        self.o_winning_move = None
        return False

    def get_x_move(self):
        pieces_placed = 0
        for i in range(3):
            for j in range(3):
                if self.pieces[i][j] != 0:
                    pieces_placed += 1
        if pieces_placed == 0:
            return [0, 0]
        elif self.x_can_win():
            return self.x_winning_move
        elif self.o_can_win():
            return self.o_winning_move
        elif pieces_placed == 2:
            return [2, 2] if self.pieces[2][2] == 0 else [1, 1]
        else:
            if self.pieces[1][1] == 0:
                return [1, 1]
            else:
                for row in self.pieces:
                    if 0 in row:
                        return [self.pieces.index(row), row.index(0)]

    def get_o_move(self):
        pieces_placed = 0
        for i in range(3):
            for j in range(3):
                if self.pieces[i][j] != 0:
                    pieces_placed += 1
        if pieces_placed == 1:
            return [0, 0] if self.pieces[0][0] == 0 else [2, 0]
        elif self.o_can_win():
            return self.o_winning_move
        elif self.x_can_win():
            return self.x_winning_move
        elif pieces_placed == 3:
            return [2, 2] if self.pieces[2][2] == 0 else [1, 1]
        else:
            return [1, 1]

    def draw(self, window):
        pygame.draw.rect(window, border_color, (border_thickness + tile_width, border_thickness, border_thickness,
                                                tile_height * 3 + border_thickness * 2))
        pygame.draw.rect(window, border_color, ((border_thickness + tile_width) * 2, border_thickness, border_thickness,
                                                tile_height * 3 + border_thickness * 2))
        pygame.draw.rect(window, border_color, (border_thickness, border_thickness + tile_height, tile_width * 3 +
                                                border_thickness * 2, border_thickness))
        pygame.draw.rect(window, border_color, (border_thickness, (border_thickness + tile_height) * 2, tile_width * 3 +
                                                border_thickness * 2, border_thickness))
        for i in range(3):
            for j in range(3):
                if self.pieces[i][j] == 1:
                    window.blit(x_mark, (border_thickness + (border_thickness + tile_width) * j, border_thickness +
                                         (border_thickness + tile_height) * i))
                elif self.pieces[i][j] == 2:
                    pygame.draw.circle(window, BLACK, (border_thickness + tile_width // 2 + (border_thickness +
                        tile_width) * j, border_thickness + tile_height // 2 + (border_thickness + tile_height) * i),
                                       tile_width // 2 - border_thickness // 4, border_thickness // 2)


def mouse_dimension_to_index(dimension):
    for i in range(3):
        if i * (tile_width + border_thickness) < dimension < i * (tile_width + border_thickness) + border_thickness:
            return "border"
        elif i * (tile_width + border_thickness) + border_thickness < dimension < (i + 1) * (tile_width + border_thickness):
            return i


def two_player_game():
    play_again = True
    ties_victories = [0, 0, 0]
    while play_again:
        pygame.init()
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Tic-Tac-Toe")
        playing = True
        winner = 0
        player_turn = 1
        turns_taken = 0
        game = Board()
        while playing:
            clock.tick(frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    pygame.quit()
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                if not (mouse_dimension_to_index(mouse_x) == "border" or mouse_dimension_to_index(mouse_y) == "border"):
                    if game.pieces[mouse_dimension_to_index(mouse_y)][mouse_dimension_to_index(mouse_x)] == 0:
                        game.pieces[mouse_dimension_to_index(mouse_y)][mouse_dimension_to_index(mouse_x)] = player_turn
                        turns_taken += 1
                        winner = game.check_for_win()
                        if game.won or turns_taken >= 9:
                            playing = False
                        player_turn += 1
                        if player_turn > 2:
                            player_turn -= 2
            window.fill(background_color)
            game.draw(window)
            pygame.display.update()
        pygame.quit()
        ties_victories[winner] += 1
        print("\n")
        if game.won:
            print("The winner was player " + str(winner))
        elif turns_taken >= 9:
            print("Game was a tie.")
        else:
            print("Game has been ended by player.")
        print("Player 1 victories: " + str(ties_victories[1]))
        print("Player 2 victories: " + str(ties_victories[2]))
        print("Ties: " + str(ties_victories[0]))
        play_again = input("Play again? Y/N: ").upper() == "Y"


def one_player_game():
    icons = [0, "X", "O"]
    play_again = True
    ties_victories = [0, 0, 0]
    while play_again:
        player_icon = input("Choose X or O: ").upper()
        if player_icon == "X":
            cpu_icon = "O"
            player_turn = True
        else:
            cpu_icon = "X"
            player_turn = False
        pygame.init()
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Tic-Tac-Toe")
        playing = True
        winner = 0
        turns_taken = 0
        game = Board()
        while playing:
            clock.tick(frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    pygame.quit()
            if player_turn:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    if not (mouse_dimension_to_index(mouse_x) == "border" or mouse_dimension_to_index(
                            mouse_y) == "border"):
                        if game.pieces[mouse_dimension_to_index(mouse_y)][mouse_dimension_to_index(mouse_x)] == 0:
                            game.pieces[mouse_dimension_to_index(mouse_y)][
                                mouse_dimension_to_index(mouse_x)] = icons.index(player_icon)
                            turns_taken += 1
                            winner = game.check_for_win()
                            if game.won or turns_taken >= 9:
                                playing = False
                            player_turn = False
            else:
                if cpu_icon == "X":
                    cpu_move = game.get_x_move()
                    game.pieces[cpu_move[0]][cpu_move[1]] = 1
                else:
                    cpu_move = game.get_o_move()
                    game.pieces[cpu_move[0]][cpu_move[1]] = 2
                turns_taken += 1
                winner = game.check_for_win()
                if game.won or turns_taken >= 9:
                    playing = False
                player_turn = True
            window.fill(background_color)
            game.draw(window)
            pygame.display.update()
        pygame.quit()
        ties_victories[winner] += 1
        print("\n")
        game.check_if_full()
        if game.won and winner == icons.index(player_icon):
            print("Congratulations! You won!")
        elif game.won:
            print("The computer has won!")
        elif game.full:
            print("Game was a tie.")
        else:
            print("Game has been ended by player.")
        print("Player victories: " + str(ties_victories[icons.index(player_icon)]))
        print("Computer victories: " + str(ties_victories[icons.index(cpu_icon)]))
        print("Ties: " + str(ties_victories[0]))
        play_again = input("Play again? Y/N: ").upper() == "Y"


if __name__ == "__main__":
    player_count = input("Enter the number of players: ")
    if player_count == "2":
        two_player_game()
    else:
        one_player_game()



