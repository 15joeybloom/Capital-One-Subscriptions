import csv
import itertools
import operator
from collections import defaultdict
from datetime import date

yearly_rev = defaultdict(itertools.repeat(0).__next__)
subs = defaultdict(list)

with open('subscription_report.csv','r') as myfile:
    myfile.readline() #skip column headers
    myreader = csv.reader(myfile)
    for row in myreader:
        subID = int(row[1])
        amt = int(row[2])
        d = date(int(row[3][6:]),int(row[3][:2]),int(row[3][3:5]))

        subs[subID].append(d)
        yearly_rev[d.year] += amt

with open('subscriptions.txt','w') as myfile:
    myfile.write('SubID SubType  Duration\n')
    for subID, dates in subs.items():
        sub_type = ''
        duration = ''
        
        if len(dates) == 1:
            sub_type = ' one-off'
            duration = '{0}/{1}/{2}'.format(dates[0].month,dates[0].day,dates[0].year)
        elif dates[0].month == dates[1].month and dates[0].day == dates[1].day:
            sub_type = '  yearly'
            duration = str(len(dates)) + ' years'
        elif dates[0].day == dates[1].day:
            sub_type = ' monthly'
            months1 = dates[0].year*12+dates[0].month
            months2 = dates[-1].year*12+dates[-1].month
            duration = str(len(dates)) + ' months'
        else:
            sub_type = '   daily'
            duration = str(len(dates)) + ' days'
        myfile.write(str(subID).rjust(5) + sub_type + duration.rjust(11)+'\n')

yearly_rev[1965] = yearly_rev[1966] #this way, the first difference will end up being 0, because it's just the baseline
difs = dict()
pctdifs = dict()
for year in range(1966,2015):
    dif = yearly_rev[year]-yearly_rev[year-1]
    pctdif = dif/float(yearly_rev[year-1])*100
    difs[year] = dif
    pctdifs[year] = pctdif

sorteddifs = sorted(difs.items(), key=operator.itemgetter(1))
sortedpctdifs = sorted(pctdifs.items(), key=operator.itemgetter(1))

with open('revenue.txt','w') as myfile:
    myfile.write('     Revenue  Year\n')
    for year in range(1966,2015):
        rev = '${:,d}'.format(yearly_rev[year])
        myfile.write(rev.rjust(12) + '  ' + str(year) + '\n')

    myfile.write('\n');
    myfile.write('The highest growth of revenue was ${0:,d} in {1}.\n'.format(sorteddifs[-1][1],sorteddifs[-1][0]))
    myfile.write('The highest percent growth of revenue was {0:.2f}% in {1}.\n'.format(sortedpctdifs[-1][1],sortedpctdifs[-1][0]))
    myfile.write('The highest loss of revenue was ${0:,d} in {1}.\n'.format(-sorteddifs[0][1],sorteddifs[0][0]))
    myfile.write('The highest percent loss of revenue was {0:.2f}% in {1}.\n'.format(-sortedpctdifs[0][1],sortedpctdifs[0][0]))
