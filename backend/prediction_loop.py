from ml_predict import machine_learning as ml
import sys, getopt

num=1
rep=1
accum_pred_time=0

try:
    opts, args = getopt.getopt(sys.argv[1:],"hn:r:",["help","num=","rep="])
except getopt.GetoptError:
    print('Bad syntax err: prediction_loop.py -n <number_of_repetitions>')
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print('prediction_loop.py') 
        print('Options:')
        print('\t-h : display this menu')
        print('\t-n <number_of_elements>: set the number of elements (63*n) for ml_predict.py (default 1)')
        print('\t-n <number_of_repetitions>: set the number of repetitios for ml_predict.py (default 1)')
        sys.exit()
    elif opt in ("-n", "--num"):
        num = int(arg)
    elif opt in ("-r", "--rep"):
        rep = int(arg)

for i in range(1,rep+1):
    pred_time, elem = ml.rocksMines_dataset(N=num)
    pred_time_elem = (pred_time/elem)*1000
    print("Mean time to predict one element: {0:.2f} us.".format(pred_time_elem))
    accum_pred_time = accum_pred_time + pred_time
mean_time = accum_pred_time/rep
print(str(rep)+" predictions done in {0:.2f} ms. Mean time = {1:.2f} ms".format(accum_pred_time, mean_time))

