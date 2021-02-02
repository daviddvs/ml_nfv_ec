import matplotlib.pyplot as plt
import sys, getopt, os
import pickle

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
    for f in test_files:
        filename=result_dir+"/"+f
        if "tpred" in f:
            t_pred = pickle.load(open(filename, 'rb'))
        if "tresp" in f:
            t_resp = pickle.load(open(filename, 'rb'))
    elem = test_files[0].split("-")[2].split("_")[0]
    rep = test_files[0].split("-")[2].split("_")[1].split(".")[0]
    return t_pred, t_resp, elem

def plot_graph(x,y,label,init,end,xlabel,ylabel,title,filename,plot_dir):
    #  Check if plot dir exists and create it
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    # Plot figure and save
    plt.figure()
    for i in range(0,len(y)):
        plt.plot(x[init:end],y[i][init:end],label=label[i])
        #plt.plot(x,y[i],label=label[i])
    plt.legend()
    axes = plt.gca()
    axes.set_xlim([x[init],x[end-1]])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
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


if __name__=="__main__":
    main()
