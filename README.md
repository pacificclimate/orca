# orca (OPeNDAP Request Compiler Application)

The purpose of orca is to pull apart large `OPeNDAP` requests to `THREDDS` into bite-sized chunks. These chunks are then reassembled before returning to the user.

## Installation
Copy and paste this section into your terminal:
```
python3 -m venv venv
source venv/bin/activate
export PIP_INDEX_URL=https://pypi.pacificclimate.org/simple
pip install -r requirements.txt -r test_requirements.txt
pip install -e .
```
