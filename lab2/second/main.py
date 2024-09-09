import pandas as pd

df = pd.DataFrame(range(101))

print(df[::15].values[:, 0])
print('done')
