import tensorflow as tf
import keras
import numpy as np
import pandas as pd
import random
import os.path
from datetime import datetime
import time
class FarmNetModel(object):
    BASE = os.path.dirname(os.path.abspath(__file__))
    TRAINING_SET_URI = '/Users/sidrajaram/Downloads/Machine_1.csv'
    KEY_FACTORS = ['FUEL_RATE', 'ENGINE_SPEED', 'ENGINE_LOAD', 'ENGINE_COOLANT_TEMP', 'SCR_TANK_LEVEL']
    training_dataset = None
    loaded_model = None
    training_features = None
    training_labels = None
    @staticmethod
    def initialize_model(file_url=TRAINING_SET_URI):
        FarmNetModel.training_dataset = FarmNetModel.generate_train_test_set(file_url)
        FarmNetModel.loaded_model = FarmNetModel.generate_model()
    @staticmethod
    def generate_model():
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=[len(FarmNetModel.training_features.keys())]),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(1)
        ])
        optimizer = keras.optimizers.RMSprop(0.001)
        model.compile(loss='mse',
                      optimizer=optimizer,
                      metrics=['mae', 'mse'])
        history = model.fit(
            FarmNetModel.training_features, FarmNetModel.training_labels,
            epochs=1000, validation_split=0.2, verbose=0)
        return model
    @staticmethod
    def predict(data):
        test_predictions = FarmNetModel.loaded_model.predict(data).flatten()
        print(test_predictions)
    @staticmethod
    def generate_train_test_set(URI=TRAINING_SET_URI):
        # THIS IS THE MAIN SAUCE
        tuples = FarmNetModel.generate_raw_tuples(URI)
        timestamps = []
        lats = []
        lngs = []
        engine_speed = []
        for tuple in tuples:
            timestamps.append(tuple[0][0])
            lats.append(tuple[0][1])
            lngs.append(tuple[0][2])
            engine_speed.append(tuple[1][1])
        for timestamp in timestamps:
            s = timestamp
        dataset = pd.DataFrame({"timestamp":timestamps,
                                "latitude":lats,
                                "longitude":lngs,
                                "engine_speed":engine_speed})
        print(dataset)
        train_dataset = dataset.sample(frac=0.8, random_state=0)
        test_dataset = dataset.drop(train_dataset.index)
        train_stats = train_dataset.describe()
        train_stats.pop("engine_speed")
        train_stats = train_stats.transpose()
        train_labels = train_dataset.pop('engine_speed')
        FarmNetModel.training_labels = train_labels
        test_labels = test_dataset.pop('engine_speed')
        normed_train_data = (train_dataset - train_stats['mean']) / train_stats['std']
        FarmNetModel.training_features = normed_train_data
        normed_test_data = (test_dataset - train_stats['mean']) / train_stats['std']
        return
    @staticmethod
    def generate_raw_tuples(URI=TRAINING_SET_URI):
        df = pd.read_csv(URI, encoding='latin1')
        new_df = df.loc[df['can_name'].isin(FarmNetModel.KEY_FACTORS)]
        # df.drop(['can_id', 'equipment', 'can_value'], axis = 1, inplace = True)
        # print(df.columns.values)
        # df[df['can_name'] == 'FUEL_']
        counts = {}
        timestamp = new_df['timestamp'][0]
        data_for_timestamp = {}
        intermediate_valid_data = {}
        master_dict = {}
        valid_times = []
        data_raw = []
        for index, row in new_df.iterrows():
            current_timestamp = row['timestamp']
            current_can_name = row['can_name']
            current_can_value = row['can_value']
            current_lat = row['latitude']
            current_lng = row['longitude']
            data_for_timestamp[current_can_name] = {'count': 1, 'value': current_can_value}
            if (current_timestamp == timestamp):
                try:
                    data_for_timestamp[current_can_name]['count'] = 1
                except KeyError:
                    pass
            else:
                print(data_for_timestamp)
                sum = 0
                for key in FarmNetModel.KEY_FACTORS:
                    try:
                        if data_for_timestamp[key]['count'] == 1:
                            intermediate_valid_data[key] = data_for_timestamp[key]['value']
                            # print(intermediate_valid_data[key])
                            sum += data_for_timestamp[key]['count']
                            # print(sum)
                    except KeyError:
                        break
                if sum == 5:
                    valid_times.append(timestamp)
                    data_row = list(intermediate_valid_data.values())
                    # print(data_row)
                    data_row.insert(0, timestamp)
                    data_row.insert(1, current_lat)
                    data_row.insert(2, current_lng)
                    data_raw.append(data_row)
                counts = {}
                timestamp = current_timestamp
                data_for_timestamp = {}
                data_for_timestamp[current_can_name] = {'count': 1, 'value': current_can_value}
                try:
                    data_for_timestamp[current_can_name]['count'] = 1
                except KeyError:
                    pass
        sampled_data_raw = random.sample(data_raw, k=100)
        sample_data_tuples = []
        for sample in sampled_data_raw:
            sample_data_tuples.append((sample[:3], sample[3:]))
        count = 0
        for tuple in sample_data_tuples:
            if count >= 10:
                break
            print(tuple[0], tuple[1])
            count += 1
        return sample_data_tuples
