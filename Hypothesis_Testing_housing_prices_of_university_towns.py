

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}





def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. 
    The following cleaning needs to be done:
    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.'''
    with open('university_towns.txt') as file:
        emp_list = []
        for line in file:
            emp_list.append(line[:-1])
    stateandtown = []
    for line in emp_list:
        if line[-6:] == '[edit]':
            state = line[:-6]
        elif '(' in line:
            town = line[:line.index('(')-1]
            stateandtown.append([state,town])     
        else:
            town = line
            stateandtown.append([state,town])
    uni_towns = pd.DataFrame(stateandtown,columns = ['State','RegionName'])
    return uni_towns





def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    rec = pd.read_excel('gdplev.xls')
    rec = rec[219:] #2000 onwards
    emp_lis = []
    for i in range(2, len(rec['Unnamed: 6'])+1):
        emp_lis.append(*rec['Unnamed: 6'][i-1:i].astype(float).tolist())
    emp_lis = pd.DataFrame(emp_lis)
    for j in range(1, len(emp_lis)+1):
        if (emp_lis[0][j]) < emp_lis[0][j-1] :
            if (emp_lis[0][j-1]) < emp_lis[0][j-2] :
                rec_GDP = list((emp_lis[0][j],emp_lis[0][j-1], emp_lis[0][j-2]))
                break
    rec_start = rec['Unnamed: 4'][rec[rec['Unnamed: 6'] == rec_GDP[1]].index.values[0]]
    return rec_start






def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    rec = pd.read_excel('gdplev.xls')
    rec = rec[219:] 
    emp_lis = []
    for i in range(2, len(rec['Unnamed: 6'])+1):
            emp_lis.append(*rec['Unnamed: 6'][i-1:i].astype(float).tolist())
    emp_lis = pd.DataFrame(emp_lis[::-1])
    for j in range(2, len(emp_lis)+1):
            if (emp_lis[0][j]) > emp_lis[0][j-1] :
                if (emp_lis[0][j-1]) > emp_lis[0][j-2] :
                    rec_GDP = list((emp_lis[0][j],emp_lis[0][j-1], emp_lis[0][j-2]))
                    break
    rec_end = rec['Unnamed: 4'][rec[rec['Unnamed: 6'] == rec_GDP[2]].index.values[0] +2]
    return rec_end






def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    rec = pd.read_excel('gdplev.xls')
    rec = rec[251:].reset_index()
    start = rec[rec['Unnamed: 4'] == '2008q3'].index.values[0]
    end = rec[rec['Unnamed: 4'] == '2010q1'].index.values[0]
    rec = rec[start:end]
    botval_in = rec[rec['Unnamed: 6'] == rec['Unnamed: 6'].min()].index[0]
    rec_bot = rec['Unnamed: 4'][botval_in]
    return rec_bot





def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    housing = pd.read_csv('City_Zhvi_AllHomes.csv', header = None)
    housing.drop(housing.columns[[1]])
    housing = housing.drop(housing.columns[np.arange(51).tolist()], axis = 1)
    housing.columns = housing.iloc[0]
    housing = housing[1:]
    housing.head()
    new_col = []
    for i in range(len(housing.columns)):
              new_col.append(housing.columns[i].replace('-01', 'q1').replace('-02', 'q1').replace('-03', 'q1').replace('-04', 'q2')
             .replace('-05', 'q2').replace('-06', 'q2').replace('-07', 'q3').replace('-08', 'q3').replace('-09', 'q3')
             .replace('-10', 'q4').replace('-11', 'q4').replace('-12', 'q4'))
    housing.columns = new_col

    housing = housing.astype(float)
    housing = housing.groupby(housing.columns, axis = 1).mean()

    dummy = pd.read_csv('City_Zhvi_AllHomes.csv', header = None)
    dummy.columns = dummy.iloc[0]
    dummy = dummy[1:]
    state_lis = dummy['State'].tolist()
    emp = []
    for i in state_lis:
        emp.append(str(states[i]))
    emp = pd.DataFrame(emp)
    emp = emp.set_index(np.arange(1,10731))

    housing['States'] = emp
    housing['RegionName'] = dummy['RegionName']
    housing.set_index(['States', 'RegionName'], inplace = True)
    return housing


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    data = convert_housing_data_to_quarters().copy()
    data = data.loc[:,'2008q3':'2009q2']
    data = data.reset_index()
    def price_ratio(row):
        return (row['2008q3'] - row['2009q2'])/row['2008q3']
    
    data['up&down'] = data.apply(price_ratio,axis=1)
    #uni data 
    
    uni_town = get_list_of_university_towns()['RegionName']
    uni_town = set(uni_town)

    def is_uni_town(row):
        #check if the town is a university towns or not.
        if row['RegionName'] in uni_town:
            return 1
        else:
            return 0
    data['is_uni'] = data.apply(is_uni_town,axis=1)
    
    
    not_uni = data[data['is_uni']==0].loc[:,'up&down'].dropna()
    is_uni  = data[data['is_uni']==1].loc[:,'up&down'].dropna()
    def better():
        if not_uni.mean() < is_uni.mean():
            return 'non-university town'
        else:
            return 'university town'
    p_val = list(ttest_ind(not_uni, is_uni))[1]
    result = (True,p_val,better())
    return result


