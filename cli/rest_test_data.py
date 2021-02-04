import sys, getopt, os
import requests
import http
import datetime
import concurrent.futures
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
import numpy as np

port="5000"
url_classifier="https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
url_regressor="http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"

def get_opts():
    global mon_ip, typ, num, rep, url, test_name, index # declare global vars
    typ="classifier"
    num=1 
    rep=1
    ip="127.0.0.1"
    mon_ip="127.0.0.1"
    index=0
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:m:t:n:r:T:i:",
        ["help","ser=","mon=","typ=","num=","rep=","testname=","index="])
    except getopt.GetoptError:
        print("Syntax err:"+os.path.basename(__file__)+" -s <server_ip> -m <monitor_ip> -t <type_of_algorithm> "+ 
        "-n <number_of_prediction_elem> -r <repetitions> -T <test_name> -i <index>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(os.path.basename(__file__)) 
            print("Options:")
            print("\t-h : display this menu")
            print("\t-n <number_of_prediction_elements>: set the number of elements (default 1) to predict"+ 
                    " 63*2^n for classifier and regressor")
            print("\t-r <number_of_repetitions>: set the number of repetitios (default 1) to predict")
            print("\t-t <type_of_algorithm>: set the algorithm to classifier/regressor")
            print("\t-T <test_name>: set a name for the test")
            print("\t-s <server_ip>: set the ip address of the backend server (default 127.0.0.1")
            #print("\t-m <monitor_ip>: set the ip address of the monitor (default 127.0.0.1")
            print("\t-i <test_index>: set the test index for a correct reordering (only used for scripting)")
            sys.exit()
        elif opt in ("-n", "--num"):
            num = int(arg)
        elif opt in ("-r", "--rep"):
            rep = int(arg)
        elif opt in ("-t", "--typ"):
            typ = str(arg)
        elif opt in ("-T", "--testname"):
            test_name = str(arg)
        elif opt in ("-s", "--server"):
            ip = str(arg)
        elif opt in ("-m", "--monitor"):
            mon_ip = str(arg)
        elif opt in ("-i", "--index"):
            index = int(arg)
    print("Algorithm: "+typ)
    if(typ=="classifier"):
        t="0"
    elif(typ=="regressor"):
        t="1"
    elif(typ=="clustering"):
        t="2"
    else:
        print("Syntax err: no such ML algorithm "+typ+". Try classifier, regressor or clustering.")
        sys.exit(2)
    N=63*pow(2,num)
    url="http://"+ip+":"+port+"/api/ml_predict_data?N="+str(N)+"&typ="+t

def get_data(): #typ= classifier/regressor/clustering
    global content
    if(typ=="classifier"):
        url_data=url_classifier
    else:
        url_data=url_regressor
    # Save csv file if it doesn't exist
    if(typ=="classifier" or typ=="regressor"):
        data_dir="data"
        file_name=data_dir+"/data_"+typ+".csv"
        if not os.path.isfile(file_name):
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            res = requests.get(url_data, allow_redirects=True)
            open(file_name, 'wb').write(res.content)
    # Read stored csv file or digits
    nlen=63 # limit number of samples
    if(typ=="classifier"):
        cont = pd.read_csv(file_name,header=None)
        cont[60] = np.where(cont[60]=='R',0,1)
        train, test = train_test_split(cont, test_size = 0.3)
        x_test = test.iloc[0:nlen,0:60]
    elif(typ=="regressor"):
        cont = pd.read_csv(file_name,header=0,sep=';')
        train, test = train_test_split(cont, test_size = 0.3)
        x_test = test.iloc[0:nlen,0:11]
    else:
        digits = load_digits()
        data = scale(digits.data)
        x_train, x_test, y_train, y_test, images_train, images_test = train_test_split(
                data, digits.target, digits.images, test_size=0.25, random_state=42)
        x_test = x_test[0:63] # x_test is already an np.ndarray object
    # Concatenate data to increment samples
    for i in range(1,num+1):
            x_test = np.concatenate((x_test,x_test), axis=0) # return an np.ndarray object
    content = x_test

def get_prediction(i=0):
    global content
    timestamp = datetime.datetime.now().timestamp()
    try:
        response = requests.post(url, data = {'upfile': content}) # upfile is the name of the var
    except http.client.HTTPException as e:
        print(e)
    now = datetime.datetime.now().timestamp()
    response_time_ms = (float(now) - float(timestamp))*1000
    return i, response, response_time_ms

def standard_loop():
    for i in range(1,rep+1):
        j, response, response_time_ms = get_prediction()
        print("#"+str(i)+"/"+str(rep)+" Prediction time: {0:.2f} ms for {1} elements. Response time: {2:.2f} ms".format(
            response.json()[0], response.json()[1], response_time_ms)) # response is in json

def parallel_loop():
        t_pred, t_resp = list(), list()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, response, response_time_ms in executor.map(get_prediction, range(1, rep+1)):
                # Create a list() to save the results 
                t_pred.append(response.json()[0])
                t_resp.append(response_time_ms) 
                elem = response.json()[1]
                # Print results
                print("#"+str(i)+"/"+str(rep)+" Prediction time: {0:.2f} ms for {1} elements. Response time: {2:.2f} ms".format(
                    response.json()[0], response.json()[1], response_time_ms)) # response is in json
            return t_pred, t_resp, elem

def save_to_file(obj,type_name):
    # Create dir if it does not exist
    result_dir="results"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    # Save the object to file
    filename = result_dir+"/"+test_name+"-"+type_name+".p"
    pickle.dump(obj, open(filename, 'wb'))
    print(type_name+"\tsaved into -> "+filename)

def start_remote_mon(mon_ip,mon_port,testname):
    url="http://"+mon_ip+":"+mon_port+"/api/start_mon?testname="+testname
    try:
        response = requests.get(url)
    except http.client.HTTPException as e:
        print(e)
    return response.json()

def stop_remote_mon(mon_ip,mon_port,pid):
    url="http://"+mon_ip+":"+mon_port+"/api/stop_mon?pid="+str(pid)
    try:
        response = requests.get(url)
    except http.client.HTTPException as e:
        print(e)
    return str(response.json())

def main():
    get_opts()
    get_data()
    #mon_port = "5001"
    #pid = start_remote_mon(mon_ip,mon_port,test_name)
    print("Sent bytes for each prediction: "+str(sys.getsizeof(content)))
    t_pred, t_resp, elem = parallel_loop()
    save_to_file(t_pred,"tpred-"+str(index)+"-"+str(elem)+"_"+str(rep))
    save_to_file(t_resp,"tresp-"+str(index)+"-"+str(elem)+"_"+str(rep))
    #msg = stop_remote_mon(mon_ip,mon_port,pid)
    #print("Remote monitoring: "+str(msg))

if __name__=="__main__":
    main()