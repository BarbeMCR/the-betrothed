# BarbeMCR's The Betrothed
BarbeMCR's The Betrothed is a platformer written in Python with the aid of Pygame.

## How do I run the code?
### If you just want to play BarbeMCR's The Betrothed:

- Use the BarbeMCR's The Betrothed Launcher (learn about it [here](https://github.com/BarbeMCR/the-betrothed-launcher))
- Do everything manually

If you chose the second option, here is how you can play BarbeMCR's The Betrothed (don't worry, it isn't very difficult):

**On Windows**
1. Go on the `Releases` page and check for the latest stable version (or any other one, if you want)
2. Download the file that best matches your system:
   - The latest Python release for **Windows 8.1 and higher**: `the_betrothed_<version>_py3x.zip`
   - Python 3.8.10 for **Windows Vista, 7 and 8**: `the_betrothed_<version>_py38.zip`

   *__All Windows executables are 32-bit, which means they are compatible with both x86 and x64 architectures.__*
   
   *__In order to run on Windows 8.1 and lower, you (in theory) need to have Microsoft Visual C++ 2015 installed (it comes as an update package, or you can get it from [here](https://www.microsoft.com/en-us/download/details.aspx?id=52685))__*
3. Extract the `.zip` file
4. Start `the_betrothed.exe`

*Note: either your antivirus or Microsoft SmartScreen might block the file thinking it's a virus. BarbeMCR's The Betrothed is **not** a virus. If you don't trust me, check the code for yourself. Please make an exception for the folder you extracted BarbeMCR's The Betrothed in or ignore the Microsoft SmartScreen warning. Thank you!*

**On macOS, Linux, UNIX or other platforms**
1. Download and install Python 3.8 or higher from [python.org](https://python.org), if you haven't already
2. Install the right version of pygame for your target version (table below): `python -m pip install pygame==x.y.z`, if you haven't already
3. Go on the `Releases` page and check for the latest stable version (or any other one, if you want)
4. Download `the_betrothed_<version>_source.zip`
5. Extract the `.zip` file
6. Start `main.py`

**Do you need to upgrade 0.12 savefiles to version 0.13 or higher?**
If so, check out [BarbeMCR/tb012to013](https://github.com/BarbeMCR/tb012to013).

### If you instead want the source code:
1. Download and install Python 3.8 or higher from [python.org](https://python.org), if you haven't already
2. Install the right version of pygame for your target version (table below): `python -m pip install pygame==x.y.z`, if you haven't already
3. Go on the `Releases` page and check for whatever version you want to run
4. Download the `the_betrothed_<version>_source.zip`
5. Extract the archive
6. To start BarbeMCR's The Betrothed, run `main.py`

## How do I compile the code?
1. Make sure to have Python 3.8 or higher and the right version of pygame, as in the table below (use a 32-bit Python version for wider compatibility)
2. Grab the Pyinstaller version that matches what is used with your target game version, if you want (probably you can just use the latest version):

| BarbeMCR's The Betrothed version | Pyinstaller version |
| -------------------------------- | ------------------- |
| 0.01                             | 4.7                 |
| 0.02                             | 4.8                 |
| 0.03                             | 4.9                 |
| 0.04                             | 4.10                |
| 0.05 - 0.06                      | 5.0.1               |
| 0.07 - 0.11a                     | 5.1                 |
| 0.12                             | 5.2                 |
| 0.13 - 0.15                      | 5.3                 |
| 0.16 - 0.19                      | 5.6.2               |
| 0.20 +                           | 5.7.0               |

3. Compile with Pyinstaller using the `--onefile` argument

**Game version to pygame version conversion table**
| BarbeMCR's The Betrothed version | pygame version |
| -------------------------------- | -------------- |
| 0.01 - 0.15                      | 2.1.2          |
| 0.16 +                           | 2.1.3.dev8 / 2.1.3 |

---
## Settings
In the settings screen, you'll find various options, listed below.
- **Controller:** this option lets you change the controller layout used by the game to best match your hardware. You can choose between three options: `Xbox One / Xbox X|S / Xbox 360`, `Dualshock 4` and `Nintendo Switch Pro`. By default this option is set to `Xbox One / Xbox X|S / Xbox 360`.
- **Music volume:** this option lets you change the music volume. You can choose between six options: `0%`, `10%`, `25%`, `50%`, `75%`, `100%`. This option only affects the volume of music, not that of SFXs. By default this option is set to `50%`.
- **VSync:** this options lets you specify whether to enable VSync. If VSync is enabled, the framerate will be synced (and limited) to your monitor's refresh rate. This generally reduces screen tearing. Keep in mind that even if the framerate is higher than your monitor's refresh rate, the "extra" frames will not be displayed. VSync also has the benefit to give a more fluid gameplay experience (it is not guaranteed though, as it greatly varies depending on your specific hardware). You can choose between two options: `Enabled` and `Disabled`. By default this option is set to `Enabled`. It is highly recommended to keep VSync on. Changing this setting *__requires restarting the game__* in order for it to be applied. VSync may not work on some hardware configurations, *even if enabled in the settings*.
- **Maximum framerate:** this option lets you change the framerate cap. You can choose between nine options: `20 FPS`, `30 FPS`, `50 FPS`, `60 FPS`, `72 FPS`, `90 FPS`, `120 FPS`, `144 FPS` and `No limit`. By default this option is set to `60 FPS`. If VSync is enabled, selecting a framerate cap higher than your monitor's refresh rate won't have any effect. It is *__HIGHLY__* recommended to keep the framerate cap lower than or equal to 60 FPS. 72 FPS is considered the highest "safe" framerate. Starting from 90 FPS, you could start to notice some slight glitches in moving sprites. Higher framerates could prevent the slowest sprites from moving at all. Keep in mind that BarbeMCR's The Betrothed was designed with 60 FPS as the target framerate. Playing with a framerate cap set higher than 72 FPS should be considered *__unsupported__*. *__USE WITH CAUTION!__* Changing this setting *__requires restarting the game__* in order for it to be applied.
- **Fade effect:** this option lets you toggle the fade transition that happens when spawning in and leaving a level. You can choose between two options: `Enabled` and `Disabled`. Having the fade effect enabled could cause temporary lag when spawning or leaving. However, it is much nicer having the transition on. By default this option is set to `Enabled`.
- **Autodownload:** this option lets you specify whether to enable autodownload. If autodownload is enabled, new versions are automatically downloaded and placed in './data' at startup. You can choose between two options: `Disabled` and `Enabled`. If you want an easier way to update the game, check out the [BarbeMCR's The Betrothed Launcher](https://github.com/BarbeMCR/the-betrothed-launcher). By default this option is set to `Disabled`.
- **Delete Game:** this lets you delete a previously generated savefile. You will be asked for the name of the savefile to delete. Keep in mind the savefile will be deleted *__permanently__*.
- **Reset Settings:** this lets you reset the settings to their default values.

---
## Controls
### While playing

*__Keyboard + Mouse__*
| Input | Action |
| ----- | ------ |
| A     | Walk left |
| D     | Walk right |
| Space | Jump |
| J     | Melee attack |
| K     | Ranged attack |
| L     | Magical attack |
| A/D + Left Ctrl [+ Left Alt] | Run (changes speed) |
| Backslash | Toggle overlay |
| F2    | Take screenshot |
| F11   | Toggle fullscreen |

*__Xbox 360 / Xbox One / Xbox Series X|S Controller__*
| Input | Action |
| ----- | ------ |
| D-Pad Left | Walk left |
| D-Pad Right | Walk right |
| A     | Jump |
| B     | Melee attack |
| X     | Ranged attack |
| Y     | Magical attack |
| RT    | Run |
| XBOX  | Toggle overlay |
| SHARE (if available) | Take screenshot |

*__DualShock 4__*
| Input | Action |
| ----- | ------ |
| Left  | Walk left |
| Right | Walk right |
| Cross | Jump |
| Circle | Melee attack |
| Square | Ranged attack |
| Triangle | Magical attack |
| R2    | Run |
| PLAYSTATION | Toggle overlay |
| TOUCHPAD CLICK | Take screenshot |

*__Nintendo Switch Pro Controller__*
| Input | Action |
| ----- | ------ |
| Left  | Walk left |
| Right | Walk right |
| A     | Jump |
| B     | Melee attack |
| X     | Ranged attack |
| Y     | Magical attack |
| ZR    | Run |
| HOME  | Toggle overlay |
| CAPTURE | Take screenshot |

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

### In the menus

*__Keyboard__*
| Input | Action |
| ----- | ------ |
| Left Arrow / Up Arrow | Move cursor back |
| Right Arrow / Down Arrow | Move cursor forward |
| Space | Select |

*__Xbox 360 / Xbox One / Xbox Series X|S Controller__*
| Input | Action |
| ----- | ------ |
| LB    | Move cursor back |
| RB    | Move cursor forward |
| A     | Select |

*__Dualshock 4__*
| Input | Action |
| ----- | ------ |
| L1    | Move cursor back |
| R1    | Move cursor forward |
| Cross | Select |

*__Nintendo Switch Pro Controller__*
| Input | Action |
| ----- | ------ |
| L     | Move cursor back |
| R     | Move cursor forward |
| A     | Select |

### In the text input boxes

*__Keyboard__*
| Input | Action |
| ----- | ------ |
| Any key | Enter text |
| Return | Confirm |

---
## Credits

@BarbeMCR (aka myself) - Programming, graphics, music, SFXs, font, level design, mechanics... (I created the game and since this is a solo project don't expect many people working on development)

**But, most importantly, everybody who contributed with testing and various tidbits, like those folks:**

-  No one for now
