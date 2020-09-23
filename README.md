# soccer_data_analysis
What can we learn about the beautiful game from data?

##################################################
Data source: www.worldfootball.net
The raw data have been compiled in CSV files.
Each CSV file contains the scores from all matches in a single Premier League season.
The columns in the CSV files are:
match week, date, home team name, away team name, home final score, away final score, home goal times, away goal times

##################################################
The following scripts are used for data cleaning, processing, and analysis:
1) calculate_weekly_match_results_data.py
	this script uses the match results from one season to calculate: 
	a) weekly cumulative league points for each team in a single season
	b) weekly cumulative goal difference for each team in a single season
	c) weekly cumulative goals scored for each team in a single season
	d) weekly league position for each team in a single season

2) calculate_avg_weekly_league_data.py
	this script uses weekly data calculated over a five season window to calculate:
	a) the mean and standard deviation of weekly cumulative league points for each team grouped by their final league positions
	b) the mean and standard deviation of weekly cumulative goal difference for each team grouped by their final league positions
	c) the mean and standard deviation of weekly cumulative goals scored for each team grouped by their final league positions
	d) the mean and standard deviation of weekly league position for each team grouped by their final league positions

3) compile_final_season_results.py
	this script collects data from the final week of the season for a five season window to compile:
	a) final league position
	b) final league points
	c) final goal difference
	d) final total number of goals scored
	e) final total number of goals conceded

##################################################
The following scripts are used for data visualization and model fitting:
1) plot_season_goals_data.py
	this script uses the raw data files to plot:
	a) a histogram of the time of the game at which all goals from all matches during a single season were scored
		a Chi-square test is used to determine whether or not goals are scored uniformly throughout matches
	b) a histogram of the total number of goals scored in all matches from a single season
		this histogram is fit to a Poisson distribution
	c) a histogram of the final goal difference in all matches from a single season
	d) a histogram of the final goal difference in all matches from a single season from the perspective of the home team
		a Chi-square test is used to determine whether or not the home and away teams are equally likely to win

2) team_colors.py
	this script contains dictionaries of the RGB primary and secondary colors used by PL teams.
	these colors are helpful when plotting the performance of multiple teams on the same axes.

3) plot_weekly_match_results_data.py
	this script uses the output of calculate_weekly_match_results_data.py to plot: 
	a) weekly cumulative league points for each team in a single season
	b) weekly cumulative goal difference for each team in a single season
	c) weekly cumulative goals scored for each team in a single season
	d) weekly league position for each team in a single season

4) plot_avg_weekly_league_data.py
	this script uses the output of calculate_avg_weekly_league_data.py to plot: 
	a) the mean and standard deviation of weekly cumulative league points for each team grouped by their final league positions
	b) the mean and standard deviation of weekly cumulative goal difference for each team grouped by their final league positions
	c) the mean and standard deviation of weekly cumulative goals scored for each team grouped by their final league positions
	d) the mean and standard deviation of weekly league position for each team grouped by their final league positions

5) plot_final_season_results.py
	this script uses the output of compile_final_season_results.py to plot correlations between the following parameters: 
	a) final league position
	b) final league points
	c) final goal difference
	d) final total number of goals scored
	e) final total number of goals conceded

##################################################
A discussion of the results of these exploratory analyses is presented in the "report.pdf" file.
