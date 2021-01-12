import subprocess 
import os, sys
import signal
import pickle
from get_plots import load_from_file

class monitor:
    def start_mon(self, testname):
        cmd = "python3 mon.py -n "+testname
        # Run in background with Popen
        proc = subprocess.Popen(cmd, shell=True)
        print("Process PID: "+proc.pid)
        return int(proc.pid)

    def stop_mon(self, testname, pid):
        # Send CTRL+C signal
        os.killpg(pid, signal.SIGINT)
        # Read result files
        return read_results(testname)

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
mon = monitor()
testname="test"
results = mon.read_results(testname)
print(results[3])

        
        
        

