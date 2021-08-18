import pandas as pd

df = pd.read_excel('simplyhired.xlsx')

# salary - remove empty, remove text, split, avg
df.dropna(subset=['salary'], inplace=True)
df.reset_index(drop=True, inplace=True)
df['salary'] = df['salary'].apply(lambda x: str(x).replace('Estimated: ', '').replace(' a year', '').replace('$', '').replace(',', ''))
df['min_salary'] = df['salary'].apply(lambda x: x.split('-')[0])
df['max_salary'] = df['salary'].apply(lambda x: x.split('-')[1])
min_sal = pd.to_numeric(df['min_salary'])
max_sal = pd.to_numeric(df['max_salary'])
df['avg_salary'] = (min_sal+max_sal)/2


# remote work - if 'remote' in company column then 'Yes' else 'No'
df['remote_work'] = df['company'].apply(lambda x: 'Remote' if 'remote' in x.lower() else 'In the office')

# state - split by last comma, take two element after comma and space if exist if not then name don't have state
df['state'] = df['company'].str.rsplit(',', 1)
df['state'] = df['state'].apply(lambda x: x[1][1:3] if len(x) == 2 else 'blank')
df['state'] = df['state'].replace('In', 'blank')

# rating - take last 3 elements from company and check if 3 element from end belong to ratings
ratings = ['0', '1', '2', '3', '4', '5']
df['company'].str.strip()
df['rating'] = df['company'].apply(lambda x: x[-3:] if x[-3] in ratings else '-1')
df['rating'] = pd.to_numeric(df['rating'], downcast="float")

# company - split by last comma (to remove state), take first element (it is company name and city), remove 'remote'
# and '\xa0' from company name,
df['company_name'] = df['company'].apply(lambda x: x if ', Inc.' in x else x.rsplit(',', 1)[0])
df['company_name'] = df['company_name'].apply(lambda x: str(x).lower().replace('- remote',''))
df['company_name'] = df['company_name'].apply(lambda x: x[0:x.find('\xa0')] if '\xa0' in x else x)

df['name'] = df['company_name'].apply(lambda x: x.rsplit('-', 1)[0] if '-' in x else x)
df['city'] = df['company_name'].apply(lambda x: x.rsplit('-', 1)[1] if '-' in x else 'blank')
df['city'] = df['city'].apply(lambda x: x.rsplit(',', 1)[0])  # some city have also abbreviations after comma


df_out = df.drop(['Unnamed: 0', 'company', 'company_name', 'salary'], axis=1)
print(df_out.columns)
df_out.to_excel("data-cleaned-sh.xlsx")
