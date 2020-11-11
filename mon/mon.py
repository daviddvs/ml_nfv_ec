from paramiko import SSHClient
import sys, getopt, os
import datetime
import signal
import time
import pickle

load_pct = list()
used_ram_pct = list()
br_mbps = list()
mon_hosts = [ 
    {# SERVER
        "IP": "10.98.1.26",
        "username": "ubuntu",
        "password": "osm2018",
        "cpu": True
    },
    {# MODELER
        "IP": "10.98.1.43",
        "username": "ubuntu",
        "password": "i2t",
        "cpu": True
    }
]

def get_opts():
    global test_name
    test_name=""
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hn:",["help","name="])
    except getopt.GetoptError:
        print("Syntax err: "+os.path.basename(__file__)+" -n <test_name>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(os.path.basename(__file__)) 
            print("Options:")
            print("\t-h : display this menu.")
            print("\t-n <test_name>: set the name of the test to plot.")
            sys.exit()
        elif opt in ("-n", "--num"):
            test_name = str(arg)
    if test_name=="":
        print("Syntax err: Option -n <test_name> must be specified")
        sys.exit(2)

def print_hosts():
    for host in mon_hosts:
        print(host["IP"]+" -> "+host["username"]+"/"+host["password"])

def ssh_session(hostname, username, password):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname, username=username, password=password)
    return ssh

def get_load_pct(ssh):
    # Packet "sysstat" required in target machine
    cmd = "sar -u 0"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    idle = float(ssh_stdout.read().decode("utf-8").split("\n")[3].split()[7])
    return round(float(100-idle),2)

def get_used_ram_pct(ssh):
    cmd = "free"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    ram = ssh_stdout.read().decode("utf-8")
    total_ram = float(ram.split("\n")[1].split()[1])
    used_ram = float(ram.split("\n")[1].split()[2])
    return round(float(used_ram/total_ram*100),2)

def get_bitrate(ssh,int_name,kbps=False):
    cmd = "sar -n DEV 1 1"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    br = ssh_stdout.read().decode("utf-8").split(int_name)[1].split()
    if (kbps): # kbps
        br_rx = round(float(br[2])*8,2)
        br_tx = round(float(br[3])*8,2)
    else: # mbps
        br_rx = round(float(br[2])*8/1000,2)
        br_tx = round(float(br[3])*8/1000,2)
    return br_rx, br_tx

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    ssh.close()
    print("Total number of measures: "+str(min([len(load_pct),len(used_ram_pct),len(br_mbps)])))
    save_to_file(load_pct,"load_pct")
    save_to_file(used_ram_pct,"used_ram_pct")
    save_to_file(br_mbps,"br_txrx_mbps")
    sys.exit(0)

def save_to_file(obj,type_name):
    # Create dir if it does not exist
    result_dir="results"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    # Save the object to file
    filename = result_dir+"/"+test_name+"-"+type_name+".p"
    pickle.dump(obj, open(filename, 'wb'))
    print(type_name+"\tsaved into -> "+filename)

def main():
    # Read options
    get_opts()
    # Set ssh conn
    global ssh
    meas_num=0
    ssh = ssh_session(mon_hosts[0]["IP"], mon_hosts[0]["username"], mon_hosts[0]["password"])
    # Get metrics
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit and show metrics')
    while 1:
        now = datetime.datetime.now().timestamp()
        load_pct.append([get_load_pct(ssh), now])
        used_ram_pct.append([get_used_ram_pct(ssh), now])
        br_rx_mbps, br_tx_mbps = get_bitrate(ssh,"ens3")
        br_mbps.append([[br_rx_mbps,br_tx_mbps],now])
        time.sleep(1)

if __name__ == '__main__':
    main()