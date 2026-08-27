import random
import csv
from typing import List, Dict

class Move:
    # Moves a Pokemon can use
    def __init__(self, name: str, move_type: str, power: int):
        self.name = name
        self.type = move_type
        self.power = power
        self.used = False
    
    def __repr__(self):
        return f"{self.name} ({self.type}, Power: {self.power})"

class Pokemon:
    # Pokemon statistics
    def __init__(self, name: str, pokemon_type: str, hp: int, attack: int, defense: int, moves: List[Move]):
        self.name = name
        self.type = pokemon_type
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves  # List of Move objects
        self.available_moves = moves.copy()  # Moves not yet used in current cycle
        self.is_fainted = False
    
    def take_damage(self, damage: int):
        # Damage Pokemon if <= 0, Pokemon fainted
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_fainted = True
            return True  # Pokemon fainted
        return False  # Pokemon still alive
    
    def use_move(self, move: Move) -> bool:
        # Keeps track of used moves
        if move in self.available_moves:
            self.available_moves.remove(move)
            move.used = True
        
        # If no moves left, reset all moves
        if len(self.available_moves) == 0:
            self.reset_moves()
            return True  # All moves were used, reset occurred
        return False
    
    def reset_moves(self):
        # If a Pokemon has used all its moves, reset them
        self.available_moves = self.moves.copy()
        for move in self.moves:
            move.used = False
    
    def get_available_moves_display(self) -> List[str]:
        # List of avaliable moves
        display = []
        for move in self.moves:
            if move in self.available_moves:
                display.append(move.name)
            else:
                display.append(f"{move.name} (N/A)")
        return display
    
    def __repr__(self):
        return f"{self.name} ({self.type}, HP: {self.current_hp}/{self.max_hp})"

class TypeMatchup:
    # Pokemon type matchup table based on the project specifications
    _matchup_table = {
        "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1},
        "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 1, "Grass": 2},
        "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Electric": 1, "Grass": 0.5},
        "Electric": {"Normal": 1, "Fire": 1, "Water": 2, "Electric": 0.5, "Grass": 0.5},
        "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 1, "Grass": 0.5},
    }
    
    @classmethod
    def get_effectiveness(cls, attack_type: str, defend_type: str) -> float:
        # Effectiveness multiplier 
        if attack_type in cls._matchup_table and defend_type in cls._matchup_table[attack_type]:
            return cls._matchup_table[attack_type][defend_type]
        return 1.0  # For "Others" case which includes any undefined types

class GameDataLoader:
    # Load Pokemon and Moves data from provided CSV files
    
    @staticmethod
    def load_moves_data(csv_file: str = "moves-data.csv") -> Dict[str, Move]:
        # Load moves data
        moves_dict = {}
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['Name']
                    move_type = row['Type']
                    # Some power values might be empty, default to 0
                    power = int(row['Power']) if row['Power'] and row['Power'].isdigit() else 0
                    moves_dict[name] = Move(name, move_type, power)
        except FileNotFoundError:
            print(f"Warning: {csv_file} not found. Using empty moves dictionary.")
        return moves_dict
    
    @staticmethod
    def load_pokemon_data(csv_file: str = "pokemon-data.csv", moves_dict: Dict[str, Move] = None) -> List[Pokemon]:
        # Load pokemon data
        if moves_dict is None:
            moves_dict = {}
        
        pokemon_list = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['Name']
                    pokemon_type = row['Type']
                    hp = int(row['HP'])
                    attack = int(row['Attack'])
                    defense = int(row['Defense'])
                    
                    # Parse moves list from the string format
                    moves_str = row['Moves']
                    # Clean up the string and extract move names
                    moves_str = moves_str.strip("[]'\"")
                    move_names = [m.strip().strip("'\"") for m in moves_str.split(',')]
                    
                    # Create Move objects for this Pokemon
                    pokemon_moves = []
                    for move_name in move_names:
                        if move_name in moves_dict:
                            # Create a new instance of the move for this Pokemon
                            move_data = moves_dict[move_name]
                            pokemon_moves.append(Move(move_name, move_data.type, move_data.power))
                        else:
                            # Create a placeholder move if not found
                            pokemon_moves.append(Move(move_name, "Normal", 0))
                    
                    pokemon = Pokemon(name, pokemon_type, hp, attack, defense, pokemon_moves)
                    pokemon_list.append(pokemon)
        except FileNotFoundError:
            print(f"Warning: {csv_file} not found. Using empty Pokemon list.")
        
        return pokemon_list

