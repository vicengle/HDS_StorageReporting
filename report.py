#!/usr/bin/python
#
#
import sqlite3
import operator
import time,sys
from shutil import copyfile
from HDS_ReportingModule import Files
from HDS_ReportingModule import SQLTools
from HDS_ReportingModule import ReportGen
from HDS_ReportingModule import HTML5
from HDS_ReportingModule import DateString

# Use meter to show usage

customer = raw_input('Enter Customer Name: ')

t = DateString()

conn = sqlite3.connect('HDS_Report.sqlite')
cur = conn.cursor()

rpt = ReportGen()
rpt.GetArrayList(cur) 


www = HTML5()
www.style_sheet()

f = Files()



htmlfile = 'Report/Report.html'
htmllist = list()
html = www.start_html('Storage Report','left')
htmllist.append(html)

content = '<table align=center><tr><td><img src="logo_datalink.png">'
content += '</td><td>Datalink Storage Report (HDS)<br>for ' + customer + '<br>Report Date: ' + t.today + '</td></tr></table>'
htmllist.append(www.header(content))

links = list()
content = '<div class="nav_content">\n'

for array in rpt.ArrayList.keys():
  links.append(['<a href="#' + rpt.Array2Name[array] + '">' + rpt.Array2Name[array] + '</a>'])

content += www.start_table('left',0,"Navigation")
for l in sorted(links, reverse=True):
  content += www.tr_list(l)
content += www.end_table  
content += '</div>\n' 



htmllist.append(www.nav(content))


htmllist.append('<div id="section">\n')
htmllist.append('<div id="section_content">\n')


# sorting the SN to Name dict() by value to display in sorted order...
sorted_arrays = sorted(rpt.Array2Name.items(), key=operator.itemgetter(1), reverse=True)


for sorted_array in sorted_arrays:
  array = sorted_array[0]
  htmllist.append('<p class="small">\n')

  htmllist.append('<a name="' + rpt.Array2Name[array] + '">' + rpt.Array2Name[array] + '</a><br>\n')
  htmllist.append('<a href="CSV/' + rpt.Array2Name[array] + '.csv">( Open CSV File )</a><br>') 
  htmllist.append('</p>\n')
  htmllist.append(www.start_table('left',1))
  htmllist.append(www.th_list(rpt.ArrayColumnHeader.split(',')))
  htmllist.append(www.tr_list(rpt.ArrayList[array]))
  htmllist.append(www.end_table)
  htmllist.append('<p class="big">' + rpt.Array2Name[array] + ' DP Pools </p>')
  

  # Define CSV file and list for this array
  csvfile = 'Report/CSV/' + rpt.Array2Name[array] + '.csv'
  csvlist = list()
  
  # Go ahead and collect pool and lun data for the report
  rpt.GetPoolList(cur,array) 
  rpt.GetLunList(cur,array) 
  
  # 
  csvlist.append( rpt.Array2Name[array])
  csvlist.append( rpt.ArrayColumnHeader)
  csvlist.append( rpt.ArrayData[array])
  csvlist.append( "\n")
  
  csvlist.append( rpt.PoolColumnHeader)


  htmllist.append(www.start_table('left',1))
  htmllist.append(www.th_list(rpt.PoolColumnHeader.split(',')))
  for pool in rpt.PoolList:
    pool_csv =  ",".join(pool)
    usage = pool[4]
    subscription = pool[7]
    pool[4] = '<meter min="0"  max="100"  value="' + usage + '">' + usage + '</meter> ' + usage + '%' 
    pool[7] = '<meter min="0"  max="100"  value="' + subscription + '">' + subscription + '</meter> ' + subscription + '%' 
    htmllist.append(www.tr_list(pool))
    csvlist.append( pool_csv)
  csvlist.append( "\n")
  htmllist.append(www.end_table)
  htmllist.append('<p class="big">' + rpt.Array2Name[array] + ' LUNs </p>')


  htmllist.append(www.start_table('left',1))
  htmllist.append(www.th_list(rpt.LunColumnHeader.split(',')))
  csvlist.append( rpt.LunColumnHeader)
  for lun in rpt.LunList:
    lun_csv =  ",".join(lun)
    htmllist.append(www.tr_list(lun))
    csvlist.append( lun_csv  )  
  csvlist.append( "\n")
  htmllist.append(www.end_table)
  htmllist.append('<p class="big">\n_______________________________________________________</p>')
  f.write_file(csvfile,csvlist)

htmllist.append('<div id="section">\n')
htmllist.append('<div id="section">\n')
html = www.end_html
htmllist.append(html)

f.write_file(htmlfile,htmllist)
sys.exit()



