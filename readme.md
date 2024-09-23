# BattleShips 

### A game made in pygame, playable on LAN for two players

---

## How to start the game:
- Run Server.py (python Server.py).
- Run Client.py twice (for each player).
- If you want to play on one PC you may leave IP filed as blank, it will take your PC IP, otherwise type IP of the computer running Server.py

---

## Game Rules
- The objective of the game is to sink all of the opponent's ships; the winner is the player who accomplishes this first.
- Ships cannot be placed adjacent to each other (there must be at least a 1-block gap between them, including diagonal spaces).
- Ship placement is determined randomly.
- Ships can be placed either vertically or horizontally.
- Each player has:
    - 4 ships of length 1.
    - 3 ships of length 2.
    - 2 ships of length 3.
    - 1 ship of length 4.
- Players take turns in the following order:
  - The starting player is chosen at random by the server.
  - The player then selects coordinates on the opponent's map to fire at.
  - After shooting, if the player hits a ship, they take another turn.
  - If the shot hits water, the next player takes their turn.
  - The game ends when one player sinks all of the opponent's ships.

---

## How to Play?
- After launching the game, you will be prompted to enter your name and the server's IP address.
- If the client is running on the same machine as the server, you can leave the IP address field blank; it will be fetched from the system.
- The game window displays two grids: one for the player and one for the opponent.
- On the player's grid, all of their ships are visible.
- On the opponent's grid, all blocks are initially unknown, but as the game progresses, the blocks will indicate the contents of the opponent's grid after each shot:
    - An orange circle means the shot hit water.
    - A red block means a ship was hit.
    - A black block means a ship has been sunk.
- To make a move, select a block from the opponent's grid on the right side.
- You can select a block by clicking the left mouse button. The selected block will be highlighted in orange. To confirm the shot, click the "Shoot" button at the bottom of the window.
- An orange circle on your grid indicates that the opponent shot and missed.
- A red block on your grid indicates that the opponent hit one of your ships.
- After the game ends, the server will automatically shut down. You can close the game window by pressing the *q* key.
- If any connection issues occur, the game will automatically close.

---

## Directory Structure
- `Settings.py` contains settings for the game window and map as well as predefined colors.
- `Server.py` contains the implementation of the Server and Client.
- `Client.py` contains the game implementation and client-server connection logic (Player).
- The `Classes` folder contains the implementations of classes needed for game handling.
- The `Assets` folder contains the ship images.

---

## Implementation

### Classes

The implementation includes the following classes: `Block`, `Button`, `Player`, `Popup`, `Ship`, `SpriteGroup`, `Server`, `Client`, `Game`.
- `Block` is a class that represents a single square on the grid, with methods for marking hits and misses.
- `Button` is a class used to create the "Shoot" button, which allows the player to make a move.
- `Player` is a class representing the player. It stores all ships and includes a method to randomly place them on the grid.
- `Popup` is a class responsible for getting the player’s name and the server IP address.
- `Ship` is a class representing a ship.
- `SpriteGroup` inherits from *pygame.sprite.Group* and overrides the `Draw` method to take the screen into account when drawing.
- `Server` is the game server implementation responsible for relaying information between players.
- `Client` is the class that handles communication with the server.
- `Game` is the class that manages the game logic.

### Key Details
- The `Ship` class keeps track of hits on a ship, allowing the game to determine when it has been sunk.
- The `Player` class keeps track of how many of the opponent's ships have been sunk, which helps determine the game outcome.
- The `Server` acts solely as an intermediary for relaying information between players and distributing turns.
- All game logic is handled on the client-side.
- Grid indexing for both players follows the format [row][column].
- The game ends when the client (player) detects that the number of sunk ships equals the total number of ships. The client sends a *GAME_OVER* message to the server, which forwards it to the other player. The player who receives the *GAME_OVER* message loses.
- The server console displays messages received from players as well as *TURN* messages sent to them.
- The client console shows messages received from the server.

### Client-Server Communication
- Communication is handled via a set of predefined messages:
    - *SHOOT*
    - *SHIP*
    - *WATER*
    - *SHIP_SUNK*
    - *GAME_OVER*
    - *TURN*
    - *READY*
    - *ERROR*
- **SHOOT** indicates a shot; its format is: *SHOOT [row]:[column]*
- **SHIP** indicates a hit on a ship: *SHIP [row]:[column]*
- **WATER** indicates a miss: *WATER [row]:[column]*
- **SHIP_SUNK** means that the hit ship has been sunk:*SHIP_SUNK [row of ship start],[column of ship start]:[ship direction]:[ship length]*
- **GAME_OVER** indicates the end of the game. The player receiving this message from the server loses. Format: *GAME_OVER*
- **TURN** tells the player it's their turn to play. Format: *TURN*
- **READY** signals that the player has received and processed the opponent's name and is ready to start the game.
- **ERROR** indicates that the server encountered an error and is closing the connection, which will also close the clients' games.

#### Notes
- The row in the messages is the actual map index, which is always reduced by 1 (since the grid is indexed from 0, but labels displayed to the user start from 1).
