import pandas as pd

details = {
    'Name': ['Sravan', 'Sai', 'Mohan', 'Ishitha'],
    'College': ['Vignan', 'Vignan', 'Vignan', 'Vignan'],
    'Physics': [99, 76, 71, 93],
    'Chemistry': [97, 67, 65, 89],
    'Data Science': [93, 65, 65, 85]
}

# converting to dataframe using DataFrame()
df = pd.DataFrame(details)
print("{}\n".format(df))

details1 = {
    'Name': ['Harsha', 'Saiteja', 'abhilash', 'harini'],
    'College': ['vvit', 'vvit', 'vvit', 'vvit'],
    'Physics': [69, 76, 51, 43],
    'Chemistry': [67, 67, 55, 89],
    'Maths': [73, 65, 61, 85]
}

# create dataframe
df1 = pd.DataFrame(details1)
print("{}\n".format(df1))

df2 = pd.concat([df, df1], axis=0, ignore_index=True)
print("{}\n".format(df2))

df2 = pd.concat([df, df1], axis=0, ignore_index=False)
print("{}\n".format(df2))