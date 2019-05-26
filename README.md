# CardCat

A simple webhook/app to be part of a zapier process to log credit-card
purchases and allow the user to categorize them.

## The process

I have a filter on my gmail account that tags emails from the bank that
alerts of purchases.  Zapier checks in on that account every five minutes
if it detects an email, it regexes the body text, then pushes an alert
to my phone and also to this webhook with the following info:

```json
{ 
    "token": "secure_token_to_allow_access",
    "card": "****1234",
    "dt": "02:30 pm EST",
    "amount": "$45.00",
    "vendor": "amazon.com/pmt/"
}
 

```

```python

from uuid import uuid4
from datetime import datetime

now = datetime.now()
dt = input_data["dt"]
dt = dt[:dt.find('m')+1].upper()
dttm = f"{now.strftime('%Y-%m-%d')} {dt}"
dttm = datetime.strptime(dttm, '%Y-%m-%d %H:%M %p')
token = uuid4().hex
output = [
    {
        'token': token, 
        'card': input_data["card"],
        'dt': dttm.isoformat(),
        'vendor': input_data["vendor"].strip(),
        'amount': input_data["amount"].replace('$','').strip()
        
    }
]


```