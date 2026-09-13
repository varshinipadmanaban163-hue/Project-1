import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, URL


engine = create_engine( "mysql+pymysql://root:NewTempPassword123!@localhost:3306/earthquake_db")



#SQL QUERIES

queries={


   '1.TOP 10 Strongest earthquake':"""
       select * from earthquake 
       order by mag desc limit 10;
    """,

   '2 .TOP 10 Deepest earthquake':"""
       select * from earthquake 
       order by depth_km desc limit 10;
    """,

   '3 .shallow earthquakes< 50 km and mag>7.5':"""
       select * from earthquake 
       where depth_km  < 50 and mag > 7.5 ;
    """,

   '4 .Average depth per continent':"""
       --Data not available
    """,

   '5 .Average magnitude  per magnitude type':"""
        select magType ,avg(mag) as avg_of_mag 
        from earthquake group by magType;
    """,

   '6.Year with most earthquakes':"""
       select YEAR(time) , count(*)  as count from earthquake
       group by YEAR(time) order by count desc limit 1;
    """,

   '7 .Month with most earthquakes':"""
       select MONTH(time) , count(*)  as count from earthquake
       group by MONTH(time) order by count desc limit 1;
    """,

   '8 .Day of week  with most earthquakes':"""
       select DAYNAME(time) , count(*)  as count from earthquake
       group by DAYNAME(time) order by count desc limit 1;
    """,
 
   '9 .Count of earthquake per hour of Day':"""
       select  HOUR(time) ,count(*) as count from earthquake
       group by HOUR(time) order by count ;
    """,

   '10 .Most active reporting network':"""
       select net, count(*)  as count from earthquake
       group by net order by count desc limit 1;
    """,

   '11 .Top 5 places with highest casualties':"""
       select place , max(felt)as casualties from earthquake
       group by place order by casualties desc limit 5;
    """,

   '12 .Top estimated economic loss per continent':"""
        --Data not available
    """,

   '13. Average economic loss by alert level':"""
       select alert ,count(*) as count from earthquake  
       group by alert;
    """,


   '14 .Count of reviewed vs automatic earthquakes':"""
        select status ,count(status) as status_count
        from earthquake group by status;
     """,

   '15 .Count of earthquake by type':"""
       select type, count(type) as type_count 
       from earthquake group by type;
    """,

   '16 .Number of earthquake by data type':"""
       select types, count(types)as number_of_eq 
       from earthquake group by types;
    """,

   '17.Average RMS and gap per continent':"""
       --Data not available
    """,

   '18 .Events with high station coverage':"""
        select nst ,place , country from earthquake
        where nst> 50 order by nst desc;
    """,


   '19 .Number of tsunami triggered per Year':"""
        select tsunami, count(tsunami)as tsunmai_triggered 
        from earthquake group by tsunami;
    """,

   '20 .count earthquake by alert level':"""
       select alert ,count(*) as count from earthquake  
       group by alert;
    """,


   '21.Top 5 countries  with highest average magnitude':"""
       select country , avg(mag) as avg_magnitude from earthquake
       group by country order by avg_magnitude desc limit 5;
    """,

   '22.Countries experienced both shallow and deep earthquake in same Month':"""
       select year, month , country  from earthquake
       group by year ,month,country
       having sum(case when depth_km <= 50 then "1" else "0" end) and sum(case when depth_km > 50 then "1" else "0" end) ;
    """,

   '23 .year-over-year growth rate in total number of earthquake':"""
       select count(*),year from earthquake
       group by year;
    """,

   '24 .Top 3 seismically active region ':"""
       select place , count(*) as frequency ,avg(mag) as avg_mag,
       (count(*) * avg(mag)) as seismic_activity from earthquake
       group by place order by seismic_activity desc limit 3;
    """,


   '25 .Average depth_km within latitude +5 or -5 for each countries':"""
       select country , avg(depth_km) from earthquake
       where latitude between -5 and 5 
       group by country;
    """,


   '26. Countries having highest ratio of shallow and deep earthquake':"""
        select country ,(case when depth_km <= 50 then "1" else "0" end)as shallow_eq,
        (case when depth_km > 50 then "1" else "0" end)as deep_eq,
        (case when depth_km <= 50 then "1" else "0" end)/(case when depth_km > 50 then "1" else "0" end) * 100 as shallow_to_deep_ration
        from earthquake ;
    """,

   '27 . average magnitude difference between earthquake alerts and those without':""" 
        select (case when alert= "0" then "without_alert" else "with_alert" end) as alert_status,
        avg(mag) as avg_magnitude from earthquake 
        group by alert_status;
    """,

   '28 .Events with lowest data reliablility':"""
       select * from earthquake
       order by gap desc , rms desc  limit 10;
    """,

   '29 .pairs of consecutive earthquake occured 50 km and within 1 hour':"""
       --Data unavaliable
    """, 

   '30 . The region with highest frequency of deep focus earthquake':"""
       select place , count (*) as deep_eq from earthquake 
       where depth_km > 300
       group by place
       order by deep_eq desc limit 1;
    """
    
}

#streamlit


st.title("Global Seismic Earthquake Analysis Dashboard")
st.write("Select any problem to run")

task = st.selectbox("Choose task number", list(queries.keys()))

if st.button("Run Query"):
    query = queries[task]
    df = pd.read_sql(query, engine)
    st.subheader(f"Results for: {task}")
    st.dataframe(df,width= 'stretch')