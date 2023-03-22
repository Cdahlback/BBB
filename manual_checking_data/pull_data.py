import pandas as pd

# data = pd.read_csv('2000_random_selection.csv')
# data = data.loc[data['FoundVia'].notna()]
#
# search = pd.read_csv('randomly_picked.csv')
#
# full_2000 = pd.concat([data, search])
# full_2000.to_csv('new_2000_random_selection.csv')

data = pd.read_csv('new_2000_random_selection.csv')
dylan = data[0:400]
dylan.to_csv("dylan_manual_check.csv")

collin = data[400:800]
collin.to_csv("collin_manual_check.csv")

jackson = data[800:1200]
jackson.to_csv("jackson_manual_check.csv")

justin = data[1200:1600]
justin.to_csv("justin_manual_check.csv")

biruk = data[1600:]
biruk.to_csv("biruk_manual_check.csv")

