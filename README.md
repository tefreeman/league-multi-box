# League of Legends Automation Project

Welcome to the League of Legends Automation Project! This project is designed to help you control your champion and Yuumi simultaneously in the game League of Legends. It offers automated functionalities such as routing specific keyboard presses to Yuumi and automatically casting spells like heal when certain conditions are met.

## Project Overview

### Main Purpose and Functionality
The primary goal of this project is to enhance the gameplay experience by allowing a player to control both their main champion and the support champion, Yuumi, at the same time. The project includes functionalities to:
- Route specific keyboard presses to Yuumi.
- Automatically cast spells based on the game state, such as healing when the health is low.
- Track various in-game elements through screen reading and image processing.

### Key Components and Their Interactions
The project is organized into several key components, each responsible for different aspects of the automation:

1. **Actions Module (`actions.py`)**
    - Provides methods for performing in-game actions like moving the mouse, pressing keys, casting spells, and switching champions.

2. **Game Loop (`game_loop.py`)**
    - Manages the main game loop, including updating game states and executing commands based on the current state.

3. **Game State (`game_state.py`)**
    - Represents the current state of the game, including player positions, health, and other critical information.
    - Provides methods to update the game state based on screen captures.

4. **Graphics Positions (`graphics_pos.py`)**
    - Stores graphical coordinates and values for various in-game elements, such as health bars and minimap positions.

5. **Loop Functions (`loop_funcs.py`)**
    - Contains functions that perform specific actions based on the game state, such as auto-healing, leveling up, and fleeing.

6. **Screen Reader (`screen_reader.py`)**
    - Captures the screen and updates the game state with the captured image. Runs continuously in a separate thread.

7. **Socket Communication (`mysocket.py` and `server.py`)**
    - Manages socket communication for routing keyboard presses to another computer and processing incoming data.

8. **Player and Spell Management (`player.py` and `spell.py`)**
    - Defines classes to represent players and their attributes as well as spells and their characteristics.

9. **Utility Functions (`utility.py`)**
    - Provides various utility functions for image processing, color matching, and distance calculations.

10. **Yummi Class (`yummi.py`)**
    - Contains the `Yummi` class, which is intended to support automation specific to the Yuumi champion.

### Overall Architecture and Design Patterns
The project follows a modular architecture, dividing responsibilities among various components to ensure maintainability and scalability. Key design patterns used include:

- **Singleton Pattern**: For managing the game state as a single instance.
- **Observer Pattern**: For adding listeners to the game loop, allowing different components to react to state changes.
- **Threading**: Used in the `ScreenReader` class to continuously capture the screen without blocking other operations.

### Important Technologies and Frameworks
The project leverages several technologies and frameworks to achieve its functionality:

- **Python**: The primary programming language used for the project.
- **OpenCV**: For image processing and screen reading.
- **PyAutoGUI**: For automating keyboard and mouse actions.
- **MSS**: For capturing screenshots.
- **Socket Library**: For managing socket communication between different components.

### Notable Features and Algorithms
- **Image Processing**: Utilizes OpenCV for capturing and analyzing the game screen to update the game state.
- **Auto-Heal Functionality**: Automatically casts healing spells when the player's health falls below a certain threshold.
- **Keyboard and Mouse Automation**: Provides methods for automating complex in-game actions through keyboard and mouse inputs.
- **Socket Communication**: Routes specific keyboard inputs to another computer, enabling multi-machine control.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

