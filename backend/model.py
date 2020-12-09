from ml_model import machine_learning
import getopt, sys, os
import time, signal
import pickle

def get_opts():
    global add_host, host_data, update_classifier, update_regressor, update_clustering, update_int
    add_host, update_classifier, update_regressor, update_clustering = False, False, False, False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hncrli:",["help","classifier","regressor","clustering","interval=","addhost="])
    except getopt.GetoptError:
        print("Syntax err: "+path.basename(__file__)+" --classifier --regressor --clustering -i <update_interval> --add <host_ip>,<user>,<pass>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(path.basename(__file__)) 
            print("Options:")
            print("\t-h : display this menu.")
            print("\t--classifier: update classifier model.")
            print("\t--regressor: update regressor model.")
            print("\t--clustering: update clustering model.")
            print("\t-i: update interval in seconds.")
            sys.exit()
        elif opt in ("--classifier"):
            update_classifier = True
        elif opt in ("--regressor"):
            update_regressor = True
        elif opt in ("--clustering"):
            update_clustering = True
        elif opt in ("-i", "--interval"):
            update_int = int(arg)
        elif opt in ("--add", "--addhost"):
            add_host = True
            host_data = str(arg).split(",")
            print(host_data)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print("Model update process finished correctly.")
    sys.exit(0)

def add_host_tofile():
    model_dir="models"
    hostfile = model_dir+'/hosts.p'
    host = {
        "IP": host_data[0],
        "username": host_data[1],
        "password": host_data[2]
        }
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print("INFO: Directory "+model_dir+" created.")
    if os.path.exists(hostfile):
        hosts = pickle.load(open(hostfile, 'rb'))
    else:
        hosts = list()
    hosts.append(host)
    pickle.dump(hosts, open(hostfile, 'wb'))
    print("Host "+host["IP"]+" added successfully")

def main():
    get_opts()
    if(add_host):
        add_host_tofile()
    else:
        model_dir="models"
        hostfile = model_dir+'/hosts.p'
        ml=machine_learning()
        # Update models every update_int
        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C to stop model')
        while 1:
            if(os.path.exists(hostfile)):
                if (update_classifier):
                    ml.classifier()
                if (update_regressor):
                    ml.regressor()
                if (update_clustering):
                    ml.clustering()
            else:
                print("Waiting for hostfile!")
            time.sleep(update_int)
if __name__=="__main__":
    main()