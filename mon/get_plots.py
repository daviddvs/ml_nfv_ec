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
    test_files = list()
    if not os.path.exists(result_dir):
        print("Error: No result directory found")
        sys.exit(2)
    else:
        files = os.listdir(result_dir)
        for f in files:
            if test_name in f:
                test_files.append(f)
    # Load objects from files
    for f in test_files:
        filename=result_dir+"/"+f
        if "load" in f:
            load_pct = pickle.load(open(filename, 'rb'))
        if "ram" in f:
            used_ram_pct = pickle.load(open(filename, 'rb'))
        if "br" in f:
            br_mbps = pickle.load(open(filename, 'rb'))
    return load_pct, used_ram_pct, br_mbps

def plot_graph(x,y,label,init,end,xlabel,ylabel,title,filename,plot_dir):
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

def get_xy(lst,brx=False):
    xx = list()
    x = list()
    y = list()
    for i in lst:
        xx.append(i[1])
        y.append(i[0])
    for i in xx:
        x.append(round(i-xx[0]))
    return x, y

def main():
    get_opts()
    load_pct, used_ram_pct, br_mbps = load_from_file(test_name)
    x_load_pct, y_load_pct = get_xy(load_pct)
    x_used_ram_pct, y_used_ram_pct = get_xy(used_ram_pct)
    x_br_mbps, y_br_mbps = get_xy(br_mbps)
    plot_dir="plots"
    # Plot load pct
    x = x_load_pct
    y = y_load_pct
    plot_graph(x,[y],["load %"],0,len(x),"Time(s)","Load (%)","Load Percentage",test_name+"-load_pct.png",plot_dir)
    # Plot used ram pct
    x = x_used_ram_pct
    y = y_used_ram_pct
    plot_graph(x,[y],["used RAM %"],0,len(x),"Time(s)","Used RAM (%)","Used RAM Percentage",test_name+"-used_ram_pct.png",plot_dir)
    # Plot bitrate
    x = x_br_mbps
    y = y_br_mbps
    label = ["br_rx_mbps","br_tx_mbps"]
    plot_graph(x,[y],label,0,len(x),"Time(s)","Bitrate (Mbps)","RX/TX Bitrate",test_name+"-br_txrx_mbps.png",plot_dir)

if __name__ == '__main__':
    main()