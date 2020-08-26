# soccer_data_analysis
What can we learn about the beautiful game from data?

Data source: www.worldfootball.net
The data have been compiled in CSV files.
Each CSV file contains the scores from all matches in a single Premier League season.
The columns in the CSV files are:
match week, date, home team name, away team name, home final score, away final score, home goal times, away goal times

The following scripts are for data cleaning, processing, visualization, and analysis.

plot_league_goals.py
This script is useful for analyzing the goals scored in each game of a given season.

This script will plot:
1) a histogram showing the number of goals scored in each time bin
2) a histogram showing the total number of goals scored in each match
3) a histogram showing the goal difference in each match

In addition:
1) a Chi-square test is used to determine whether or not goals were scored with uniform probability throughout matches
2) a Poisson probability mass function is fit to the goal difference data to see if

plot_league_points.py
This script is useful for analyzing the league points acquired by each team in a given season.

This script will plot:
1) the league points acquired by each team versus match week
2) the goal differential for each team versus match week
3) the total number of goals scored by each team versus match week
4) the resultant league position of each team versus match week
5) TODO the number of league positions that changed hands versus match week

In addition:
1) TODO fit the league positions switch data to a __ model

A discussion of the results of these analyses is presented in the "REPORT.pdf" file.
