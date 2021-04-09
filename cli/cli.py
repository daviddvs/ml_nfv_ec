import sys, getopt, os
import subprocess
import requests
import http
import time
import random
import signal

def get_opts():
    global ip, mon_ip, typ, num, rep, url, test_name, index # declare global vars
    typ="classifier"
    num=1 
    rep=1
    ip="127.0.0.1"
    mon_ip="127.0.0.1"
    index=0
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:m:t:n:r:T:",["help","ser=","mon=","typ=","num=","rep=","testname="])
    except getopt.GetoptError:
        print("Syntax err:"+os.path.basename(__file__)+" -s <server_ip> -m <monitor_ip> -t <type_of_algorithm> -n <number_of_prediction_elem> -r <repetitions> -T <test_name>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(os.path.basename(__file__)) 
            print("Options:")
            print("\t-h : display this menu.")
            print("\t-n <number_of_prediction_elements>: set the number of elements (default 1) to predict."+ 
                    " 63*2^n for classifier and regressor.")
            print("\t-r <number_of_repetitions>: set the number of repetitios (default 1) to predict.")
            print("\t-t <type_of_algorithm>: set the algorithm to classifier/regressor.")
            print("\t-T <test_name>: set a name for the test.")
            print ("\t-s <server_ip>: set the ip address of the backend server (default 127.0.0.1")
            print ("\t-m <monitor_ip>: set the ip address of the monitor (default 127.0.0.1")
            sys.exit()
        elif opt in ("-n", "--num"):
            num = int(arg)
        elif opt in ("-r", "--rep"):
            rep = int(arg)
        elif opt in ("-t", "--typ"):
            typ = str(arg)
        elif opt in ("-T", "--testname"):
            test_name = str(arg)
        elif opt in ("-s", "--server"):
            ip = str(arg)
        elif opt in ("-m", "--monitor"):
            mon_ip = str(arg)
    if typ not in ("classifier","regressor","clustering"):
        print("Syntax err: no such ML algorithm "+typ+". Try classifier, regressor or clustering.")
        sys.exit(2)

def start_remote_mon(mon_ip,mon_port,testname):
    url="http://"+mon_ip+":"+mon_port+"/api/start_mon?testname="+testname
    print(url)
    try:
        response = requests.get(url)
    except http.client.HTTPException as e:
        print(e)
    return response.json()

def stop_remote_mon(mon_ip,mon_port,pid):
    url="http://"+mon_ip+":"+mon_port+"/api/stop_mon?pid="+str(pid)
    try:
        response = requests.get(url)
    except http.client.HTTPException as e:
        print(e)
    return str(response.json())

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    msg = stop_remote_mon(mon_ip,mon_port,pid)
    print("Remote monitoring: "+str(msg))
    sys.exit(0)

def main():
    get_opts()
    global mon_port, pid
    mon_port = "5001"
    pid = start_remote_mon(mon_ip,mon_port,test_name)
    # The following two params can be inserted from the command line
    duration = 180
    max_slot = 3
    accum_slot = 0
    i=0
    signal.signal(signal.SIGINT, signal_handler)
    print(f'Press Ctrl+C to exit and save metrics or program will finish in {duration} ms')
    while 1: 
    #for i in range(0,duration):
        repe = random.randint(1, rep)
        cmd = f"python3 rest_test_data.py -s {ip} -t {typ} -n {num} -r {repe} -T {test_name} -i {i}"
        #proc = subprocess.run(cmd, shell=True)
        proc = subprocess.Popen(cmd, shell=True) #Parallel execution
        slot = random.randint(1, max_slot)
        time.sleep(slot)
        accum_slot = accum_slot + slot
        i+=1
        if(accum_slot >= duration):
            print(f"Accum slot: {accum_slot}")
            msg = stop_remote_mon(mon_ip,mon_port,pid)
            print("Remote monitoring: "+str(msg))
            break

if __name__=="__main__":
    main()