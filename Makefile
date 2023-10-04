DIR := ${CURDIR}

postgresql_start: postgresql_rm
	docker run -e POSTGRES_HOST_AUTH_METHOD=trust --name alpinista -v $(DIR)/data:/var/lib/postgresql-files -p 5432:5432 -d postgres:12-alpine
	@{ \
		echo "waiting for postgresql : \c" ; \
		while !(psql -h localhost -U postgres -c "select version(); " 2> /dev/null ) ; \
		do  sleep 1 ; echo '#\c' ; done ; \
		echo " => progresql started" ; \
		createdb -h localhost -U postgres dev ; \
		echo 'created database "dev"' ; \
		echo "connect using:\n\npsql -h localhost -U postgres dev\n" ; \
	}

postgresql_rm:
	@# added true, to make sure this command always succeeds from a Make perspective
	docker rm alpinista ; true

postgresql_stop:
	docker stop alpinista

postgresql_restart: postgresql_stop postgresql_start

postgresql_fill_messages:
	@{ \
	   psql -h localhost -U postgres dev -c "\copy ship_messages_shipmessage \
	   (device_id,datetime,address_ip, address_port,original_message_id, \
	   status,lat,lat_dir,lon,lon_dir,spd_over_grnd,true_course,datestamp,mag_variation,mag_var_dir) \
	   from 'cleaned_messages.csv' with delimiter ','  csv header"; \
   }

postgresql_fill_ship:
	@{ \
  		echo "Inserting the weather data for ship st-1a290" ; \
  		psql -h localhost -U postgres dev -c "truncate ship_messages_ship1a2090; \
  		insert into ship_messages_ship1a2090 (datetime, wind_spd, weather, temp, pres) \
  		select a.datetime, c.wind_spd, c.weather, c.temp, c.pres \
        from (select * from ship_messages_shipmessage where device_id = 'st-1a2090' and date_trunc('day', datetime)='2019-02-13') a \
        inner join ship_messages_weatherstation b \
        on a.lat=b.lat and a.lon=b.lon \
        left join ship_messages_measurement c \
        on c.weather_station_id=b.id and abs(extract(epoch from c.timestamp_utc) - extract(epoch from a.datetime)) \
        = (select min(abs(extract(epoch from timestamp_utc) - extract(epoch from a.datetime))) \
        from ship_messages_measurement where weather_station_id = b.id) \
        order by a.datetime;" ; \
  	}

postgresql_fill_ship_detailed:
	@{ \
  		echo "This might take a little longer." ; \
  		psql -h localhost -U postgres dev -c "truncate ship_messages_ship1a2090; \
  		insert into ship_messages_ship1a2090 (datetime, wind_spd, weather, temp, pres) \
  		select a.datetime, c.wind_spd, c.weather, c.temp, c.pres \
        from (select * from ship_messages_shipmessage where device_id = 'st-1a2090' and date_trunc('day', datetime)='2019-02-13') a \
        inner join ship_messages_weatherstation b \
          on acos(sin(a.lat/180 * pi())*sin(b.lat/180 * pi())+cos(a.lat/180*pi())*cos(b.lat/180*pi())*cos(b.lon/180*pi() - a.lon/180*pi())) = \
          (select min(acos(sin(a.lat/180*pi())*sin(lat/180*pi())+cos(a.lat/180*pi())*cos(lat/180*pi())*cos(lon/180*pi() - a.lon/180*pi()))) \
          from ship_messages_weatherstation) \
        left join ship_messages_measurement c \
          on c.weather_station_id=b.id and abs(extract(epoch from c.timestamp_utc) - extract(epoch from a.datetime)) \
          = (select min(abs(extract(epoch from timestamp_utc) - extract(epoch from a.datetime))) \
          from ship_messages_measurement where weather_station_id = b.id) \
        order by a.datetime;" ; \
  }

.PHONY: clean-pyc
clean-pyc:
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

.PHONY: clean-cache
clean-cache:
	@rm -rf */.pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .coverage
	@find . -name '.coverage.*' -exec rm -f {} +

.PHONY: clean
clean: clean-pyc clean-cache
