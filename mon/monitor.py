import subprocess 
import os, sys
import signal
import pickle
#from get_plots import load_from_file
import time

class monitor:
    def start_mon(testname):
        cmd = "python3 mon2.py -i eth0 -n "+testname
        # Run in background with Popen
        proc = subprocess.Popen(cmd, shell=True)
        print("Process PID: "+str(proc.pid))
        # PID must be increased to work (probably due to shell=True param)
        pid = proc.pid + 1
        return pid

    def stop_mon(pid):
        # Send CTRL+C signal
        try:
            os.kill(pid, signal.SIGINT)
            msg="Process correctly stopped"
        except ProcessLookupError:
            msg="No such PID"
        print(msg)
        return msg
        # Read result files
        #return read_results(testname)

    '''
    # Dejo esto para que se haga manual 
    def read_results(self,testname):
        hostfile = './hosts.p'
        if os.path.exists(hostfile):
            hosts = pickle.load(open(hostfile, 'rb'))
        else:
            print("Error: "+hostfile+" not found")
            #sys.exit(2)
            hosts = None
        load_pct, used_ram_pct, br_mbps = load_from_file(testname)
        return [load_pct, used_ram_pct, br_mbps, hosts]
    '''