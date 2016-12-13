# Uptime_monitor
##### Python script to monitor status of a website and alert if down using email.

It uses http requests at an interval every 60 seconds to each site in the list. The request timeout interval for each is set to 60 seconds. Both the intervals can be edited as per needed.

Alert scenarios -

* In case if any site responds with response code other than HTTP-200, or an error: Alert email is sent to hard coded list of email-addresses.

* Alert is sent once the site is back up after it was down.

