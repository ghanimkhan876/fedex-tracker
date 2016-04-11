# fedex-tracker
A tool to automatically scrape fedex delivery information given a list of service tickets.

Uses Selenium to drive a Chrome browser automatically through the CSV of service tickets and their associated tracking numbers, returning a CSV as output containing the delivery dates and times.

Note that Fedex now has an API, which is almost certainly a better way to do this!
