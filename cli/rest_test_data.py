import sys, getopt
import requests
import http
import datetime
import concurrent.futures

rep=10
num=100
url="http://10.98.1.26:5000/api/ml_predict_data?N="+str(num)
data=""

def get_data():
    url_data="https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
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

#standard_loop()
parallel_loop()
#get_data()