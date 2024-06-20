'''
Copyright 2023 Nicholas Kaplan
11/13/2023
ISTA 131 Final Project
'''

import pandas as pd, numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import matplotlib.pyplot as plt
import statsmodels.api as sm
import math

#Fig 1 functions
def make_heatmap_df(df):
    '''
    This function takes LA crime data from 2022 and counts the number of crimes at each longitute-latitude coordinate.
    Parameters:
    df: an LA crime df
    returns:
    result_df: a df with all lon-lat coordinates with a crime count for each pair
    '''
    index = []
    result_df = pd.DataFrame(columns = ['LAT', 'LON', 'Count'])
    for ind in df.index:
        temp = str(df.loc[ind,'LAT']) + '_' + str(df.loc[ind,'LON'])
        if temp in result_df.index:
            result_df.loc[temp,'Count'] += 1
        else:
            
            result_df.loc[temp, 'LAT'] = df.loc[ind,'LAT']
            result_df.loc[temp, 'LON'] = df.loc[ind, 'LON']
            result_df.loc[temp, 'Count'] = 1
    return result_df

def make_heatmap_fig(heatmap_df):
    '''
    This function creates a heatmap of LA crime.
    heatmap_df: a make_heatmap_df() df
    Returns: None
    '''
    fig = px.density_mapbox(heatmap_df, lat = 'LAT', lon = 'LON', z = 'Count',
                        radius = 8,
                        center = dict(lat = 34.0549, lon = -118.2426),
                        zoom = 8.25,
                        mapbox_style = 'open-street-map',
                        title = '2022 LA Crime Heatmap')
    fig.update_layout(font=dict(size=18))
    fig.show()


#fig 2 functions
def make_fig_2_df(df):
    '''
    This function creates the dataframe used for fig 2.
    Parameters: 
    df: an LA crime data df
    returns:
    crimes_per_month: a dataframe with the number of crimes committed each month.
    '''
    crimes_per_month = pd.DataFrame(index = [1,2,3,4,5,6,7,8,9,10,11,12], data = 0, columns =['Count', 'Average'])
    add_count_to_crimes_per_month(df, crimes_per_month)
    add_average(crimes_per_month)
    set_month_names(crimes_per_month)
    return crimes_per_month

def add_count_to_crimes_per_month(df, crimes_per_month):
    '''
    This function fills in data to a crimes_per_month df
    parameters:
    df: an LA crime data df
    crimes_per_month: a dataframe with indexes 1-12 and a count and a average column
    Returns: None
    '''
    for ind in df.index:
        crimes_per_month.loc[df.loc[ind, 'DATE OCC'].month , 'Count'] += 1

def add_average(crimes_per_month):
    '''
    This function adds the average daily crime to a crimes_per_month df
    Parameters: a crimes_per_month df with add_count_to_crimes_per_month already called to it
    Returns: none
    '''
    days_dict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    for ind in crimes_per_month.index:
        crimes_per_month.loc[ind, 'Average'] = crimes_per_month.loc[ind,'Count'] / days_dict[ind]

def set_month_names(crimes_per_month):
    '''
    This function adds month names to a crimes_per_month df
    Parameters: a crimes_per_month df
    returns: None
    '''
    se = pd.Series(data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
          'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    crimes_per_month.loc[:,'Month_Names'] = se.values



def make_fig_2(crimes_per_month):
    '''
    This function creates the second visualization
    Parameters: a crimes_per_month df
    returns: None
    '''
    plt.style.use('Solarize_Light2')
    crimes_per_month.plot(kind ='scatter', y = 'Average', x = 'Month_Names')
    plt.xlabel('2022', fontsize = 15)
    plt.ylabel('Average Crimes Per Day', fontsize = 15)
    plt.title('LA Average Daily Crime Reports in 2022', fontsize = 20)
    #regression line stuff
    x = crimes_per_month.index - 1
    X = sm.add_constant(x)
    model = sm.OLS(crimes_per_month.Average, X)
    line = model.fit()
    y = line.params['x1']*x + line.params['const']
    plt.plot(x,y, color = 'black')

    plt.show()

    #fig 3 code
def make_sun_df():
    '''
    This function creates a dataframe with sunrise and sunset data for the year 2022
    Parameters: None
    Returns: a dataframe
    '''
    sun_df = pd.read_csv('LA_sunrise_sunset.csv', delim_whitespace = True, index_col = 0, header = None)
    sun_df.replace(0, np.nan, inplace=True)
    sun_df.columns = ['Jan_rise','Jan_set','Feb_rise','Feb_set','Mar_rise','Mar_set', 'Apr_rise', 'Apr_set', 'May_rise','May_set',
                 'Jun_rise','Jun_set','Jul_rise','Jul_set','Aug_rise','Aug_set','Sep_rise','Sep_set','Oct_rise','Oct_set',
                 'Nov_rise','Nov_set','Dec_rise','Dec_set']
    return sun_df

def fig_3_full_df(df, sun_df):
    '''
    This function creates a dataframe of all 2022 days, and adds eachs days sunrise and sunset to the df
    Parameters:
    df: a LA crime data df
    sun_df: a make_sun_df() df
    returns:
    plt_df: a df with every 2022 day and sunrise-sunset data
    '''
    #make dataframe
    first = datetime(2022,1,1)
    last = datetime(2022, 12,31)
    plt_df = pd.DataFrame(index = pd.date_range(first, last),
                          columns = ['day_crimes', 'day_cph', 'night_crimes', 'night_cph',
                                     'sunrise','sunset', 'sun_time' 'percent_sun'],
                          data = 0)
    #dict for sun_df conversion
    months = {1:'Jan', 2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun', 7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12 : 'Dec'}
    #assembling sunrise/set times
    for date in plt_df.index:
        month = str(months[date.month])
        plt_df.loc[date, 'sunrise'] = sun_df.loc[date.day, (month) + '_rise']
        plt_df.loc[date, 'sunset'] = sun_df.loc[date.day, (month) + '_set']
        rise_time = datetime(year = 2022, month = date.month, day = date.day, hour = int(plt_df.loc[date, 'sunrise']) // 100,
                         minute = int(plt_df.loc[date, 'sunrise']) %100)
        set_time = datetime(year = 2022, month = date.month, day = date.day, hour = int(plt_df.loc[date, 'sunset'] // 100),
                        minute = int(plt_df.loc[date, 'sunset'] %100))
        plt_df.loc[date, 'sun_time'] = set_time - rise_time
    return plt_df

def fig_3_crime_count(plt_df, df, sun_df):
    '''    
    This function fills in a fig_3_full_df() df
    Parameters:
    df: a LA crime data df
    sun_df: a make_sun_df() df
    plt_df: a fig_3_full_df() df
    Returns: None
    '''
    months = {1:'Jan', 2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun', 7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12 : 'Dec'}
    for elm in df.index:
        #prep for crime counts
        date = df.loc[elm,'DATE OCC']
        month = str(months[date.month])
        timeod = df.loc[elm, 'TIME OCC']
        rise_time = datetime(year = 2022, month = date.month, day = date.day, hour = int(plt_df.loc[date, 'sunrise']) // 100,
                         minute = int(plt_df.loc[date, 'sunrise']) %100)
        set_time = datetime(year = 2022, month = date.month, day = date.day, hour = int(plt_df.loc[date, 'sunset'] // 100),
                        minute = int(plt_df.loc[date, 'sunset'] %100))
        plt_df.loc[date, 'sun_time'] = set_time - rise_time
        
        if date > datetime(2022,3,13) and date < datetime(2022,11,6): #accounts for dsl
            if timeod + 100 > plt_df.loc[date, 'sunrise'] and timeod + 100 <= plt_df.loc[date, 'sunset']:
                plt_df.loc[date, 'day_crimes'] += 1
            else:
                plt_df.loc[date, 'night_crimes'] += 1             
        else:
            if timeod > plt_df.loc[date, 'sunrise'] and timeod <= plt_df.loc[date, 'sunset']:
                plt_df.loc[date, 'day_crimes'] += 1
            else:
                plt_df.loc[date, 'night_crimes'] += 1

def crimes_per_hr(plt_df):
    '''
    This function adds the hourly crime rate to a fig_3_crime_count() df
    Parameters:
    plt_df: a fig_3_crime_count() df
    Returns: None
    '''
    for elm in plt_df.index:
        st_hr = timedelta.total_seconds(plt_df.loc[elm, 'sun_time'])/3600
        dark = timedelta(hours = 24) - plt_df.loc[elm, 'sun_time']
        dark_hr = timedelta.total_seconds(dark)/3600
        plt_df.loc[elm, 'day_cph'] = plt_df.loc[elm, 'day_crimes'] /st_hr
        plt_df.loc[elm, 'night_cph'] = plt_df.loc[elm, 'night_crimes'] /dark_hr
def fig_3_fin(plt_df):
    '''
    This function converts the fig_3_crime_count() df into a df with monthly averages to be plotted
    Parameters:
    plt_df: a fig_3_crime_count() df
    Returns:
    fin_df: a plt_df sorted by month rather than day
    '''
    fin_df = pd.DataFrame(index = [1,2,3,4,5,6,7,8,9,10,11,12], columns = ['day_cph','night_cph'])
    fin_df.loc[1, 'day_cph'] = plt_df.loc[datetime(2022,1,1):datetime(2022,1,31), 'day_cph'].mean()
    fin_df.loc[1, 'night_cph'] = plt_df.loc[datetime(2022,1,1):datetime(2022,1,31), 'night_cph'].mean()
    fin_df.loc[2, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,2,28), 'day_cph'].mean()
    fin_df.loc[2, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,2,28), 'night_cph'].mean()
    fin_df.loc[3, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,3,31), 'day_cph'].mean()
    fin_df.loc[3, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,3,31), 'night_cph'].mean()
    fin_df.loc[4, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,4,30), 'day_cph'].mean()
    fin_df.loc[4, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,4,30), 'night_cph'].mean()
    fin_df.loc[5, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,5,31), 'day_cph'].mean()
    fin_df.loc[5, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,5,31), 'night_cph'].mean()
    fin_df.loc[6, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,6,30), 'day_cph'].mean()
    fin_df.loc[6, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,6,30), 'night_cph'].mean()
    fin_df.loc[7, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,7,31), 'day_cph'].mean()
    fin_df.loc[7, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,7,31), 'night_cph'].mean()
    fin_df.loc[8, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,8,31), 'day_cph'].mean()
    fin_df.loc[8, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,8,31), 'night_cph'].mean()
    fin_df.loc[9, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,9,30), 'day_cph'].mean()
    fin_df.loc[9, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,9,30), 'night_cph'].mean()
    fin_df.loc[10, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,10,31), 'day_cph'].mean()
    fin_df.loc[10, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,10,31), 'night_cph'].mean()
    fin_df.loc[11, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,11,30), 'day_cph'].mean()
    fin_df.loc[11, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,11,30), 'night_cph'].mean()
    fin_df.loc[12, 'day_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,12,31), 'day_cph'].mean()
    fin_df.loc[12, 'night_cph'] = plt_df.loc[datetime(2022,2,1):datetime(2022,12,31), 'night_cph'].mean()
    fin_df.columns = ['Daytime', 'Nighttime']
    fin_df.loc[:, 'Month Names'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
          'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return fin_df

def make_fig_3(fig_df):
    '''
    This function takes a fig_3_fin() df and graphs it
    Parameters:
    fig_df: a fig_3_fin() df
    Returns: None
    '''
    plt.style.use('ggplot')
    fig = fig_df.plot(x = 'Month Names', title = '2022 LA Average Hourly Crime')
    plt.title('2022 LA Average Hourly Crime Reports', fontsize = 20)
    plt.ylabel('Crimes Per Hour', fontsize = 15)
    plt.xlabel('Month', fontsize = 15)
    plt.show()

def main():
    #fig 1
    
    df = pd.read_csv('Crime_Data_from_2022.csv', index_col = 0, infer_datetime_format =True)
    '''
    heatmap_df = make_heatmap_df(df)
    make_heatmap_fig(heatmap_df)
    '''
    #fig 2
    df.loc[:,'DATE OCC'] = pd.to_datetime(df.loc[:,'DATE OCC'])
    crimes_per_month = make_fig_2_df(df)
    make_fig_2(crimes_per_month)
    #fig 3
    sun_df = make_sun_df()
    plt_df = fig_3_full_df(df, sun_df)
    fig_3_crime_count(plt_df, df, sun_df)
    crimes_per_hr(plt_df)
    fig_df = fig_3_fin(plt_df)
    make_fig_3(fig_df)


if __name__ == "__main__":
    main()