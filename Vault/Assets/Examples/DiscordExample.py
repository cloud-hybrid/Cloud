import os
import sys

class BattleGame(object):
  def __init__(self, status: bool):
    self.status = status

  @staticmethod
  def exitBattle():
    sys.quit()

class BattleShip(object):
  def __init__(self, name: str, health: int, turn: bool):
    self.name = name
    self.shipHP = health
    self.turn = turn

  @staticmethod
  def attack(opponent):
    damage = int(input("Attack Opponent with Damage: "))
    opponent.shipHP -= damage

class BattleEnd(object):
  def __init__(self):
    pass

  @staticmethod
  def printWon(player: str):
    print(f"Player {player} has won.")

def main():
  Game = BattleGame(True)

  player_1 = BattleShip("Player 1", 100, True)
  player_2 = BattleShip("Player 2", 100, False)

  while Game.status == True:
    print("Player 1's Current Health: " + str(player_1.shipHP))
    player_1.attack(player_2)
    if player_2.shipHP <= 0:
      BattleEnd().printWon(player_1.name)
      Game.status = False
      break
    print("Player 2's Current Health: " + str(player_2.shipHP))
    player_2.attack(player_1)
    if player_1.shipHP <= 0:
      BattleEnd().printWon(player_2.name) 
      Game.status = False
      break
  
  option = str(input("Exit Game? (Y/N): "))

  if option == "Y":
    BattleGame.exitBattle()
  elif option == "N":
    print("N/A")

if __name__ == "__main__":
  main()
