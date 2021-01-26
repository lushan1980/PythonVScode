import pyodbc
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import random


driver = '{ODBC Driver 17 for SQL Server}'
server = 'logecaldatabase.database.windows.net'
database = 'CoronaVirus'
username = 'logecal'
password = 'Lushan2020$'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# conn = pymssql.connect(server='logecaldatabase.database.windows.net', user='logecal@server', password='Lushan2020$', database='CoronaVirus')

st.title('Surgery Time table and plots')

SQL_Query = pd.read_sql_query('''exec [dbo].[SurgeryTime]''', conn)

df = pd.DataFrame(SQL_Query)

Control = random.normal(loc=150, scale=40, size=69)
Device = random.normal(loc=70, scale=20, size=71)

df.loc[df.Randomization == 'Control', 'SurgeryTime'] = Control
df.loc[df.Randomization == 'Device', 'SurgeryTime'] = Device

st.markdown("""
### Surgery Time Table
""")

st.write(df)
# st.table(df)
# conn.close()

st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("""
### Surgery Time by Group
""")
sns.boxplot(x="Randomization", y="SurgeryTime", palette="husl", data=df)
st.pyplot()

# g = sns.catplot(x="MonthProc", y="SurgeryTime", hue="Randomization", kind="bar", palette="husl", ci=95, data=df)
# g.set_xticklabels(rotation=45)
# st.pyplot()
st.write("""
### Surgery Time by Month
""")
l = sns.pointplot(x="MonthProc", y="SurgeryTime", hue="Randomization", err_style="bars", ci=95, data=df, dodge=0.4, join=True)
plt.setp(l.get_xticklabels(), rotation=45)
st.pyplot()

# st.write(pyodbc.drivers())