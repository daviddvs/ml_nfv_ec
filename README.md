# ML application for NFV
This repo contains the code of Python-based ML application designed for NFV. The application is also oriented to a vehicular scenario.

## Scenario
There are two elements in the architecture:
- Client: uses the REST API to request predictions
- Backend: runs the REST backend and the ML prediction

## Get started
This repo must be cloned in both Client and Backend machines.

1. Run the following command to set up python3 modules in Client/Backend.
```
pip3 install -r requirements.txt
```
2. Backend deployment
```
python3 ./backend/server.py
```
3. Run the Client
```
python3 ./cli/rest_test.py
```

## Check machine status
These are the main commands to check Backend machine status. More infor [here](stress.md).
```
cat /proc/loadavg  | awk '{load_pct=$1*100.00} END {print load_pct}'
sudo apt install sysstat
sar -u 1
mpstat
mpstat -P ALL
htop
```

## Interesting links
- [Multiprocessing/Multithreading](https://stackoverflow.com/questions/9786102/how-do-i-parallelize-a-simple-python-loop)
