import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def read_data(path):
    attack = pd.read_csv(path, encoding= 'unicode_escape')
    attack.columns = attack.columns.str.rstrip()
    pd.set_option("display.max_rows", None)
    return attack

def clean_data(attack):
    
    #initial cleaning of the CSV, getting rid of unwanted columns or columns with NaN values
    unwanted_data = ['pdf','href','href formula', 'original order','Case Number.1','Case Number.2', 'Unnamed: 22', 'Unnamed: 23', 'Year', 'Type', 'Date', 'Investigator or Source', 'Injury', 'Name']
    attack = attack.drop(columns = unwanted_data)
    attack = attack.dropna()
    shark_counts = attack["Species"].value_counts()
    valid_species = ['White shark', 'Tiger shark', 'Bull shark']
    attack = attack[attack['Species'].isin(valid_species)]
    attack.set_index('Case Number', inplace=True)
    case_values = attack.index.value_counts()
    attack = attack.loc[~attack.index.str.startswith('ND')]
    
    #reseting time values to be nice and clean
    time_values = attack['Time'].value_counts()
    attack['Time'] = attack['Time'].replace({'Afternoon':'12h00', 'Morning':'09h00', 'Early afternoon':'14h00', '08h00 / 09h30 ': '08h30', '>06h45': '06h45', 'Shortly before 12h00': '12h00', 'Late afternoon': '16h00', '"Just before 11h00"':'11h00', 'Early morning ': '07h00'})
    attack['Time'] = attack['Time'].str.replace('h', ':')
    country_values = attack['Country'].value_counts()
    northern_countries = ['USA', 'CROATIA', 'CUBA', 'MEXICO', 'IRAQ', 'BAHAMAS', 'MALDIVES', 'COSTA RICA', 'ITALY']
    attack['Hemisphere'] = 'Southern'
    attack.loc[attack['Country'].isin(northern_countries), 'Hemisphere'] = 'Northern'
    return attack

def create_hem_attack(attack):
    hem_attack = attack[['Country', 'Hemisphere', 'Fatal (Y/N)']]
    return hem_attack

def create_year_attack(attack):
    attack['year'] = attack.index.str[:4].astype(int)
    year_attack = attack[['year', 'Fatal (Y/N)', 'Country']]
    return year_attack

def create_us_attacks(attack):
    us_attacks = attack[attack['Country'] == 'USA'][['Area', 'Fatal (Y/N)']]
    west_coast = ['California', 'Oregon', 'Hawaii']
    us_attacks['West/East'] = 'East'
    us_attacks.loc[us_attacks['Area'].isin(west_coast), 'West/East'] = 'West'
    return us_attacks


def export_csv(attack, hem_attack, year_attack, us_attacks):
    attack.to_csv("data/attack_clean.csv", index=True)
    year_attack.to_csv("data/attack_by_year.csv", index=True)
    us_attacks.to_csv("data/us_attacks.csv", index=True)


"""now for the functions to create the visualizations"""
def read_attack_year():
    attack_year = pd.read_csv('data/attack_by_year.csv', encoding= 'unicode_escape')
    attack_year.columns = attack_year.columns.str.rstrip()
    return attack_year

def read_attack_hemisphere():
    attack_hemisphere = pd.read_csv('data/attack_by_hemisphere.csv', encoding= 'unicode_escape')
    return attack_hemisphere

def read_us_attacks():
    us_attacks = pd.read_csv('data/us_attacks.csv', encoding = 'unicode_escape')
    return us_attacks


def prepare_data(attack_year, attack_hemisphere, us_attacks):
    # Convert year column to numeric for plotting
    attack_year['year'] = pd.to_numeric(attack_year['year'])
    
    # New dataframe that looks at attacks prior to 1980
    df_before_1980 = attack_year[(attack_year["year"] < 1980) & (attack_year["Fatal (Y/N)"])]
    
    return df_before_1980

def set_style():
    sns.set_style("darkgrid")

def prepare_attack_year(attack_year):
    attack_year['year'] = pd.to_numeric(attack_year['year'])
    return attack_year

def plot_attack_year_violin(attack_year):
    df_before_1980 = attack_year[(attack_year["year"] < 1980) & (attack_year["Fatal (Y/N)"])]
    attack_year_plot = sns.violinplot(x='Fatal (Y/N)', y='year', data=df_before_1980)
    plt.title("Shark attack fatalities prior to 2000")
    attack_year_plot.figure.savefig("data/year_plot.png")
    return attack_year_plot

def plot_attack_year_swarm(attack_year):
    df_before_1980 = attack_year[(attack_year["year"] < 1980) & (attack_year["Fatal (Y/N)"])]
    attack_year_swarm = sns.swarmplot(x='Fatal (Y/N)', y='year', data=df_before_1980)
    plt.xlabel("Fatal (Y/N)")
    plt.ylabel("Year")
    plt.title("Shark attack fatalities by year")
    attack_year_swarm.figure.savefig("data/year_swarm.png")
    return attack_year_swarm

def plot_attack_hemisphere_heatmap(attack_hemisphere):
    contingency_table = pd.crosstab(attack_hemisphere['Fatal (Y/N)'], attack_hemisphere['Hemisphere'])
    attack_hemisphere_table = sns.heatmap(contingency_table, annot=True, cmap='Reds')
    attack_hemisphere_table.figure.savefig("data/hemisphere_heatmap.png")
    return attack_hemisphere_table

def plot_attack_hemisphere_bar(attack_hemisphere):
    contingency_table = pd.crosstab(attack_hemisphere['Fatal (Y/N)'], attack_hemisphere['Hemisphere'])
    attack_hemisphere_bar = contingency_table.plot(kind="bar", stacked=True)
    plt.xlabel("Fatal (Y/N)")
    plt.ylabel("Attack Count")
    plt.title

def plot_us_attacktable(us_attacks):
    #creating a contingency table to look at the ration of fatalities:location in the USA
    us_attack_table = pd.crosstab(us_attacks['Fatal (Y/N)'], us_attacks['West/East'])

    #visualizing the contingency table
    us_attack_heatmap = sns.heatmap(us_attack_table, annot=True, cmap='inferno')

    #saving file as pic to use in analysis
    us_attack_heatmap.figure.savefig("data/us_attack_heatmap.png")

    return us_attack_heatmap

def plot_us_attack_bar(us_attacks):
    
    #visualizing the us attacks table with a stacked bar graph and saving as pic
    us_attack_table = pd.crosstab(us_attacks['Fatal (Y/N)'], us_attacks['West/East'])
    us_attack_bar = us_attack_table.plot(kind="bar", stacked=True)
    plt.xlabel("Fatal (Y/N)")
    plt.ylabel("Attack Count")
    plt.title("Fatalities per Coast")
    us_attack_bar.figure.savefig("data/us_attack_bar.png")
    return plot_us_attack_bar

def dangerous_countries(attack_hemisphere):
    #Looking at the worst countries for shark attacks
    dangerous_countries = attack_hemisphere['Country'].value_counts().head(5).index
    df_dangerous_countries = attack_hemisphere[attack_hemisphere['Country'].isin(dangerous_countries)]

    #plotting the most dangerous countries to swim in
    dangrous_waters = sns.countplot(x='Country', hue='Fatal (Y/N)', data=df_dangerous_countries)
    plt.xticks(rotation=90)

    #saving as pic
    dangrous_waters.figure.savefig("data/dangerous_waters.png",  dpi=300, bbox_inches='tight')
