from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
import csv, unicodedata
from datetime import datetime, timedelta

try:
   config = open( 'trackingtimes.cfg', 'rb' )
   params = config.readlines(  )
   inputfile = params[ 0 ][ params[ 0 ].find( '=' ) +2: ].rstrip( '\r\n' )
   outputfile= params[ 1 ][ params[ 1 ].find( '=' ) +2: ].rstrip( '\r\n' )
except:
   cfg = open( 'trackingtimes.cfg', 'wb' )
   cfg.write( 'Input Filename  = 3rd Timestamp Tracking.csv\r\nOutput Filename = tracking_output.csv\r\n# Note that this config file, and the indicated input file must be in the same directory as the EXE.' )
   cfg.close(  )
   inputfile = '3rd Timestamp Tracking.csv'
   outputfile= 'tracking_output.csv'
   

def scrape_web( array ):
   with closing(Firefox()) as browser:
      for order in array:
         browser.get('https://www.fedex.com/fedextrack/index.html?tracknumbers='+order[4]+'&cntry_code=us')
         WebDriverWait(browser, timeout=10).until(
            lambda x: x.find_element_by_id('destinationDateTime'))
         deliverydate = unicodedata.normalize( 'NFKD', browser.find_element_by_id('destinationDateTime').get_attribute('innerHTML') ).encode( 'ascii', 'ignore' )
         deliverydate = deliverydate.replace('Mon ','').replace('Tues ','').replace('Wed ','').replace('Thur ','').replace('Fri ','').replace('Sat ','').replace('Sun ','')
         print order[0]
         deliverydate = datetime.strptime( deliverydate, '%m/%d/%Y %I:%M %p' ).strftime( '%m/%d/%y %H:%M' )
         order.append( deliverydate )
   return array

def diff_hours( t1, t2 ):
   return (t1-t2).days*24 + (t1-t2).seconds/60/60

allrows = [  ]
header = [  ]

print 'Processing ticket data ...'

with open( inputfile, 'rb' ) as source:
   reader = csv.reader( source )
   for x in reader:
      if x[0][0] == 'A':
         allrows.append( [ x[0], x[4], x[1], x[5], x[3], x[2] ] )
         
   
print 'Scraping Fedex.com ...'

with open( outputfile, 'wb' ) as result:
   writer = csv.writer( result )
   header = [ 'SC Ticket #', 'Order #', 'Agent', 'Open Time', 'Tracking #', 'Onsite Timestamp', 'Fedex Delivery Date' ]
   writer.writerow( header )
   for x in scrape_web( allrows ):
#      a = datetime.strptime( x[ 2 ], '%m/%d/%y %H:%M' )
#      b = datetime.strptime( x[ 6 ], '%m/%d/%y %H:%M' )
#      x.append( diff_hours( a, b ) )
      writer.writerow( x )

print 'Finished!'



'''
Source:
http://stackoverflow.com/questions/8960288/get-page-generated-with-javascript-in-python
'''
