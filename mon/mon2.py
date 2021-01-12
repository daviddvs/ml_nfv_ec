from paramiko import SSHClient, AutoAddPolicy
import sys, getopt, os
import datetime
import signal
import time
import pickle

load_pct = list()
used_ram_pct = list()
br_mbps = list()
ssh_list = list()
data = list()


def get_opts():
    global test_name, add_host, host_data
    test_name="testName"
    add_host=False
    host_data=None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hn:a:",["help","name=","add="])
    except getopt.GetoptError:
        print("Syntax err: "+os.path.basename(__file__)+" -n <test_name> --add hostname,user,password")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(os.path.basename(__file__)) 
            print("Options:")
            print("\t-h : display this menu.")
            print("\t-n <test_name>: set the name of the test to plot.")
            sys.exit()
        elif opt in ("-n", "--name"):
            test_name = str(arg)
        elif opt in ("--add", "--addhost"):
            add_host = True
            host_data = str(arg).split(",")
            print(host_data)

def add_host_tofile():
    hostfile = './hosts.p'
    host = {
        "IP": host_data[0],
        "username": host_data[1],
        "password": host_data[2]
        }
    if os.path.exists(hostfile):
        hosts = pickle.load(open(hostfile, 'rb'))
    else:
        hosts = list()
    hosts.append(host)
    pickle.dump(hosts, open(hostfile, 'wb'))
    print("Host "+host["IP"]+" added successfully")

def get_hosts():
    hostfile = './hosts.p'
    if os.path.exists(hostfile):
        hosts = pickle.load(open(hostfile, 'rb'))
    else:
        hosts = None
    return hosts

def print_hosts(hosts):
    for host in hosts:
        print(host["IP"]+" -> "+host["username"]+"/"+host["password"])

def ssh_session(hostname, username, password):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    return ssh

def get_ssh_sessions(diff, hosts):
    for i in range(1,diff+1):
        print(hosts[diff-i]["IP"])
        ssh = ssh_session(hosts[diff-i]["IP"], hosts[diff-i]["username"], hosts[diff-i]["password"])
        ssh_list.append(ssh)

def check_host_count(hosts, host_count):
    if (len(hosts)!=host_count):
        diff = len(hosts) - host_count
        host_cnt = len(hosts)
    else:
        host_cnt = host_count
        diff = 0
    return diff, host_cnt

def get_load_pct(ssh):
    # Packet "sysstat" required in target machine
    cmd = "sar -u 1 1"
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
    for ssh in ssh_list:
        ssh.close()
    print("Total number of measures: "+str(len(data)))
    save_to_file(data,"mon_data")
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
    host_count=0
    # Read options
    get_opts()
    if(add_host):
        add_host_tofile()
    else:
        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C to exit and save metrics')
        while 1: 
            hosts = get_hosts()
            if (hosts == None):
                print("No host found in ./hosts.p file")
                time.sleep(1)
                #sys.exit(2)
            else:            
                #print_hosts(hosts)
                diff, host_count = check_host_count(hosts,host_count)
                get_ssh_sessions(diff, hosts) # ssh_list is fulfilled
                print("Number of monitored hosts: "+str(len(ssh_list)))
                # Get metrics
                n=0
                hosts_data=list()
                for ssh in ssh_list:
                    now = datetime.datetime.now().timestamp()
                    load_pct = get_load_pct(ssh)
                    used_ram_pct = get_used_ram_pct(ssh)
                    br_rx_mbps, br_tx_mbps = get_bitrate(ssh,"ens3")
                    br_mbps = [br_rx_mbps,br_tx_mbps]
                    print("Storing data from h"+str(n))
                    hosts_data.append([load_pct, used_ram_pct, br_mbps, now, n])
                    n+=1
                data.append(hosts_data)
                print(data)
                time.sleep(1)

if __name__ == '__main__':
    main()
