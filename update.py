import urllib.request
import shutil
import configparser
import pygame
import sys
import os

"""This file defines some functions used for various tasks involved with updating."""

def check_updates(version_id, display_surface):
    """Check for updates.

    Arguments:
    version_id -- the build to check against
    display_surface -- the screen
    """
    try:
        with urllib.request.urlopen('https://raw.githubusercontent.com/BarbeMCR/the-betrothed/main/latest.ini') as latest:
            data = latest.read().decode(latest.info().get_param('charset', 'utf-8'))
        config = configparser.ConfigParser()
        config.read_string(data)
        latest = config['latest']
        id = latest['id']
        version = latest['version']
        if sys.platform.startswith('win32'):
            import platform
            if platform.version().startswith(('10.0', '6.3')):
                download_file = f"the_betrothed_{latest['download_version']}_py{latest['download_python_version']}.zip"
            elif platform.version().startswith(('6.2', '6.1', '6.0')):
                download_file = f"the_betrothed_{latest['download_version']}_py38.zip"
            else:
                download_file = f"the_betrothed_{latest['download_version']}_source.zip"
        else:
            download_file = f"the_betrothed_{latest['download_version']}_source.zip"
        download_url = 'https://github.com/BarbeMCR/the-betrothed/releases/latest/download/' + download_file
        settings = configparser.ConfigParser()
        settings.read('./data/settings.ini')
        autodownload = settings.getboolean('autodownload', 'autodownload')
        if version_id < int(id) and not os.path.isfile('./data/' + download_file):
            show_banner(version, display_surface)
            if autodownload:
                download_update(download_url, download_file)
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass

def download_update(download_url, filename):
    """Download an update from a URL.

    Arguments:
    download_url -- the URL to download from
    filename -- the name of the output file
    """
    filename = './data/' + filename
    with urllib.request.urlopen(download_url) as download_file:
        with open(filename, 'wb') as local_file:
            shutil.copyfileobj(download_file, local_file)

def show_banner(version, display_surface):
    """Show an update banner in pygame.

    Arguments:
    version -- the latest version
    display_surface -- the screen
    """
    font = pygame.font.Font('./font.ttf', 18)
    text = [
        "Update available!",
        f"Latest version: {version}",
        "The update will automatically be downloaded",
        "and put in './data' if autodownload",
        "is enabled in the settings.",
        "The program might hang while downloading."
    ]
    display_surface.fill('black')
    y = 256
    for string in text:
        surface = font.render(string, False, 'white')
        rect = surface.get_rect(midtop=(display_surface.get_rect().centerx, y))
        display_surface.blit(surface, rect)
        y += 32
    pygame.display.flip()
    pygame.event.pump()
    pygame.time.wait(5000)
