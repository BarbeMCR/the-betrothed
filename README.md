# BarbeMCR's The Betrothed
The Betrothed is a platformer written in Python with the aid of Pygame.

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BarbeMCR/the-betrothed.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BarbeMCR/the-betrothed/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/BarbeMCR/the-betrothed.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BarbeMCR/the-betrothed/alerts/)

## How do I run the code?
**If you just want to play The Betrothed:**
1. Go on the `Releases` page and check for the latest stable version (or any other one, if you want)
2. Download the file that best matches your system:
   - Python 3.8.10 for **Windows Vista and higher**: for example `the_betrothed_001_py38.zip`
   - The latest Python release for **Windows 8.1 and higher**: for example `the_betrothed_001_py310.zip`

   *__All executables are 32-bit, which means they are compatible with both x86 and x64 architectures.__*
3. Extract the `zip` file
4. Start `the_betrothed.exe`

*Note: either your antivirus or Microsoft SmartScreen might block the file thinking it's a virus. The Betrothed is **not** a virus. If you don't trust me, check the code for yourself. Please make an exception for the folder you extracted The Betrothed in or ignore the Microsoft SmartScreen warning. Thank you!*

**If you instead want to run the source code:**
1. Go on the `Releases` page and check for whatever version you want to run
2. Download the `the_betrothed_<version>_source.zip`
3. Extract the archive
4. Run `main.py` with at least Python 3.8 (probably it works with previous versions but I don't guarantee)

## How do I compile the code?
1. Make sure to have Python 3.8 or higher (32-bit Python for wider compatibility)
2. Grab the Pyinstaller version that matches what is used with your target game version:

| The Betrothed version | Pyinstaller version |
| --------------------- | ------------------- |
| 0.01                  | 4.7                 |
| 0.02                  | 4.8                 |
| 0.03                  | 4.9                 |
| 0.04                  | 4.10                |
| 0.05 - 0.06           | 5.0.1               |
| 0.07 +                | 5.1                 |

3. Compile with Pyinstaller using the `--onefile` argument

---
## Controls
### While playing

*__Keyboard__*
| Input | Action |
| ----- | ------ |
| A     | Walk left |
| D     | Walk right |
| Space | Jump |
| F11 | Toggle fullscreen |

*__Xbox 360 / Xbox One / Xbox Series X|S Controller__*
| Input | Action |
| ----- | ------ |
| D-Pad Left | Walk left |
| D-Pad Right | Walk right |
| A     | Jump |

*__DualShock 4__*
| Input | Action |
| ----- | ------ |
| Left  | Walk left |
| Right | Walk right |
| Cross | Jump |

*__Nintendo Switch Pro Controller__*
| Input | Action |
| ----- | ------ |
| Left  | Walk left |
| Right | Walk right |
| A     | Jump |

### In the level selection screen

*__Keyboard__*
| Input | Action |
| ----- | ------ |
| Left Arrow | Move to previous level |
| Right Arrow | Move to following level |
| Space | Select level |

*__Xbox 360 / Xbox One / Xbox Series X|S Controller__*
| Input | Action |
| ----- | ------ |
| LB    | Move to previous level |
| RB    | Move to following level |
| A     | Select level |

*__DualShock 4__*
| Input | Action |
| ----- | ------ |
| L1    | Move to previous level |
| R1    | Move to following level |
| Cross | Select level |

*__Nintendo Switch Pro Controller__*
| Input | Action |
| ----- | ------ |
| L     | Move to previous level |
| R     | Move to following level |
| A     | Select level |

---
## Credits

@BarbeMCR (aka myself) - Programming, graphics, music, SFXs, font, level design, mechanics... (I created the game and since this is a solo project don't expect many people working on the actual game)

**But, most importantly, everybody who contributed with testing and various tidbits, like those folks:**

- Aleee - Early testing, early controller testing
