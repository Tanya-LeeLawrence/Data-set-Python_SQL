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

# type in your query to retrieve all column names in the SCHOOLS table along with their datatypes and length
%sql SELECT name,type,length(type) FROM PRAGMA_TABLE_INFO('CHICAGO_PUBLIC_SCHOOLS_DATA');

%sql select count(*) from CHICAGO_PUBLIC_SCHOOLS_DATA where "Elementary, Middle, or High School"='ES'


%sql select MAX(Safety_Score) AS MAX_SAFETY_SCORE from CHICAGO_PUBLIC_SCHOOLS_DATA


%%sql select Name_of_School, Safety_Score from CHICAGO_PUBLIC_SCHOOLS_DATA where 
  Safety_Score= (select MAX(Safety_Score) from CHICAGO_PUBLIC_SCHOOLS_DATA)

%%sql select Name_of_School, Average_Student_Attendance from CHICAGO_PUBLIC_SCHOOLS_DATA 
    order by Average_Student_Attendance desc nulls last limit 10 

%%sql SELECT Name_of_School, Average_Student_Attendance  
     from CHICAGO_PUBLIC_SCHOOLS_DATA 
     order by Average_Student_Attendance 
     LIMIT 5

%%sql SELECT Name_of_School, REPLACE(Average_Student_Attendance, '%', '') 
     from CHICAGO_PUBLIC_SCHOOLS_DATA 
     order by Average_Student_Attendance 
     LIMIT 5

%%sql SELECT Name_of_School, Average_Student_Attendance  
     from CHICAGO_PUBLIC_SCHOOLS_DATA
     where CAST ( REPLACE(Average_Student_Attendance, '%', '') AS DOUBLE ) < 70 
     order by Average_Student_Attendance

%sql select Community_Area_Name, sum(College_Enrollment) AS TOTAL_ENROLLMENT \
   from CHICAGO_PUBLIC_SCHOOLS_DATA \
   group by Community_Area_Name

%sql select Community_Area_Name, sum(College_Enrollment) AS TOTAL_ENROLLMENT \
   from CHICAGO_PUBLIC_SCHOOLS_DATA \
   group by Community_Area_Name \
   order by TOTAL_ENROLLMENT asc \
   LIMIT 5 

%sql SELECT name_of_school, safety_score \
FROM CHICAGO_PUBLIC_SCHOOLS_DATA  where safety_score !='None' \
ORDER BY safety_score \
LIMIT 5

%%sql 
select hardship_index from CENSUS_DATA CD, CHICAGO_PUBLIC_SCHOOLS_DATA CPS 
where CD.community_area_number = CPS.community_area_number 
and college_enrollment = 4368

%sql select community_area_number, community_area_name, hardship_index from CENSUS_DATA \
   where community_area_number in \
   ( select community_area_number from CHICAGO_PUBLIC_SCHOOLS_DATA order by college_enrollment desc limit 1 )