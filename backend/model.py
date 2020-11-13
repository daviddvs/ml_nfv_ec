from ml_model import machine_learning
import getopt, sys
import time, signal

def get_opts():
    global update_classifier, update_regressor, update_clustering, update_int
    update_classifier, update_regressor, update_clustering = False, False, False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hncrli:",["help","classifier","regressor","clustering","interval="])
    except getopt.GetoptError:
        print("Syntax err: "+path.basename(__file__)+" --classifier --regressor --clustering -i <update_interval>")
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

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    print("Model update process finished correctly.")
    sys.exit(0)

def main():
    get_opts()
    ml=machine_learning()
    # Update models every update_int
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to stop model')
    while 1:
        if (update_classifier):
            ml.classifier()
        if (update_regressor):
            ml.regressor()
        if (update_clustering):
            ml.clustering()
        time.sleep(update_int)

if __name__=="__main__":
    main()