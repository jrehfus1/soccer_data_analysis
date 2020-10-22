################################################################################
#author: JER
#date of last modification: 201022
#summary of last modification: separated this script from other season-spanning analyses of goals data for clarity

################################################################################
##### description #####
#this script generates one plot, based on goals data from a single EPL season
#   1) outcomes of EPL matches versus the distance the away team traveled
#       TODO add a statistical test to see if there is a correlation? do logistic regression instead?

################################################################################
##### import packages #####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

################################################################################
##### decide whether or not to save the figures that this script produces #####
save_figs = False
out_path_figs = '../../figures/exploratory_figures/'

################################################################################
##### read in the data file containing the goals data from the season of choice #####
#season_span = '19_20'
season_span = input('\n=== Enter season span (eg. 19_20): ')
in_file = season_span + '_PL_goals_web_data.csv'
in_path = '../../data/raw_data/'
match_results_df = pd.read_csv(in_path+in_file)

################################################################################
##### determine which games were won by the home team #####
home_team_goal_difference = match_results_df['home final score'] -  match_results_df['away final score'] #makes a new data series with home team goal diff for each match

match_outcome_array = np.zeros(away_team_travel_distance_series.size)
match_outcome_array[home_team_goal_difference>0] = 1 #home team won
match_outcome_array[home_team_goal_difference<0] = -1 #away team won
match_outcome_array = match_outcome_array[:, np.newaxis] #make a column vector for compatibility with sklearn
#print(away_team_travel_distance_series.shape)

################################################################################
##### define haversine function to calculate great circle distance between two points on earth #####
#I used this site as a reference: https://www.movable-type.co.uk/scripts/latlong.html
#coordinates should be input as signed decimal degrees (positive indicates N/E, negative indicates S/W)
#here we assume that the earth is spherical, which should produce answers accurate to within ~0.5%
def haversine(A_lat_deg, A_long_deg, B_lat_deg, B_long_deg):
    r_earth = 6371000 #mean radius of the earth in meters (6,371km)

    A_lat_rad = np.pi*(A_lat_deg/180) #convert degrees to radians
    A_long_rad = np.pi*(A_long_deg/180) #convert degrees to radians
    B_lat_rad = np.pi*(B_lat_deg/180) #convert degrees to radians
    B_long_rad = np.pi*(B_long_deg/180) #convert degrees to radians

    delta_lat_rad = B_lat_rad - A_lat_rad #get the difference in radians between the two latitudes
    delta_long_rad = B_long_rad - A_long_rad #get the difference in radians between the two longitudes

    a_term = ( np.sin(delta_lat_rad/2)**2 ) + ( np.cos(A_lat_rad) * np.cos(B_lat_rad) * ( np.sin(delta_long_rad/2)**2 ) ) #square of half the chord length between the points
    c_term = 2 * np.arctan2( a_term**0.5, (1-a_term)**0.5 ) #angular distance in radians via element-wise arctan of x1/x2
    gc_dist = r_earth * c_term #great circle distance (in meters) between the two points

    return round(gc_dist/1000, 2) #return the great circle distance in kilometers with two decimal places
#print( haversine(51.556667, -0.106111, 50.861822, -0.083278) )

################################################################################
##### determine the difference traveled by the away team for each match #####
stadium_info_df = pd.read_csv('../../data/tidy_data/stadium_info.csv')
stadium_info_df.set_index('stadium_name', inplace=True) #make the stadium name the index

away_team_travel_distance_series = match_results_df.apply(lambda row: haversine(stadium_info_df.loc[stadium_info_df['home_team'] == row['home team name'], 'latitude'][0], stadium_info_df.loc[stadium_info_df['home_team'] == row['home team name'], 'longitude'][0], stadium_info_df.loc[stadium_info_df['home_team'] == row['away team name'], 'latitude'][0], stadium_info_df.loc[stadium_info_df['home_team'] == row['away team name'], 'longitude'][0]), axis=1) #USE ROW DATA TO LOOK UP STADIUM INFO
away_team_travel_distance_array = np.array(away_team_travel_distance_series.values.tolist())
away_team_travel_distance_array = away_team_travel_distance_array[:, np.newaxis] #make a column vector for compatibility with sklearn
#print( away_team_travel_distance_array.shape )

################################################################################
##### fit a line to the match outcome versus distance data #####
linear_model = LinearRegression(fit_intercept=True)
linear_model.fit(away_team_travel_distance_array, match_outcome_array)
#print( linear_model.coef_, linear_model.intercept_ )

dist_to_fit = np.arange(0, 501)
dist_to_fit = dist_to_fit[:, np.newaxis]
outcome_fit = linear_model.predict(dist_to_fit)
#print( outcome_fit )

################################################################################
##### plot the match outcome versus travel distance #####
fig_01 = plt.figure(figsize=(5, 5))
fig_01.suptitle('Season: ' + season_span)
grid_01 = plt.GridSpec(3, 3)
axes_01 = []
axes_01.append( fig_01.add_subplot(grid_01[:, :]) )

axes_01[0].set_title('travel effects')
axes_01[0].set_xlabel('away team distance traveled (km)', fontsize=14, color='black')
axes_01[0].set_ylabel('match outcome', fontsize=14, color='black')
axes_01[0].set_xlim(0, 500)
axes_01[0].set_ylim(-1.5, 1.5)

axes_01[0].scatter( away_team_travel_distance_series[home_team_goal_difference < 0], np.ones(away_team_travel_distance_series[home_team_goal_difference < 0].size), marker='h', facecolor=(0.37,0.73,0.49), edgecolor='black', linewidth=1, s=50 ) #plot points for every away team victory
axes_01[0].scatter( away_team_travel_distance_series[home_team_goal_difference > 0], -np.ones(away_team_travel_distance_series[home_team_goal_difference > 0].size), marker='h', facecolor=(0.69,0.23,0.56), edgecolor='black', linewidth=1, s=50 ) #plot points for every home team victory
axes_01[0].scatter( away_team_travel_distance_series[home_team_goal_difference == 0], np.zeros(away_team_travel_distance_series[home_team_goal_difference == 0].size), marker='h', facecolor='gray', edgecolor='black', linewidth=1, s=50 ) #plot points for every draw

axes_01[0].plot( dist_to_fit, outcome_fit, linewidth=2.0, linestyle='-', color=(0.07,0.41,0.98) ) #plot the fit of a line to the data to illustrate the correlation

################################################################################
##### show the figures #####
plt.show()
