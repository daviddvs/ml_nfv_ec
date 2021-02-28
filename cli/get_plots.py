import matplotlib.pyplot as plt
import sys, getopt, os
import pickle
from scipy.interpolate import splrep, splev

def get_opts():
    global test_name
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
    test_files.sort() # sort files by name
    t_pred = list()
    t_resp = list()
    for f in test_files:
        filename=result_dir+"/"+f
        if "tpred" in f:
            t_pred_n = pickle.load(open(filename, 'rb'))
            t_pred = t_pred + t_pred_n # merge lists with "+"
        if "tresp" in f:
            t_resp_n = pickle.load(open(filename, 'rb'))
            t_resp = t_resp + t_resp_n # merge lists with "+"
    elem = test_files[0].split("-")[3].split("_")[0]
    #rep = test_files[0].split("-")[3].split("_")[1].split(".")[0]
    return t_pred, t_resp, elem

def plot_graph(x,y,label,init,end,xlabel,ylabel,title,filename,plot_dir):
    #  Check if plot dir exists and create it
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    # Plot figure and save
    plt.figure()
    for i in range(0,len(y)):
        smooth = splrep(x[init:end],y[i][init:end],s=15000)
        y_smooth = splev(x[init:end],smooth)
        plt.plot(x[init:end],y_smooth,label=label[i])
        #plt.plot(x[init:end],y[i][init:end],label=label[i])
    plt.legend()
    axes = plt.gca()
    axes.set_yscale('log')
    axes.set_xlim([x[init],x[end-1]])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(plot_dir+"/"+filename)
    print("Saved figure to -> "+plot_dir+"/"+filename)

def plot_hist(x1,x2,filename,plot_dir):
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    plt.tight_layout()
    ax1.hist(x1, ec='black')
    ax1.set_title('t_resp (ms)')
    ax2.hist(x2, ec='black')
    ax2.set_title('t_pred (ms)')
    plt.savefig(plot_dir+"/"+filename)
    print("Saved figure to -> "+plot_dir+"/"+filename)

def main():
    get_opts()
    t_pred, t_resp, elem = load_from_file(test_name)
    # Plot t_pred and r_resp in the same graphic
    plot_dir="plots"
    x = list(range(0,len(t_pred)))
    y = [t_pred,t_resp]
    label = ["t_pred","t_resp"]
    plot_graph(x,y,label,0,len(x),"Iterations","Time (ms)","Prediction/Response time for "+
        elem+" elements",test_name+"-tpred_tresp-"+elem+".png",plot_dir)
    plot_hist(t_resp,t_pred,test_name+"-tpred_tresp-"+elem+"_hist.png",plot_dir)

if __name__=="__main__":
    main()
