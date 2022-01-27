import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl

def calculate_passes(df, event, points):
    
    falcons = ['Banxx', 'JNo', 'Manson',
           'Margo','Molly','Emma',
           'Anika','Denise','Goda',
           'Grace','Lauren','Nicole',
           'Sophie','Taylor','Piorer',
           'Kate C','Kate T','Lyda']

    pears = ['Arjun','Ben','Garrett',
             'Kamal','Souma','Stephen',
             'Lukie','Button','Tian',
             'Roach','Craig','Gabe',
             'Niemer','PGL','Roy',
             'Landy','Ollie','Jake','Tom']
    
    df_clean = df.where(df.Receiver.isin(falcons+pears)).dropna(axis=0, how = 'all')
    falcon_passes = len(df_clean.where(df.Passer.isin(falcons)).dropna(axis = 0, how = 'all'))
    pear_passes = len(df.where(df_clean.Passer.isin(pears)).dropna(axis=0, how = 'all'))
    all_passes = falcon_passes+pear_passes
    
    # classify passes

    falcon_falcon = df.where(df_clean.Passer.isin(falcons) & df_clean.Receiver.isin(falcons)).dropna(axis =0, how = 'all')
    falcon_pear = df.where(df_clean.Passer.isin(falcons) & df_clean.Receiver.isin(pears)).dropna(axis =0, how = 'all')
    pear_pear = df.where(df_clean.Passer.isin(pears)& df_clean.Receiver.isin(pears)).dropna(axis =0, how = 'all')
    pear_falcon= df.where(df_clean.Passer.isin(pears) & df_clean.Receiver.isin(falcons)).dropna(axis =0, how = 'all')
    
    # sum passes by type

    ff_passes = len(falcon_falcon)
    fp_passes = len(falcon_pear)
    pp_passes = len(pear_pear)
    pf_passes = len(pear_falcon)
    
    fig1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2,figsize = (12,6))
    
    # plot
    ax1.bar(x=['falcon','pear'],
            height=[falcon_passes/all_passes*100,
                    pear_passes/all_passes*100],
           color =['blue','orange'],
           edgecolor = 'black',
           linewidth = 3,
           alpha = 0.3)
    tag = str(round(points)) + ' points'
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.set_xlabel('Type of Pass', fontsize =16, fontweight = 'bold', color = 'grey')
    ax1.set_ylabel('Percent of Passes (%)', fontsize =16, fontweight = 'bold', color = 'grey')
    ax1.set_ylim([0,100])
    ax1.set_title(event, fontweight = 'bold', fontsize = 18, color = 'grey', loc = 'left',pad = 10)
    fig1.suptitle('Distribution of Passes on Birdfruit 2021', fontweight = 'bold', fontsize=20)
    ax1.text(-0.25, 85 ,tag, fontsize = 14, fontweight='bold', color = 'grey')
#     ax1.tight_layout()

#     fig2 = plt.figure(figsize=(6,6))
    
    # plot
    labels = ['falcon-falcon','falcon-pear','pear-pear','pear-falcon']
    sizes = [ff_passes/all_passes*100, 
             fp_passes/all_passes*100, 
             pp_passes/all_passes*100,
             pf_passes/all_passes*100
            ]
    colors = ['limegreen', 'darkgreen', 'limegreen', 'darkgreen']
    patches, texts, pcts = ax2.pie(sizes, labels=labels, colors = colors, autopct='%1.1f%%',startangle=90, 
                                   wedgeprops = {'alpha':0.5, 'linewidth':3,'edgecolor':'white'}, 
                                   textprops = {'fontsize':12, 'fontweight': 'bold', 'color':'grey'})
    plt.setp(pcts, color='white', fontweight='bold')
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.set_title('Passer-Receiver Breakdown', fontweight='bold', fontsize = 18, color = 'darkgrey', loc= 'right', pad = 10) 
    
    fig1.tight_layout(pad=1.5)
    
def falcon_or_pear(df):
    falcons = ['Banxx', 'Jno', 'Manson','Mel',
               'Margo','Molly','Emma',
               'Anika','Denise','Goda',
               'Grace','Lauren','Nicole',
               'Sophie','Taylor','Piorer',
               'Kate C','Kate T','Lyda']
        
    for ind in df.index:
#         print(ind)
        line = df['line'][ind]
        check = sum([player in falcons for player in line])
        if check > 3:
            df.loc[ind, ('line_type')] = 'falcon'
        else:
            df.loc[ind, ('line_type')] = 'pear'
            
    return df

def who_handles(df):
    falcon_handlers = ['Banxx', 'Manson','Mel',
                       'Margo','Molly','Emma']
    falcon_cutters = ['Anika','Jno','Denise','Goda',
                      'Grace','Lauren','Nicole',
                      'Sophie','Taylor','Piorer',
                      'Kate C','Kate T','Lyda']
    for ind in df.index:
#         print(ind)
        line = df['line'][ind]
        check_handles = sum([player in falcon_handlers for player in line])
        if check_handles >= 2:
            df.loc[ind, ('handler_maj')] = 'falcon'
        else:
            df.loc[ind, ('handler_maj')] = 'pear'
            
        check_cuts = sum([player in falcon_cutters for player in line])
        if check_cuts > 2:
            df.loc[ind, ('cutter_maj')] = 'falcon'
        elif check_cuts < 2:
            df.loc[ind, ('cutter_maj')] = 'pear'
        else:
            df.loc[ind, ('cutter_maj')] = 'even'
            
    return df

def tally_points(df):
    count = 0
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    
    df.loc[:, 'Last Point Elapsed Seconds'] = df["Point Elapsed Seconds"].shift(periods=1)
    for ind in df.index:
        check = df['line_type'][ind]
        check_handles = df['handler_maj'][ind]
        if count1 == 0:
            this_point = 0
            last_point = 0
            count1=1
        else:
            this_point = int(df['Point Elapsed Seconds'][ind])
            last_point = int(df['Last Point Elapsed Seconds'][ind])
            
        if check == 'falcon' and this_point != last_point:
            count += 1
            df.loc[ind, ('falcon_points')] = count
        else:
            df.loc[ind, ('falcon_points')] = count
            
        if check == 'falcon' and check_handles == 'falcon' and this_point != last_point:
            count2 += 1
            df.loc[ind, ('ff_points')] = count2
        else:
            df.loc[ind, ('ff_points')] = count2
            
        if check == 'falcon' and check_handles == 'pear' and this_point != last_point:
            count3 += 1
            df.loc[ind, ('fp_points')] = count3
        else: 
            df.loc[ind, ('fp_points')] = count3
            
        if check == 'pear' and check_handles == 'pear' and this_point != last_point:
            count4 += 1
            df.loc[ind, ('pp_points')] = count4
        else:
            df.loc[ind, ('pp_points')] = count4
            
        if check == 'pear' and check_handles == 'falcon' and this_point != last_point:
            count5 += 1
            df.loc[ind, ('pf_points')] = count5
        else:
            df.loc[ind, ('pf_points')] = count5
            
    return df