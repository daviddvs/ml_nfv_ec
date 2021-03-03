import matplotlib.pyplot as plt
import sys, getopt, os
import pickle
#from scipy.interpolate import splrep, splev
#import numpy as np

def get_opts():
    global test_name
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hn:",["help","name="])
    except getopt.GetoptError:
        print("Bad syntax err: "+os.path.basename(__file__)+" -n <test_name>")
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

def load_from_file(test_name):
    # Check if results dir exists and read files
    result_dir="results"
    test_file = result_dir+"/"+test_name+"-mon_data.p"
    # Load test data from file
    if os.path.exists(test_file):
        data = pickle.load(open(test_file, 'rb'))
    else:
        print("Error: No such file or directory found:"+test_file)
        sys.exit(2)
    # Reorder data
    host_data = list()
    host_num = len(data[-1]) # taken from the last sample to include hosts added on the fly
    sample_num = len(data)
    for i in range(0,host_num):
        for d in data:
            try:
                host_data.append(d[i])
            except IndexError:
                host_data.append([])
    hosts_data = split_hosts(host_data,sample_num,host_num)
    return hosts_data

def split_hosts(host_data, sample_num, host_num):
    hosts_data=list()
    for j in range(0,host_num):
        offset = j*sample_num
        h = host_data[offset:offset+sample_num]
        hosts_data.append(h)
    return hosts_data

def plot_graph(x,y,label,init,end,xlabel,ylabel,title,filename,plot_dir,stem=False,step=False):
    #  Check if plot dir exists and create it
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    # Plot figure and save
    plt.figure()
    for i in range(0,len(y)):
        #smooth = splrep(x[init:end],y[i][init:end],s=3)
        #y_smooth = splev(x[init:end],smooth)
        #plt.plot(x[init:end],y_smooth,label=label[i])
        if(stem):
            plt.stem(x[init:end],y[i][init:end],label=label[i])
        elif (step):
            plt.step(x[init:end],y[i][init:end],label=label[i])
        else:
            plt.plot(x[init:end],y[i][init:end],label=label[i])
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([x[init],x[end-1]])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(plot_dir+"/"+filename)
    print("Saved figure to -> "+plot_dir+"/"+filename)

def split_xy(lst):
    x = list()
    y = list()
    for i in lst:
        x.append(i[1])
        y.append(i[0])
    return x, y

def normalize(array):
    x=list()
    for i in array:
        x.append(round(i-array[0]))
    return x

def get_data(hosts_data):
    y_load = list()
    y_ram = list()
    y_br = list()
    x = list()
    for h in hosts_data:
        yy_load =list()
        yy_load = list()
        yy_ram = list()
        yy_br = list()
        xx = list()
        for i in h:
            if (len(i) != 0):
                yy_load.append(i[0])
                yy_ram.append(i[1])
                yy_br.append(i[2])
                xx.append(i[3])
            else:
                yy_load.append(0)
                yy_ram.append(0)
                yy_br.append([0,0])
                xx.append(0)
        y_load.append(yy_load)
        y_ram.append(yy_ram)
        y_br.append(yy_br)
        x.append(xx)
    return y_load, y_ram, y_br, x

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]

def interpolate_gaps(values, limit=None):
    """
    Fill gaps using linear interpolation, optionally only fill gaps up to a
    size of `limit`.
    """
    values = np.asarray(values)
    i = np.arange(values.size)
    valid = np.isfinite(values)
    filled = np.interp(i, i[valid], values[valid])

    if limit is not None:
        invalid = ~valid
        for n in range(1, limit+1):
            invalid[:-n] &= invalid[n:]
        filled[invalid] = np.nan

    return filled

def main():
    get_opts()
    hosts_data = load_from_file(test_name)
    #print(hosts_data)
    load_pct, used_ram_pct, br_mbps, x = get_data(hosts_data)
    print(load_pct)
    plot_dir="plots"
    host_num=len(load_pct)
    #Plot load pct
    x = normalize(x[0]) # you chose the first one, which is the full one
    y = load_pct
    label_load_ram=list()
    label_br=list()
    for i in range(0,host_num):
        label_load_ram.append("host_"+str(i))
        label_br.append("host_"+str(i)+" RX")
        label_br.append("host_"+str(i)+" TX")
    plot_graph(x,y,label_load_ram,0,len(x),"Time(s)","Load (%)","Load Percentage",test_name+"-load_pct.png",plot_dir, step=True)
    # Plot used ram pct
    y = used_ram_pct
    plot_graph(x,y,label_load_ram,0,len(x),"Time(s)","Used RAM (%)","Used RAM Percentage",test_name+"-used_ram_pct.png",plot_dir, step=True)
    # Plot bitrate
    y=list()
    for br in br_mbps:
        tx,rx = split_xy(br) # returns first the second position, which is tx
        #print(rx)
        #rx = zero_to_nan(rx) # convert zeros to 'nan' (not plotable)
        #rx = interpolate_gaps(rx)
        #tx = zero_to_nan(tx)
        #print(rx)
        y.append(rx)
        y.append(tx)
    plot_graph(x,y,label_br,0,len(x),"Time(s)","Bitrate (Mbps)","RX/TX Bitrate",test_name+"-br_txrx_mbps.png",plot_dir, step=True)

if __name__ == '__main__':
    main()