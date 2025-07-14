import pandas as pd
import uuid

try:
    master = pd.read_csv('data/clients_merged.csv')
except FileNotFoundError:
    master = pd.DataFrame(columns=['ClientIndex','ClientID','FirstName','LastName','Email','Phone','Source'])

# Loading data from different sources
web_df = pd.read_csv('data/clients_website.csv')
crm_df = pd.read_csv('data/clients_legacy.csv')
agent_ref_df = pd.read_csv('data/clients_agent.csv')

# Renaming columns 
web_df.rename(columns={'id':'ClientID','f_name':'FirstName','l_name':'LastName','email':'Email','phone':'Phone'}, inplace= True)
crm_df.rename(columns={'id':'ClientID','first_name':'FirstName','last_name':'LastName','phone':'Phone','email':'Email'}, inplace=True)
agent_ref_df.rename(columns={'id':'ClientID','firstname':'FirstName','lastname':'LastName','phone':'Phone','email':'Email'}, inplace=True)

# Adding Source detail
web_df['Source'] = 'Website'
crm_df['Source'] = 'CRM'
agent_ref_df['Source'] = 'Agent Reference'

# Merging data
new_data = pd.concat([
    web_df[['ClientID','FirstName','LastName','Email','Phone','Source']],
    crm_df[['ClientID','FirstName','LastName','Email','Phone','Source']],
    agent_ref_df[['ClientID','FirstName','LastName','Email','Phone','Source']]
])

# Removing duplicates
new_data = new_data.drop_duplicates(subset=['Email','Phone'])

if not master.empty:
    # Merging data into already existing merged dataset
    merged = pd.merge(new_data, master, on=['Email','Phone'], how='left', suffixes=('','_master'))
    merged['ClientIndex'] = merged['ClientIndex'].fillna('').apply(lambda x: x if x!='' else str(uuid.uuid4()))
    master = merged[['ClientIndex','ClientID','FirstName','LastName','Email','Phone','Source']]

else:
    # Creating merged dataset
    new_data['ClientIndex'] = [str(uuid.uuid4()) for _ in range(len(new_data))]
    master = new_data[['ClientIndex','ClientID','FirstName','LastName','Email','Phone','Source']]

# Saving merged dataset
master.to_csv('data/clients_merged.csv', index=False)