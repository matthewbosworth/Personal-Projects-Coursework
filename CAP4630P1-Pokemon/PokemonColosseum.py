import random
import sys
from typing import List, Tuple
from Pokemon import Pokemon, Move, TypeMatchup, GameDataLoader

class BattleQueue:
    # First in first out queue for Pokemon battle order
    def __init__(self, pokemon_list: List[Pokemon]):
        self.queue = pokemon_list.copy()
    
    def is_empty(self) -> bool:
        return len(self.queue) == 0
    
    def get_current(self) -> Pokemon:
        # Get the current Pokemon without removing it
        if self.queue:
            return self.queue[0]
        return None
    
    def next_pokemon(self) -> Pokemon:
        # Remove and return the current Pokemon
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def add_pokemon(self, pokemon: Pokemon):
        # Add a Pokemon to the end of the queue
        self.queue.append(pokemon)
    
    def __len__(self):
        return len(self.queue)
    
    def __repr__(self):
        return f"BattleQueue({[p.name for p in self.queue]})"

class PokemonColosseum:
    # Main game class
    
    def __init__(self):
        self.moves_dict = GameDataLoader.load_moves_data()
        self.all_pokemon = GameDataLoader.load_pokemon_data(moves_dict=self.moves_dict)
        self.team_player = []
        self.team_rocket = []
        self.player_queue = None
        self.rocket_queue = None
        self.player_name = ""
        self.current_turn = ""  # "player" or "rocket"
    
    def select_random_teams(self):
        # Select 6 unique Pokemon randomly from the database

        # Error if not enough Pokemon
        if len(self.all_pokemon) < 6:
            print("Error: Not enough Pokemon in database.")
            sys.exit(1)
        
        # Shuffle all Pokemon
        available_pokemon = self.all_pokemon.copy()
        random.shuffle(available_pokemon)
        
        # Select 6 unique Pokemon
        selected_pokemon = available_pokemon[:6]
        
        # Split into two teams of 3 each
        self.team_player = selected_pokemon[:3]
        self.team_rocket = selected_pokemon[3:6]
        
        # Create battle queues with random order
        random.shuffle(self.team_player)
        random.shuffle(self.team_rocket)
        
        self.player_queue = BattleQueue(self.team_player)
        self.rocket_queue = BattleQueue(self.team_rocket)
    
    def calculate_damage(self, move: Move, attacker: Pokemon, defender: Pokemon) -> int:
        # Damage calculation formula

        # Get base values
        power = move.power
        attack = attacker.attack
        defense = defender.defense
        
        # Calculate STAB (Same Type Attack Bonus)
        stab = 1.5 if move.type == attacker.type else 1.0
        
        # Calculate type effectiveness
        type_effectiveness = TypeMatchup.get_effectiveness(move.type, defender.type)
        
        # Random factor between 0.5 and 1
        random_factor = random.uniform(0.5, 1.0)
        
        # Calculate damage
        damage = power * (attack / defense) * stab * type_effectiveness * random_factor
        
        # Round up to nearest integer
        return int(damage) if damage == int(damage) else int(damage) + 1
    
    def perform_attack(self, attacker: Pokemon, defender: Pokemon, move: Move, is_player: bool) -> bool:
        # Perform an attack and return fainted if the defender fainted 
        damage = self.calculate_damage(move, attacker, defender)
        
        # Determine team names for display
        attacker_team = self.player_name if is_player else "Team Rocket"
        defender_team = "Team Rocket" if is_player else self.player_name
        
        print(f"\n{attacker_team}'s {attacker.name} cast '{move.name}' to {defender.name}: ", end="")
        
        # Apply damage
        fainted = defender.take_damage(damage)
        
        if fainted:
            print(f"Damage to {defender.name} is {damage} points. Now {defender.name} faints back to poke ball.")
        else:
            print(f"Damage to {defender.name} is {damage} points. Now {attacker.name} has {attacker.current_hp} HP, and {defender.name} has {defender.current_hp} HP.")
        
        # Mark move as used for the attacker
        move_reset = attacker.use_move(move)
        if move_reset:
            print(f"  Note: {attacker.name} has used all moves! All moves are now available again.")
        
        return fainted
    
    def player_select_move(self, pokemon: Pokemon) -> Move:
        # Let the player select a move for their Pokemon

        print(f"\nChoose the move for {pokemon.name}:")
        
        # Get move display list
        move_display = pokemon.get_available_moves_display()
        
        # Display moves with numbers
        for i, move_name in enumerate(move_display, 1):
            print(f"{i}. {move_name}")
        
        # Get valid input
        while True:
            try:
                choice = input(f"\n{self.player_name}'s choice: ").strip()
                if not choice:
                    continue
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(pokemon.moves):
                    selected_move = pokemon.moves[choice_num - 1]
                    
                    # Check if move is available
                    if selected_move in pokemon.available_moves:
                        return selected_move
                    else:
                        print(f"Move '{selected_move.name}' is not available. Please choose an available move.")
                else:
                    print(f"Please enter a number between 1 and {len(pokemon.moves)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def rocket_select_move(self, pokemon: Pokemon) -> Move:
        # Randomly select a move for Team Rocket's Pokemon

        # Only select from available moves
        if pokemon.available_moves:
            return random.choice(pokemon.available_moves)
        else:
            # This shouldn't happen if reset logic works, but just in case
            pokemon.reset_moves()
            return random.choice(pokemon.available_moves)
    
    def battle_round(self):
        # Round of battle

        if self.current_turn == "player":
            # Player's turn
            attacker = self.player_queue.get_current()
            defender = self.rocket_queue.get_current()
            
            if attacker and defender:
                move = self.player_select_move(attacker)
                fainted = self.perform_attack(attacker, defender, move, is_player=True)
                
                if fainted:
                    # Remove fainted Pokemon
                    self.rocket_queue.next_pokemon()
                    if not self.rocket_queue.is_empty():
                        print(f"\nNext for Team Rocket, {self.rocket_queue.get_current().name} enters battle!")
                
                # Switch turn
                self.current_turn = "rocket"
        
        else:  
            # Rocket's turn
            attacker = self.rocket_queue.get_current()
            defender = self.player_queue.get_current()
            
            if attacker and defender:
                move = self.rocket_select_move(attacker)
                fainted = self.perform_attack(attacker, defender, move, is_player=False)
                
                if fainted:
                    # Remove fainted Pokemon
                    self.player_queue.next_pokemon()
                    if not self.player_queue.is_empty():
                        print(f"\nNext for {self.player_name}, {self.player_queue.get_current().name} enters battle!")
                
                # Switch turn
                self.current_turn = "player"
    
    def display_team(self, team: List[Pokemon], team_name: str):
        # Display team
        names = [p.name for p in team]
        print(f"{team_name} enters with {', '.join(names[:-1])}, and {names[-1]}.")
    
    def run(self):
        # Main game

        #Welcome messahe
        print("\n" + "="*50)
        print("Welcome to Pokemon Colosseum!")
        print("="*50)
        
        # Get player name
        self.player_name = input("\nEnter Player Name: ").strip()
        if not self.player_name:
            self.player_name = "Player"
        
        # Select teams
        self.select_random_teams()
        
        # Display teams
        print()
        self.display_team(self.team_rocket, "Team Rocket")
        self.display_team(self.team_player, f"Team {self.player_name}")
        
        # Coin toss for first move
        print("\nLet the battle begin! ", end="")
        if random.choice([True, False]):
            print("Coin toss goes to ... Drumroll Please!... Team Rocket to start the attack!")
            self.current_turn = "rocket"
        else:
            print(f"Coin toss goes to ... Drumroll Please!... Team {self.player_name} to start the attack!")
            self.current_turn = "player"
        
        # Main battle loop
        while not self.player_queue.is_empty() and not self.rocket_queue.is_empty():
            self.battle_round()
        
        # Determine winner
        print("\n" + "="*50)
        if self.player_queue.is_empty():
            print("All of Team Player's Pokemon fainted, and Team Rocket prevails!")
        else:
            print(f"All of Team Rocket's Pokemon fainted, and Team {self.player_name} prevails!")
        print("="*50)

def main():
    # Run the Pokemon Colosseum game
    game = PokemonColosseum()
    game.run()

if __name__ == "__main__":
    main()