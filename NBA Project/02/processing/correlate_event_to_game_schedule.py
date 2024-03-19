"""

The function finds the nearest scheduled NBA game to a missed game(MG)/inactive list (IL).
In most cases, the event date corresponds exactly with a scheduled game. However, in the 
cases it does not, the first game that occura after the event must be found.

"""

from datetime import timedelta
import pandas as pd

def correlate_event_to_game_schedule (teams_schedule_df, event_date, event_team):
    # ensure event_date is a datatime object
    event_date = pd.to_datetime(event_date)

    # ensure the 'Date' column in teams_schedule_df is in datetime format
    teams_schedule_df['Date'] = pd.to_datetime(teams_schedule_df['Date'])

    # slice team_schedules_df to those games that occured on or after event (only include games for team of interest)
    after_event_df = teams_schedule_df.loc[(teams_schedule_df['Date'] >= event_date) & (teams_schedule_df['Team'] == event_team)]
    
    #empty dataframe means event occured in offseason in between a team name/city change
    if after_event_df.empty:
        team_name_change = {
            'Charlotte Bobcats': 'Charlotte Hornets',
            'New Orleans Hornets': 'New Orleans Pelicans',}
        # change team name if applicable
        if event_team in team_name_change:
            event_team = team_name_change[event_team]
            after_event_df = teams_schedule_df.loc[(teams_schedule_df['Date'] >= event_date) & (teams_schedule_df['Team'] == event_team)]

    # reset data without adding old index as column
    after_event_df.reset_index(drop = True, inplace = True)

    # handle the case where no matching games are found
    if after_event_df.empty:
        return None, None, 'off', None, 0
    # the first row in DataFrame corresponds to the game that is closest to (on or after) the event
    closest_game_event_df = after_event_df.iloc[0]

    # identify game number corresponding to event
    # game numbers go from 1-82 for regular season games
    game_number = closest_game_event_df['Game_num']
    game_date = closest_game_event_df['Date']

    # identify season and year in which event occured
    # event occured during the regular or post season
    season = closest_game_event_df['Season'] if game_number != 1 else 'off'
    year = closest_game_event_df['Year']


    # find the total number of games the team played in during season
    team_total = 0
    if season != 'off':
        team_total = teams_schedule_df[(teams_schedule_df['Team'] == event_team) & (teams_schedule_df['Season'] == season) & (teams_schedule_df['Year'] == year)]['Game_num'].max()
    
    return game_number, game_date, season, year, team_total