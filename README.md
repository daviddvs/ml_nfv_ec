# ML application for NFV
This repo contains the code of Python-based ML application designed for NFV. The application is also oriented to a vehicular scenario.

## Scenario
There are four elements in the architecture:
- Client: uses the REST API to request predictions
- Backend: runs the REST backend and the ML prediction
- Modeler: creates and distributes the model to the backend
- Monitor: monitors backed (CPU, RAM and Bitrate)
- Balancer: balances the load between multiple instances of the backend

## Get started
Clone this repo in the root directory of your user.
```
cd ~
git clone https://github.com/daviddvs/ml_nfv_ec.git
```

Run the **Backend** server.
```
cd ~/ml_nfv_ec/backend
pip3 install -r requirements.txt
python3 server.py
```

Run the **Modeler** to create/update models in the Backend. Note that hosts must be added so that the modeler knows which are the IP and credentials of the target hosts. It can be done before of after running the Modeler.
Note: press CTRL+C to exit.
```
cd ~/ml_nfv_ec/backend
pip3 install -r requirements.txt
python3 model.py --classifier --regressor --clustering -i <update_interval_seconds>
python3 model.py --addhost <IP,user,password>
```

Run the **Monitor**. 
This will gather CPU, RAM and TX/RX bitrate info from the specified machines (e.g. Backend) and it will save it into a results dir. It provides a REST API so that the Client can trigger the monitoring of the added machines.
Add hosts for monitoring (they can be added on the fly) and start REST server:
```
cd ~/ml_nfv_ec/mon
pip3 install -r requirements.txt
python3 mon2.py --add <IP,user,password>
python3 server.py
```

Run the tests in the **Client**. A file with data to be processed will be downloaded once and stored in the Client.
Data from that file will be extracted and sent to the Backend. 
In the case of clustering algorithm, data is loaded from the sklearn python library.
The Client also communicates with the REST API of the Monitor to trigger the monitoring of the previously added machines. 
Note: The IP of the Monitor must be manually edited in the `rest_test_data.py` file.
```
cd ~/ml_nfv_ec/cli
pip3 install -r requirements.txt
python3 rest_test_data.py -t <type_of_algorithm> -n <number_of_prediction_elem> -r <repetitions> -T <test_name>
# As an example:
python3 rest_test_data.py -t clustering -n 4 -r 50 -T test3
```

Plot test results
 - Prediction and response time
    ```
    cd ~/ml_nfv_ec/cli
    python3 get_plots.py -n <test_name>
    ```
 - CPU, RAM and Bitrate
    ```
    cd ~/ml_nfv_ec/mon
    python3 get_plots2.py -n <test_name>
    ```

## Configure the Balancer
We use the `haproxy` to balance the load between the multiple instances of the Backend server.
The balancer should run in a differen machine inside the Backend's network.
HA-Proxy version 1.8.8-1ubuntu0.11 2020/06/22.
For more information go to this [page](https://devops.ionos.com/tutorials/install-and-configure-haproxy-load-balancer-on-ubuntu-1604/).

Install the package on Linux.
```
sudo apt install haproxy
```

Edit the config file `/etc/haproxy/haproxy.cfg` to add the following lines.
```
listen firstbalance
        bind *:<local_port>
        balance roundrobin
        option forwardfor
        option httpchk
        server webserver1 <host_ip/name>:<remote_port>
        server webserver2 <host_ip/name>:<remote_port>
```
   - *roundrobin*: balancing criteria algorithm
   - *forwardfor*: capture the client's source IP address in our web server's logs
   - *httpchk*: look for a successful HTTP response

Restart the service.
```
sudo service haproxy restart
```

## Check machine status
These are the main commands to check Backend machine status. More infor [here](stress.md).
```
cat /proc/loadavg  | awk '{load_pct=$1*100.00} END {print load_pct}'
sudo apt install sysstat
sar -u 1
sar -u 1 1 # CPU
free # RAM
sar -n DEV 1 1 # bitrate
mpstat
mpstat -P ALL
htop
```

## Interesting links
- [Multiprocessing/Multithreading](https://stackoverflow.com/questions/9786102/how-do-i-parallelize-a-simple-python-loop)
