from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

import pickle
import numpy as np
import pandas as pd 
import os
import json

import warnings
warnings.filterwarnings("ignore")


model_file = "/mnt/ml/models/models.p"

# Load all the model artifacts 
loaded_model_artifacts = pickle.load(open(model_file, 'rb'))
knn = loaded_model_artifacts['svmp']
scaler = loaded_model_artifacts['norma']
lookup_genre_name = loaded_model_artifacts['lgn']
wav_file_hash = loaded_model_artifacts['wav_file_hash']
df_music_features = loaded_model_artifacts['df_music_features']

# Get the music features
def get_np_song(song_name):
    
    np_song = df_music_features.iloc[wav_file_hash[song_name]]
    
    return np_song
    
    

# Lambda handler code
def lambda_handler(event, context):
    
    # Reading the song name 
    body = json.loads(event['body'])
    song_name = body["song_name"]
    
    print("**********")
    print(body)
    print(song_name)
    print("**********")    
    # Fetching the song features and saving it in a Numpy array
    np_song = get_np_song(song_name)
    np_song = np.array(np_song[1:])
    np_song_scaled = scaler.transform([np_song])

    print("**********")    
    print("np_song")
    print("**********")    

    
    # Performing the prediction 
    genre_prediction = knn.predict(np_song_scaled)
    prediction = lookup_genre_name[genre_prediction[0]]
    
    print(prediction)
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_label": prediction,
            }
        )
    }