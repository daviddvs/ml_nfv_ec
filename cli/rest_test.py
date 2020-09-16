import sys, getopt
import requests
import http
import datetime
import concurrent.futures

rep=10
num=1000
url="http://10.98.1.26:5000/api/ml_predict?N="+str(num)
data=""

def get_prediction(i=0):
    timestamp = datetime.datetime.now().timestamp()
    try:
        response = requests.get(url, data=data)
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