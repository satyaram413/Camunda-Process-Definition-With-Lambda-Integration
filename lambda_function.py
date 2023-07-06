import json
import urllib.parse
import boto3
import pickle
import numpy as np
import logging

print('Loading function')

s3 = boto3.resource('s3')

def predict(model_load, data):
    int_features = [x for x in data.values()]
    print("reached here")
    final_features = [np.array(int_features)]
    output = model_load.predict(final_features).tolist()
    if output == [1]:
        response_data =  'Customer will go'
    elif output == [0]:
        response_data = 'Customer will stay'
    else:
        response_data = 'Unknown'
    
    return response_data

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = "machine-learning-models-automation"
    key="rf_model.pkl"
    try:
        model=pickle.loads(s3.Bucket(bucket).Object(key).get()['Body'].read())
        data = event['data']
        print(data)
        return predict(model,data)
    except Exception as e:
        logging.error(str(e))
        return
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

