# ML application for NFV
This repo contains the code of Python-based ML application designed for NFV. The application is also oriented to a vehicular scenario.

## Scenario
There are four elements in the architecture:
- Client: uses the REST API to request predictions
- Backend: runs the REST backend and the ML prediction
- Modeler: creates and distributes the model to the backend
- Monitor: monitors backed (CPU, RAM and Bitrate)

## Get started
Clone this repo and install the Python requirements for each element of the architecture.
```
cd ~
git clone https://github.com/daviddvs/ml_nfv_ec.git
cd ml_nfv_ec/<element>
pip3 install -r requirements.txt
```

Run the Backend server.
```
cd ~/ml_nfv_ec/backend
python3 server.py
```

Run the Modeler to create/update models in the Backend.
Note: server IP must be edited in `ml_model` to point to the Backed server.
Note: update interval in seconds
```
cd ~/ml_nfv_ec/backend
python3 model.py --classifier --regressor --clustering -i <update_interval>
# As an example
python3 model.py --classifier --regressor --clustering -i 5
```

Run the Monitor. 
This will gather CPU, RAM and bitrate info from the Backend machine and it will the save into a results dir.
Backedn machine IP must be edited in the file.
```
cd ~/ml_nfv_ec/mon
python3 mon.py
```

Run the tests in the Client. A file with data to be processed will be downloaded in the Client and sent to the Backend.
```
cd ~/ml_nfv_ec/cli
python3 rest_test_data.py -t <type_of_algorithm> -n <number_of_prediction_elem> -r <repetitions> -T <test_type>
# As an example:
python3 rest_test_data.py -t clustering -n 4 -r 50 -T test3
```

Plot test results
 - Prediction and response time
    ```
    cd ~/ml_nfv_ec/cli
    python3 get_plots.py -n <test_name>
    # As an example:
    python3 get_plots.py -n test3
    ```
 - CPU, RAM and Bitrate
    ```
    cd ~/ml_nfv_ec/mon
    python3 get_plots.py -n <test_name>
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
