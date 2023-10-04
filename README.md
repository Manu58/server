# The ship messages Django app

This is a Django site that can easily be deployed as a serverless site using zappa on AWS. 
You need to have python installed
to run it locally use the following steps (tested with python 3.10):
* Install docker (docker-desktop in osx, windows)
* Install the postgres client (psql or psql.exe on windows). The setup has been tested on Linux and osx
* From the root: 

      pip install -r dev_requirements.txt
*     cd src
*     ./manage.py migrate
*     ./manage.py createsuperuser 
     choose a name , some emaiil and a password (can be just one character)
*     ./manage.py runserver
* click on the link (http://127.0.0.1:8000)
* in the website click on the *+Add* next to Tokens
* pick your name from the dropdown list and click save.
* copy the token that appears and log out from the website (this is important! you could create a non superuser user and login with that one but you need to give him proper view rights on the ship messages)
*     cd ../
* Next we are going to import the cleaned_messages.csv

      make postgresql_fill_messages
*     cd utils
* edit the 'insert_weather_data.py' and paste the copied token on line 8 replacing the existing token. Then run:
*     python insert_weather_data.py
* This inserts (part of) the weather data in the database. It uses the rest api of the django site and this won't work while you are logged in as a superuser.
* Now you can login into the site again.
* From the root of the project run:
*     make postgresql_fill_ship
* This will create a table with weather conditions (wind speed, temperature, type of weather and air pressure) for ship st-1a2090 at 2019-02-13.  
  It matches exactly the latitude and longitude with a weather station and finds the measurement at a time closest to the datetime of the ship. 
  This results in a small number of points along the trajectory.  
  It is possible to get a measurement for each point along the trajectory.
  Hereto we calculate the closest weather station to a trajectory point and again find the closest time of measurement.
*     make postgres_fill_ship_detailed
* The metrics and generated weather tables are visible in the website.
* The local postgres database can be approached using psql on localhost port 5432 with user postgres without a password and database dev.

# Remarks.
All other metrics have been generated using Django's orm. 
A library Zappa has been included which makes it fairly straightforward to deploy the website serverless on AWS in a lambda.
A postgres RDS has to be setup and there is a choice of exposing the endpoints through API gateway or using a loadbalancer to keep it in the vpc.
The two sqls used to create the weather tables are for the small table:
```sql
insert into ship_messages_ship1a2090 (datetime, wind_spd, weather, temp, pres)
select a.datetime, c.wind_spd, c.weather, c.temp, c.pres
from 
    (select * from ship_messages_shipmessage 
              where device_id = 'st-1a2090' 
                and date_trunc('day', datetime)='2019-02-13') a
inner join ship_messages_weatherstation b
    on a.lat=b.lat and a.lon=b.lon  
    -- only choose weather stations that are at the point of the trajectory
left join ship_messages_measurement c
    on c.weather_station_id=b.id 
    and abs(extract(epoch from c.timestamp_utc) - extract(epoch from a.datetime))
    = (select min(abs(extract(epoch from timestamp_utc) - extract(epoch from a.datetime)))
from ship_messages_measurement where weather_station_id = b.id)
order by a.datetime;
```
and for the weather along every point of the trajectory:
```sql
insert into ship_messages_ship1a2090 (datetime, wind_spd, weather, temp, pres)
select a.datetime, c.wind_spd, c.weather, c.temp, c.pres
from 
    (select * from ship_messages_shipmessage 
              where device_id = 'st-1a2090' 
                and date_trunc('day', datetime)='2019-02-13') a
inner join ship_messages_weatherstation b  
    -- first getting the closest weather station
  on acos(sin(a.lat/180 * pi())*sin(b.lat/180 * pi())
          +cos(a.lat/180*pi())*cos(b.lat/180*pi())
          *cos(b.lon/180*pi() - a.lon/180*pi())) =
  (select min(acos(sin(a.lat/180*pi())*sin(lat/180*pi())
              +cos(a.lat/180*pi())*cos(lat/180*pi())
              *cos(lon/180*pi() - a.lon/180*pi())))
  from ship_messages_weatherstation)
left join ship_messages_measurement c
  on c.weather_station_id=b.id 
  and abs(extract(epoch from c.timestamp_utc) - extract(epoch from a.datetime))
  = (select min(abs(extract(epoch from timestamp_utc) - extract(epoch from a.datetime)))
  from ship_messages_measurement where weather_station_id = b.id)
order by a.datetime;
```