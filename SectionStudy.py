
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os
import numpy as np

ogdf = pd.DataFrame()
ogdir = 'C:\\Users\\chris.knowles\\OneDrive - Steel Dynamics Inc\Desktop\\Product Portfolio\\JDS JEDI Data Sharing\\Sections\\Sectiondata'
filelist = os.listdir(ogdir)
for file in filelist:
    fullpath = ogdir + '\\' + file
    curdf = pd.read_csv(fullpath)
    curdf['Plant'] = file
    if len(ogdf) == 0:
        ogdf = curdf
    else:
        ogdf = pd.concat([ogdf, curdf])



yearlist = []
for datedrawn in ogdf['DateDrawn']:
    entries = str(datedrawn).split('/')
    #print(entries)
    try:
        curyear = entries[2]
    except:
        curyear = 'NULL'
    if len(curyear) == 2:
        curyear = '20' + str(curyear)
    if len(curyear) > 4:
        curyear = curyear[:4]
    #print(curyear)
    yearlist.append(curyear)

ogdf['Year'] = yearlist
ogdf = ogdf.sort_values(by=['Year'])
years = ogdf['Year'].unique()
offices = ogdf['Plant'].unique()

print(years)

yearsdf = pd.DataFrame(columns=['Year', 'SectionCount'])
yearplantdf = pd.DataFrame(columns=['Year', 'Office', 'SectionCount'])
for year in years:
    curdf = ogdf.loc[ogdf['Year'] == year]
    totsections = len(curdf['Year'])
    addto = []
    addto.append(year)
    addto.append(totsections)
    yearsdf.loc[len(yearsdf)] = addto
    # now look at office level
    for office in offices:
        #print(office)
        #print(yearsdf['Plant'])
        curdfoffice = curdf.loc[curdf['Plant'] == office]
        totsections = len(curdfoffice['Year'])
        addnow = []
        addnow.append(year)
        addnow.append(office)
        addnow.append(totsections)
        yearplantdf.loc[len(yearplantdf)] = addnow

yearsdf = yearsdf.sort_values(by=['Year'], ignore_index=True)
yearsdf = yearsdf.loc[yearsdf['Year'] != 'NULL']
yearplantdf = yearplantdf.sort_values(by=['Year'], ignore_index=True)
yearplantdf = yearplantdf.loc[yearplantdf['Year'] != 'NULL']
# setting up our grid for different plots
# setting up our grid for different plots
fig, axis = plt.subplots(3)
plt.subplots_adjust(hspace=0.5)

#platform level total sections cut
row = 0
x = np.arange(len(yearsdf['SectionCount']))
axis[row].plot(x, yearsdf['SectionCount'])
axis[row].set_xticks(x, labels=yearsdf['Year'])
axis[row].set_title(label='Sections Cut Platform Level')

# office level total sections cut
row = 1
for office in offices:
    curdf = yearplantdf.loc[yearplantdf['Office'] == office]
    officeadj = office[:-4]
    axis[row].plot(x, curdf['SectionCount'], label=officeadj)

axis[row].set_xticks(x, labels=yearsdf['Year'])
axis[row].set_title(label='Sections Cut Office Level')
axis[row].legend(loc='upper left')
#platform level total sections by category
# FIRST BUILD A GOOD DF TO PLOT
row = 2
yearlist = ogdf['Year'].unique()
plotlabeldf = pd.DataFrame(columns=['Year', 'Category', 'SectionCount'])
labellist = ogdf['Category'].unique()
for year in yearlist:
    curdf = ogdf.loc[ogdf['Year'] == year]
    for label in labellist:
        labeldf = curdf.loc[curdf['Category'] == label]
        labelsum = len(labeldf)
        quickadd = []
        quickadd.append(year)
        quickadd.append(label)
        quickadd.append(labelsum)
        plotlabeldf.loc[len(plotlabeldf)] = quickadd
#print(plotlabeldf)
plotlabeldf = plotlabeldf.sort_values(by=['Category','Year'], ignore_index=True)
plotlabeldf = plotlabeldf.loc[plotlabeldf['Year'] != 'NULL']
#NOW PLOT THE DF
labelslist = plotlabeldf['Category'].unique()

for label in labelslist:
    try:
        labeldf = plotlabeldf.loc[plotlabeldf['Category'] == label]
        #print(label)
        #print(labeldf)
        axis[row].plot(x, labeldf['SectionCount'], label=label)
    except:
        print(label)
axis[row].set_xticks(x, labels=yearsdf['Year'])
axis[row].set_title(label='Sections by Label')
axis[row].legend(loc='upper left')



plt.show()

outputfile = 'C:\\Users\\chris.knowles\\OneDrive - Steel Dynamics Inc\Desktop\\Product Portfolio\\JDS JEDI Data Sharing\\Sections\YearlyResults\\platformLABELS.xlsx'

with pd.ExcelWriter(outputfile) as writer:
    for year in years:
        outputdf = pd.DataFrame(columns = ['Label', 'Count', 'Percentage','Year'])
        yeardf = ogdf.loc[ogdf['Year'] == year]
        sectiontypes = yeardf.Label.unique()
        for label in sectiontypes:
            todf = []
            curdf = yeardf.loc[yeardf.Label == label]
            count = len(curdf)
            todf.append(label)
            todf.append(count)
            todf.append(0)
            todf.append(year)
            outputdf.loc[len(outputdf)] = todf
        outputdf['Percentage'] = round((outputdf['Count'] / outputdf['Count'].sum()) * 100,2)
        outputdf = outputdf.sort_values(by='Percentage', ascending=False)
        outputdf.to_excel(writer, sheet_name=year + '-labels',index=False)

        catdf = pd.DataFrame(columns = ['Label', 'Count', 'Percentage','Year'])
        cattypes = yeardf.Category.unique()
        for category in cattypes:
            todf = []
            curdf = yeardf.loc[yeardf.Category == category]
            count = len(curdf)
            todf.append(category)
            todf.append(count)
            todf.append(0)
            todf.append(year)
            catdf.loc[len(catdf)] = todf
        catdf['Percentage'] = round((catdf['Count'] / catdf['Count'].sum()) * 100,2)
        catdf = catdf.sort_values(by=['Percentage'], ascending=False)            
    #yearlyresultsloc = 'C:\\Users\\chris.knowles\\OneDrive - Steel Dynamics Inc\Desktop\\Product Portfolio\\JDS JEDI Data Sharing\\Sections\YearlyResults\\'
        catdf.to_excel(writer, sheet_name=year + '-categories',index=False)

    platformdf = pd.DataFrame(columns = ['Label', 'Count'])
    alllabels = outputdf.Label.unique()

    for label in alllabels:
        addto = []
        curdf = ogdf.loc[ogdf['Label'] == label]
        curcount = len(curdf)
        addto.append(label)
        addto.append(curcount)
        platformdf.loc[len(platformdf)] = addto
    platformcat = pd.DataFrame(columns = ['Label', 'Count'])
    catlist = ogdf['Category'].unique()
    for cat in catlist:
        addto = []
        curdf = ogdf.loc[ogdf['Category'] == cat]
        totalit = len(curdf)
        addto.append(cat)
        addto.append(totalit)
        platformcat.loc[len(platformcat)] = addto

    platformdf['Percentage'] = round((platformdf['Count'] / platformdf['Count'].sum()) * 100,1)
    platformdf = platformdf.sort_values(by=['Percentage'], ascending=False)
    platformdf.to_excel(writer, sheet_name='ALL',index=False)  

    platformcat['Percentage'] = round((platformcat['Count'] / platformcat['Count'].sum()) * 100,1)
    platformcat = platformcat.sort_values(by=['Percentage'], ascending=False)
    platformcat.to_excel(writer, sheet_name='ALL-Categories',index=False)  
#print(outputdf)