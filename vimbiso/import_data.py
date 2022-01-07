import sys
import pandas as pd
from models import *
# Give the location of the file
loc = sys.argv[1]
print(loc)

df = pd.read_excel (f'{loc}')
print(df)
for i in df.index:
    email = df['Email'][i]
    company = df['company'][i]
    country = df['country'][i]
    city = df['city'][i]
    block = df['block'][i]
    contact = df['contact'][i]
    category = df['category'][i]
    try:
        print(email.strip(),company.strip())
    except:
        pass