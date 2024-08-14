import csv, sqlite3
import pandas

con = sqlite3.connect("ChicagoPublicRecords.db")
cur = con.cursor()

%load_ext sql
%sql sqlite:///ChicagoPublicRecords.db


## Store the dataset in a table

df = pandas.read_csv("Data/ChicagoCensusData.csv")
df.to_sql("CENSUS_DATA", con, if_exists='replace', index=False,method="multi")

df = pandas.read_csv("Data/ChicagoCrimeData.csv")
df.to_sql("CHICAGO_CRIME_DATA", con, if_exists='replace', index=False, method="multi")

df = pandas.read_csv("Data/ChicagoPublicSchools.csv")
df.to_sql("CHICAGO_PUBLIC_SCHOOLS_DATA", con, if_exists='replace', index=False, method="multi")

##Query the database system catalog to retrieve table metadata

%sql SELECT name FROM sqlite_master WHERE type='table

#Query to retrieve the number of columns in the SCHOOLS table

%sql SELECT count(name) FROM PRAGMA_TABLE_INFO('CHICAGO_PUBLIC_SCHOOLS_DATA');

