import sys

class Nim:
    def __init__(self, red, blue, version, starting_player):
        self.red = red
        self.blue = blue
        self.version = version
        self.score = 0
        self.starting_player = starting_player
        self.current_player = starting_player
        self.standard_moves = [("red", 2), ("blue", 2), ("red", 1), ("blue", 1)]
        self.misere_moves = [("blue", 1), ("red", 1), ("blue", 2), ("red", 2)]
    
    
    def get_moves(self):
        if self.version == "standard":
            return self.standard_moves
        else:
            return self.misere_moves
        
        
    def is_game_over(self):
        return self.red == 0 or self.blue == 0


    def calculate_score_at_terminal(self, red, blue, is_maximizer_turn):
        # calculate points
        points = (red * 2) + (blue * 3)
        
        # Determine based on version and maximizer turn whether positive or negative points get returned
        if is_maximizer_turn and self.version == "standard":
            return -points
        elif not is_maximizer_turn and self.version == "standard":
            return points
        
        if is_maximizer_turn and self.version == "misere":
            return points
        elif not is_maximizer_turn and self.version == "misere":
            return -points
    
    def calculate_final_score(self):
        return (self.red * 2) + (self.blue * 3)
    
    def minmax(self, red, blue, is_maximizer_turn, alpha, beta):
        if red == 0 or blue == 0:
            return self.calculate_score_at_terminal(red, blue, is_maximizer_turn)
        
        if is_maximizer_turn:
            best_val = -float("inf")
            moves = self.get_moves()
            val = None
            
            for marble, count in moves:
                if marble == "red" and red - count >= 0:
                    val = self.minmax(red - count, blue, False, alpha, beta)
                elif marble == "blue" and blue - count >= 0:
                    val = self.minmax(red, blue - count, False, alpha, beta)
                else:
                    continue
            
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                
                if beta <= alpha:
                    break
                
            return best_val
        else:
            best_val = float("inf")
            moves = self.get_moves()
            val = None
            
            for marble, count in moves:
                if marble == "red" and red - count >= 0:
                    val = self.minmax(red - count, blue, True, alpha, beta)
                elif marble == "blue" and blue - count >= 0:
                    val = self.minmax(red, blue - count, True, alpha, beta)
                else:
                    continue
                
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                
                if beta <= alpha:
                    break
                
            return best_val
    
    
    def play_computer_move(self):
        best_move = None
        best_val = -float("inf")
        moves = self.get_moves()
        
        alpha = -float("inf")
        beta = float("inf")
        
        for marble, count in moves:
            if marble == "red" and self.red - count >= 0:
                val = self.minmax(self.red - count, self.blue, False, alpha, beta)
            elif marble == "blue" and self.blue - count >= 0:
                val = self.minmax(self.red, self.blue - count, False, alpha, beta)
            else:
                continue
            
            if val > best_val:
                best_val = val
                best_move = (marble, count)
                alpha = max(alpha, best_val)
        
        if best_move[0] == "blue":
            self.blue -= best_move[1]
        else:
            self.red -= best_move[1]
        
        # Update current game state to player
        output_line = f"Computer chose to remove {best_move[1]} {best_move[0]} marble(s)"
        print(output_line)
        print("*" * len(output_line))
        
    
    def play_human_move(self):
        # Tell player current game state
        print(f"Current game state = red:{self.red} blue:{self.blue}")
        
        color = input("Enter the color of the marble to remove (red or blue): ").strip().lower()
        # If the color isnt red or blue ask again
        while color not in ["red", "blue"]:
            color = input("This color is not available to pick please choose (red or blue): ").strip().lower()
        
        number_to_remove = int(input(f"Enter the number of {color} marbles to remove (1 or 2): ").strip())
        # If the amount to remove is invalid ask again
        while not self.number_to_remove_is_valid(color, number_to_remove):
            number_to_remove = int(input("This is an invalid choice please pick again: "))
        
        # Record the player's mover
        if color == "red":
            self.red -= number_to_remove
        if color == "blue":
            self.blue -= number_to_remove

        
    def play(self):
        # Handle turn taking
        while not self.is_game_over():
            if self.current_player == "computer":
                self.play_computer_move()
                self.current_player = "human"
            else:
                self.play_human_move()
                self.current_player = "computer"

        # Determine and print the winner
        final_score = self.calculate_final_score()
        
        computer_wins = f"Computer wins with score of {final_score}"
        human_wins = f"Human wins with score of {final_score}"
        
        # If the version is standard and you find an empty pile on your turn, other player wins
        if self.version == "standard":
            if self.current_player == "computer":
                print("*** " + human_wins + " ***")
            else:
                print("*** " + computer_wins + " ***")
        # If the version is misere and you find an empty pile on your turn, you win
        else:
            if self.current_player == "computer":
                print("*** " + computer_wins + " ***")
            else:
                print("*** " + human_wins + " ***")
    
    
    def number_to_remove_is_valid(self, color, number_to_remove):
        # Dont allow removal if its any number other than 1 or 2
        if number_to_remove < 1 or number_to_remove > 2:
            return False
        
        # If the color chosen is red and that many to remove results in a negative number dont allow
        if color == "red" and self.red - number_to_remove < 0:
            return False
        # If the color chosen is blue and that many to remove results in a negative number dont allow
        elif color == "blue" and self.blue - number_to_remove < 0:
            return False
        else:
            return True


def initialize():
    # Set defaults and initialize game state
    version = "standard"
    starting_player = "computer"
    red, blue = int(sys.argv[1]), int(sys.argv[2])
    
    if len(sys.argv) == 4:
        if sys.argv[3] == "standard" or sys.argv[3] == "misere":
            version = sys.argv[3]
        elif sys.argv[3] == "computer" or sys.argv[3] == "human":
            starting_player = sys.argv[3]
    elif len(sys.argv) == 5:
        version = sys.argv[3]
        starting_player = sys.argv[4]
    
    game = Nim(red, blue, version, starting_player)
    game.play()


if __name__ == "__main__":
    initialize()