# orca (OPeNDAP Request Compiler Application)

The purpose of orca is to pull apart large `OPeNDAP` requests to `THREDDS` into bite-sized chunks. These chunks are then reassembled before returning to the user.

## Installation
We use `make` to handle the installation process. Copy and paste this section into your terminal:
```
make
source /tmp/orca/venv/bin/activate
```

## Run App
`Flask` can be used to spin up an instance of `orca` on your local machine:
```
export FLASK_APP=orca/app.py
flask run
```
Once the instance has been spun up you can request a file from it using a url like this:
```
http://127.0.0.1:5000/orca/tasmax[0:150][0:91][0:206]/tasmax_day_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19500101-21001231_Canada
```
