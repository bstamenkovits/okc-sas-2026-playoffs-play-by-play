"""
This module defines a Player dataclass and provides a list of players from the San Antonio Spurs (SAS) and
Oklahoma City Thunder (OKC) teams. These names have been hardcoded based on the names of the players provided
by the official NBA website.
"""

from dataclasses import dataclass

@dataclass
class Player:
    first_name: str
    last_name: str

    @property
    def identifier(self):
        """
        Returns the player's identifier in the format 'A. Lastname'.

        This is the format used by www.nbaplaydb.com, which is used to identify players in
        the description of each play. As an example, Lebron James is identified as 'L. James'.
        """
        return f"{self.first_name[0]}. {self.last_name}"


SAS_players = [
    Player("Jordan", "McLaughlin"),
    Player("Victor", "Wembanyama"),
    Player("Dylan", "Harper"),
    Player("Keldon", "Johnson"),
    Player("De'Aaron", "Fox"),
    Player("Stephon", "Castle"),
    Player("Luke", "Kornet"),
    Player("Kelly", "Olynyk"),
    Player("Carter", "Bryant"),
    Player("Emanuel", "Miller"),
    Player("Bismack", "Biyombo"),
    Player("Devin", "Vassell"),
    Player("David", "Jones Garcia"),
    Player("Julian", "Champagnie"),
    Player("Harrison", "Barnes"),
    Player("Lindy", "Waters III"),
    Player("Mason", "Plumlee"),
    Player("Harrison", "Ingram"),
]

OKC_players = [
    Player("Shai", "Gilgeous-Alexander"),
    Player("Jared", "McCain"),
    Player("Luguentz", "Dort"),
    Player("Jaylin", "Williams"),
    Player("Chet", "Holmgren"),
    Player("Jalen", "Williams"),
    Player("Alex", "Caruso"),
    Player("Isaiah", "Joe"),
    Player("Thomas", "Sorber"),
    Player("Payton", "Sandfort"),
    Player("Branden", "Carlson"),
    Player("Aaron", "Wiggins"),
    Player("Cason", "Wallace"),
    Player("Brooks", "Barnhizer"),
    Player("Ajay", "Mitchell"),
    Player("Kenrich", "Williams"),
    Player("Nikola", "Topić"),
    Player("Isaiah", "Hartenstein"),
]

players = SAS_players + OKC_players
