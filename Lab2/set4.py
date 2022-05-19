import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../resources/sales_data.csv')
print(df)
months = df["month_number"].values
profit_list = df['total_profit'].values
plt.figure()
plt.plot(months, profit_list, label=' Month - wise Profit data of last year')
plt.xlabel('Month number')
plt.ylabel('Profit [ $ ]')
plt.xticks(months)
plt.title('Company profit per month')
plt.yticks([1e5, 2e5, 3e5, 4e5, 5e5])
plt.show()
# es 1 e 2
'''
sales = df["total_profit"]
plt.plot(months, sales, color="r", marker='o', markerfacecolor="k", linestyle='-', linewidth="3")
plt.xlabel("months")
plt.ylabel("sales")
'''
#es 3
'''
plt.plot(m, df["facecream"], label="facecream")
plt.plot(m, df["facewash"], label="facewash")
plt.plot(m, df["moisturizer"], label="moisturizer")
plt.plot(m, df["bathingsoap"], label="bathingsoap")
plt.plot(m, df["shampoo"], label="shampoo")
plt.plot(m, df["toothpaste"], label="toothpaste")
'''
# es 4
'''
plt.scatter(m, df["toothpaste"])
'''
#es 5
# plt.bar(m, df["bathingsoap"])
# plt.savefig("../results/Soap_plot.png")
#es 6 e 7
"""
fig, ax = plt.subplots(2)
ax[0].hist(df["total_profit"])
ax[0].grid(axis="y", color="r")
ax[1].plot(m, df["bathingsoap"])
ax[1].grid(axis="y", color="r")
# plt.xticks(np.arange(1, 13, step=1))

plt.show()
"""