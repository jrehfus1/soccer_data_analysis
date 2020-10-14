# What can we learn about the beautiful game from data?
Soccer (football) is the most-watched sport on the planet. It is an exciting game, played the world over, contested by determined competitors, celebrated by passionate fans, and producing moments of sheer brilliance that are remebered for generations. Here, I will provide quantitative insight into this beloved sport by applying data analytics to the *English Premier League* (EPL).

#### Data source and structure
The raw data has been compiled from [www.worldfootball.net](www.worldfootball.net) and stored in CSV files. Each CSV file contains the scores from all matches in a single EPL season.
The columns in the CSV files are:
+ match week
+ date
+ home team name
+ away team name
+ home team final score
+ away team final score
+ home team goal times
+ away team goal times

#### Scripts I: data cleaning, processing, and analysis
1) `calculate_weekly_match_results_data.py`
uses the match results from one season to calculate: 
+ weekly cumulative league points for each team in a single season
+ weekly cumulative goal difference for each team in a single season
+ weekly cumulative goals scored for each team in a single season
+ weekly league position for each team in a single season

2) `calculate_avg_weekly_league_data.py`
uses weekly data calculated over a five season span to calculate:
+ the mean and standard deviation of weekly cumulative league points for each team grouped by their final league positions
+ the mean and standard deviation of weekly cumulative goal difference for each team grouped by their final league positions
+ the mean and standard deviation of weekly cumulative goals scored for each team grouped by their final league positions
+ the mean and standard deviation of weekly league position for each team grouped by their final league positions

3) `compile_final_season_results.py`
collects data from the final week of the season for a five season span to compile:
+ final league position
+ final league points
+ final goal difference
+ final total number of goals scored
+ final total number of goals conceded

#### Scripts II: visualization and model fitting
1) `plot_season_goals_data.py`
uses the raw CSV data files to plot:
+ a histogram of the time of the game at which all goals from all matches during a single season were scored 
    - a Chi-square test is used to determine whether or not goals are scored uniformly throughout matches
+ a histogram of the total number of goals scored in all matches from a single season
		this histogram is fit to a Poisson distribution
+ a histogram of the final goal difference in all matches from a single season
+ a histogram of the final goal difference in all matches from a single season from the perspective of the home team 
    - a Chi-square test is used to determine whether or not the home and away teams are equally likely to win

2) `team_colors.py`
contains dictionaries of the RGB primary and secondary colors used by PL teams (these colors are helpful when plotting the performance of multiple teams on the same axes).

3) `plot_weekly_match_results_data.py`
uses the output of calculate_weekly_match_results_data.py to plot: 
+ weekly cumulative league points for each team in a single season
+ weekly cumulative goal difference for each team in a single season
+ weekly cumulative goals scored for each team in a single season
+ weekly league position for each team in a single season

4) `plot_avg_weekly_league_data.py`
uses the output of calculate_avg_weekly_league_data.py to plot: 
+ the mean and standard deviation of weekly cumulative league points for each team grouped by their final league positions
+ the mean and standard deviation of weekly cumulative goal difference for each team grouped by their final league positions
+ the mean and standard deviation of weekly cumulative goals scored for each team grouped by their final league positions
+ the mean and standard deviation of weekly league position for each team grouped by their final league positions

5) `plot_final_season_results.py`
uses the output of compile_final_season_results.py to plot correlations between the following parameters: 
+ final league position
+ final league points
+ final goal difference
+ final total number of goals scored
+ final total number of goals conceded

#### Results summary
A full discussion of the results of these exploratory analyses is presented in the *report.pdf* file.