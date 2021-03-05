# OPeNDAP Request Compiler Application (`orca`)

The purpose of orca is to pull apart large `OPeNDAP` requests to `THREDDS` into bite-sized chunks. These chunks are then reassembled before returning to the user.

## Installation
We use `make` to handle the installation process. Copy and paste this section into your terminal:
```
make
source /tmp/orca-venv/bin/activate
```

## Run App
### Locally
Before starting the app, ensure that you have set all the required environment variables:
```
export FLASK_APP=orca/app.py
export DSN=postgresql://<USER>:<PASSWORD>@db3.pcic.uvic.ca/pcic_meta
```

Once those have all been set, `Flask` can be used to spin up an instance of `orca` on your local machine:
```
flask run
```

When the instance is running you can request a url in your browser in this form:
```
http://127.0.0.1:5000/orca/tasmax_day_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19500101-21001231_Canada/tasmax[0:150][0:91][0:206]
```

### Docker
To run the `orca` docker container ensure that you have set all variables in the `deployment.env` then run:
```
docker-compose up -d
```
To stop the container:
```
docker-compose down
```

Again you will be able to acesss the service through a url:
```
http://docker-dev03.pcic.uvic.ca:30333/orca/tasmax_day_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19500101-21001231_Canada/tasmax[0:150][0:91][0:206]
```

*NOTE: The variables in `deployment.env` are private and as such must not be committed to the repo*
