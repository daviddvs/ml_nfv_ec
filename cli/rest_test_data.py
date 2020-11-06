import sys, getopt
import requests
import http
import datetime
import concurrent.futures

ip="10.98.1.26"
data=""
url_classifier="https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
url_regressor="http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"


def get_opts():
    global typ, num, rep, url # declare global vars
    typ="classifier"
    num=1 
    rep=1
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ht:n:r:",["help","typ=","num=","rep="])
    except getopt.GetoptError:
        print('Bad syntax err: rest_test_data.py -t <type_of_algorithm> -n <number_of_prediction_elem> -r <repetitions>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('rest_test_data.py') 
            print('Options:')
            print('\t-h : display this menu.')
            print('\t-n <number_of_prediction_elements>: set the number of elements (default 1) to predict.'+ 
                    ' 63*n for classifier and 480*n for regressor.')
            print('\t-r <number_of_repetitions>: set the number of repetitios (default 1) to predict.')
            print('\t-t <type_of_algorithm>: set the algorithm to classifier/regressor.')
            sys.exit()
        elif opt in ("-n", "--num"):
            num = int(arg)
        elif opt in ("-r", "--rep"):
            rep = int(arg)
        elif opt in ("-t", "--typ"):
            typ = str(arg)
    print("Algorithm: "+typ)
    if(typ=="regressor"):
        t="1"
    else:
        t="0"
    url="http://"+ip+":5000/api/ml_predict_data?N="+str(num)+"&typ="+t


def get_data(): #typ= classifier, regressor
    if(typ=="classifier"):
        url_data=url_classifier
    elif (typ=="regressor"):
        url_data=url_regressor
    else:
        print("Bad syntax err: no such ML algorithm. Try classifier or regressor.")
        sys.exit(2)
    res = requests.get(url_data, allow_redirects=True)
    content = res.content
    return content

def get_prediction(i=0):
    content = get_data()
    timestamp = datetime.datetime.now().timestamp()
    try:
        response = requests.post(url, files = {'upfile': content}) # upfile is the name of the var
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
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, response, response_time_ms in executor.map(get_prediction, range(1, rep+1)):
                print("#"+str(i)+"/"+str(rep)+" Prediction time: {0:.2f} ms for {1} elements. Response time: {2:.2f} ms".format(
                    response.json()[0], response.json()[1], response_time_ms)) # response is in json
get_opts()
#standard_loop()
parallel_loop()
#get_data()