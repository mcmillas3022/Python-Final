import db
import csv

from objects import Player, Lineup

POSITIONS = ("PG", "SG", "SF", "PF", "C")

def add_player(players):    
    first_name = input("First name: ").title()
    last_name = input("Last name: ").title()
    position = get_player_position()
    points = get_points()
    rebounds = get_rebounds()
    assists = get_assists()

    starting_order = players.count + 1

    player = Player(first_name, last_name, position, points, rebounds, assists, starting_order)
    players.add(player)
    db.add_player(player)
    print(f"{player.fullName} was added.\n")

def get_player_position():
    while True:
        position = input("Position: ").upper()
        if position in POSITIONS:
            return position
        else:
            print("Invalid position. Try again.")

def get_points():
    while True:
        try:
            points = int(input("Points: "))
        except ValueError:
            print("Invalid integer. Try again.")
            continue

        if points < 0 or points > 100000:    
            print("Invalid entry. Must be from 0 to 100,000.")
        else:
            return points      

def get_rebounds():
    while True:
        try:
            rebounds = int(input("Rebounds: "))
        except ValueError:
            print("Invalid integer. Try again.")
            continue

        if rebounds < 0 or rebounds > 10000:        
            print(f"Invalid entry. Must be from 0 to 10,000.")
        else:
            return rebounds
        
def get_assists():
    while True:
        try:
            assists = int(input("Assists: "))
        except ValueError:
            print("Invalid integer. Try again.")
            continue

        if assists < 0 or assists > 10000:        
            print(f"Invalid entry. Must be from 0 to 10,000.")
        else:
            return assists
        
def get_lineup_number(players, prompt):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("Invalid integer. Please try again.")
            continue

        if number < 1 or number > players.count:
            print("Invalid player number. Please try again.")
        else:
            return number

def delete_player(players):
    number = get_lineup_number(players, "Number: ")
    player = players.remove(number)
    db.delete_player(player)
    db.update_starting_order(players)
    print(f"{player.fullName} was deleted.\n")

def edit_player_stats(players):
    number = get_lineup_number(players, "Lineup number: ")
    player = players.get(number)
    print(f"You selected {player.fullName} Points={player.points} Rebounds={player.rebounds} Assists={player.assists}")
    
    player.points = get_points()
    player.rebounds = get_rebounds()
    player.assists = get_assists()
    db.update_player(player)
    print(f"{player.fullName} was updated.\n")

def display_lineup(players):
    if players == None:
        print("There are currently no players in the lineup.")        
    else:
        print(f"{'':3}{'Player':20}{'POS':10}{'Points':>10}{'Rebounds':>10}{'Assists':>10}")
        print("-" * 64)
        for player in players:
            print(f"{player.startingOrder:<3d}{player.fullName:20}{player.position:6}" + \
                  f"{player.points:10d}{player.rebounds:10d}{player.assists:10d}")
    print()   

def display_separator():
    print()
    print("---------------------------------------------------------------------------")
    print()

def display_title():
    print("                 Milwaukee Bucks Basketball Team ")


def display_menu():
    print("MENU OPTIONS")
    print("1 – Display lineup")
    print("2 – Add player")
    print("3 – Delete player")
    print("4 – Edit player stats")
    print("5 - Display Menu")
    print("6 - Exit program")
    print()

def display_positions():
    print("POSITIONS")
    print("C, PG, SG, F, SF, PF")

def main():
    display_separator()
    display_title()
    display_menu()
    display_positions()

    db.connect()
    players = db.get_players()
    if players == None:
        players = Lineup()         

    display_separator()
    
    while True:
        try:
            option = int(input("Menu option: "))
            print()
        except ValueError:
            option = -1
            
        if option == 1:
            display_lineup(players)
        elif option == 2:
            add_player(players)
            players = db.get_players()
        elif option == 3:
            delete_player(players)
        elif option == 4:
            edit_player_stats(players)
        elif option == 5:
            display_menu()
        elif option == 6:
            db.close()
            print("Goodbye!  Go Bucks!")
            break
        else:
            print("Not a valid option. Please try again.\n")
            display_menu()

if __name__ == "__main__":
    main()
