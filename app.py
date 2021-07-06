import json
import boto3
import numpy as np
import PIL.Image as Image
import tensorflow as tf

s3 = boto3.resource('s3')
client_s3 = boto3.client('s3')
result = client_s3.download_file("dsikar.models.bucket",'firemodel.h5', "/tmp/firemodel.h5")
model = tf.keras.models.load_model('/tmp/firemodel.h5')
plot_size = 64
IMAGE_SHAPE = (plot_size, plot_size)
CATEGORIES = ['nofire', 'fire']

def lambda_handler(event, context):
  bucket_name = event['Records'][0]['s3']['bucket']['name']
  key = event['Records'][0]['s3']['object']['key']
  img = readImageFromBucket(key, bucket_name).resize(IMAGE_SHAPE)
  img = np.array(img)/255.0
  prediction = model.predict(np.expand_dims(img, axis=0))[0]
  predicted_class = CATEGORIES[np.argmax(prediction)] 
  print('ImageName: {0}, Prediction: {1}'.format(key, predicted_class))
  response_str = 'ImageName: {0}, Prediction: {1}'.format(key, predicted_class)
  filename = key + '.txt'
  client_s3.put_object(Body=response_str, Bucket='tensorflow-images-predictions-dsikar', Key=filename)

def readImageFromBucket(key, bucket_name):
  bucket = s3.Bucket(bucket_name)
  object = bucket.Object(key)
  response = object.get()
  return Image.open(response['Body']) 
