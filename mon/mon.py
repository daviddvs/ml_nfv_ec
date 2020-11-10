from paramiko import SSHClient
import sys
import matplotlib.pyplot as plt
import os.path as path
import datetime
import signal
import time

load_pct = list()
used_ram_pct = list()
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

def plot_graph(x,y,label,init,end,xlabel,ylabel,title,filename):
    plt.figure()
    for i in range(0,len(y)):
        plt.plot(x[init:end],y[i][init:end],label=label[i])
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([init,end])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(results_dir+filename)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    ssh.close()
    print(load_pct)
    print(used_ram_pct)
    sys.exit(0)

def main():
    # Set ssh conn
    global ssh 
    ssh = ssh_session(mon_hosts[0]["IP"], mon_hosts[0]["username"], mon_hosts[0]["password"])
    # Get metrics
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit and show metrics')
    while 1:
        load_pct.append([get_load_pct(ssh), datetime.datetime.now().timestamp()])
        used_ram_pct.append([get_used_ram_pct(ssh), datetime.datetime.now().timestamp()])
        time.sleep(1)
    
    

if __name__ == '__main__':
    main()