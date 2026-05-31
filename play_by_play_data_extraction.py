from bs4 import BeautifulSoup
import pandas as pd
from nba_players import players


def load_html_file(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def extract_game_data(file_path):
    """
    This function extract play-by-play data from an NBA game described by a webpage from www.nbaplaysdb.com

    The website www.nbaplaysdb.com performs server-side-rendering, which is why an API
    call is not sufficient, instead the generated HTML content needs to be parsed and the
    relevant data extracted. This function expects the webpage to be saved as an HTML
    file, and the path to this file should be provided as input for this function.

    The generated HTML does not use descriptive classes for its DIV elements, but instead
    uses class names to describe styling. Fortunately each piece of information is uniquely
    styled, which allows us to extract the relevant information using CSS selectors.

    The logic to derive different types of plays is pretty ugly (not gonna lie), but it works.
    This is a quick hobby project, so get off my back!

    Args:
        file_path(str): Path to the HTML file containing the game data.

    Returns:
        DataFrame containing the extracted game data.
    """
    soup = load_html_file(file_path)
    data = []

    # identify teams
    teams = soup.find('div', class_="text-xs font-bold tracking-wide text-muted-foreground uppercase font-mono").text
    home_team = teams[5:8]
    away_team = teams[-3:]

    # create a new row for each play
    previous_score = "0–0"
    for list_element in soup.find_all('li'):
        is_FGA = False
        is_FGM = False
        is_FTA = False
        is_FTM = False
        is_REB = False
        is_BLK = False
        is_TO = False
        is_STL = False
        is_PF = False
        is_AST = False
        is_jump_ball = False
        primary_player = None
        secondary_player = None
        play_identified = False

        score = list_element.find('div', class_="text-[11px] font-mono tabular-nums px-2 py-0.5 rounded-full bg-background border border-border text-muted-foreground").text
        minute = list_element.find('div', class_="text-[10px] text-muted-foreground/70 mt-1 font-mono").text
        team = list_element.find('span', class_="text-[10px] font-bold uppercase tracking-wide").text
        description = list_element.find('a').find_all('div')[2].text

        score_away = int(score.split('–')[0])
        score_home = int(score.split('–')[1])

        if 'Jump Ball' in description:
            is_jump_ball = True
            play_identified = True

        if 'Assist' in description:
            is_AST = True
            play_identified = True

        if 'MISS' in description:
            is_FGA = True
            play_identified = True

            for player in players:
                if player.identifier in description:
                    primary_player = player.identifier
                    break

        if 'STEAL' in description:
            is_STL = True
            play_identified = True

            for player in players:
                if description.startswith(player.identifier):
                    primary_player = player.identifier
                    break

        if 'REBOUND' in description:
            is_REB = True
            play_identified = True

        if 'BLOCK' in description:
            is_BLK = True
            play_identified = True

        if 'TURNOVER' in description:
            is_TO = True
            play_identified = True

        if 'Free Throw' in description:
            is_FTA = True
            if score != previous_score:
                is_FTM = True
            play_identified = True

            for player in players:
                if description.startswith(player.identifier):
                    primary_player = player.identifier
                    break
        else:
            if score != previous_score:
                is_FGA = True
                is_FGM = True
                play_identified = True

            for player in players:
                if description.startswith(player.identifier):
                    primary_player = player.identifier
                    break

        if 'personal FOUL' in description:
            is_PF = True
            play_identified = True

            for player in players:
                if description.startswith(player.identifier):
                    primary_player = player.identifier
                    break
            for player in players:
                if player.last_name in description and player.identifier != primary_player:
                    secondary_player = player.identifier
                    break

        data.append({
            'game': None,
            'period': None,
            'minute': minute,
            'away_team': away_team,
            'home_team': home_team,
            'score_away': score_away,
            'score_home': score_home,
            'description': description,
            'play_by': team,
            'play_primary_player': primary_player,
            'play_secondary_player': secondary_player,
            'is_FGA': is_FGA,
            'is_FGM': is_FGM,
            'is_FTA': is_FTA,
            'is_FTM': is_FTM,
            'is_REB': is_REB,
            'is_BLK': is_BLK,
            'is_TO': is_TO,
            'is_STL': is_STL,
            'is_PF': is_PF,
            'is_AST': is_AST,
            'is_jump_ball': is_jump_ball,
            'play_identified': play_identified
        })

        previous_score = score

    df = pd.DataFrame(data)
    return df
