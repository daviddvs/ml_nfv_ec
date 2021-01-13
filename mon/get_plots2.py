import matplotlib.pyplot as plt
import sys, getopt, os
import pickle

def get_opts():
    global test_name
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hn:",["help","name="])
    except getopt.GetoptError:
        print("Bad syntax err: "+path.basename(__file__)+" -n <test_name>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(path.basename(__file__)) 
            print("Options:")
            print("\t-h : display this menu.")
            print("\t-n <test_name>: set the name of the test to plot.")
            sys.exit()
        elif opt in ("-n", "--name"):
            test_name = str(arg)

def load_from_file(test_name):
    # Chech if results dir exists and read files
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
    hosts_data = list()
    initial_hosts = len(data[0])
    final_hosts = len(data[-1])
    for i in range(0,final_hosts):
        for d in data:
            try:
                host_data.append(d[i])
            except IndexError:
                host_data.append([])
        hosts_data.append(host_data)
    return hosts_data

def plot_graph(x,y,label,init,end,xlabel,ylabel,title,filename,plot_dir,br=False):
    #  Check if plot dir exists and create it
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    # Plot figure and save
    plt.figure()
    for i in range(0,len(y)):
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
            yy_load.append(i[0])
            yy_ram.append(i[1])
            yy_br.append(i[2])
            xx.append(i[3])
        y_load.append(yy_load)
        y_ram.append(yy_ram)
        y_br.append(yy_br)
        x.append(xx)
    return y_load, y_ram, y_br, x

def main():
    get_opts()
    hosts_data = load_from_file(test_name)
    load_pct, used_ram_pct, br_mbps, x = get_data(hosts_data)
    print (load_pct)
    print (used_ram_pct)
    print (br_mbps)
    print (x)
    plot_dir="plots"
    host_num=len(load_pct)
    #Plot load pct
    x = normalize(x[0])
    y = load_pct
    label_load_ram=list()
    label_br=list()
    for i in range(0,host_num):
        label_load_ram.append("host_"+str(i))
        label_br.append("host_"+str(i)+" RX")
        label_br.append("host_"+str(i)+" TX")
    plot_graph(x,y,label_load_ram,0,len(x),"Time(s)","Load (%)","Load Percentage",test_name+"-load_pct.png",plot_dir)
    # Plot used ram pct
    y = used_ram_pct
    plot_graph(x,y,label_load_ram,0,len(x),"Time(s)","Used RAM (%)","Used RAM Percentage",test_name+"-used_ram_pct.png",plot_dir)
    # Plot bitrate
    y=list()
    for br in br_mbps:
        rx,tx = split_xy(br)
        y.append(rx)
        y.append(tx)
    plot_graph(x,[rx,tx],label_br,0,len(x),"Time(s)","Bitrate (Mbps)","RX/TX Bitrate",test_name+"-br_txrx_mbps.png",plot_dir)

if __name__ == '__main__':
    main()