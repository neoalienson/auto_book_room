It uses Selenium and Firefox with Python to book room automatically from
Microsoft Outlook 2000 (OWA)

run:
python autobook.py [config file]

config file's content:
{ 
  'url':'base url of the OWA, e.g., http://sample/'
  'username':'someone', 
  'password':'plain-text password',
  'room':"room name" }
