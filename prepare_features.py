import pickle
from datetime import datetime
from sklearn import preprocessing
import numpy as np
import random
random.seed(42)

with open('train_data.pickle', 'rb') as f:
    train_data = pickle.load(f)
    num_records = len(train_data)
with open('store_data.pickle', 'rb') as f:
    store_data = pickle.load(f)


def feature_list(record):
    dt = datetime.strptime(record['Date'], '%Y-%m-%d')
    store_index = int(record['Store'])
    year = dt.year
    month = dt.month
    day = dt.day
    day_of_week = int(record['DayOfWeek'])
    try:
        store_open = int(record['Open'])
    except:
        store_open = 1

    promo = int(record['Promo'])

    return [
        store_open,
        store_index,# cat feature
        day_of_week,
        promo,
        year,
        month,
        day,
        store_data[store_index - 1]['State'] # cat feature
    ]


train_data_X = []
train_data_y = []
for record in train_data:
    if record['Sales'] != '0' and record['Open'] != '':
        # get feature
        fl = feature_list(record)
        train_data_X.append(fl)
        train_data_y.append(int(record['Sales']))

print("Number of train datapoints: ", len(train_data_y))
print(f"min-y :{min(train_data_y)} max-y: {max(train_data_y)}")


full_X = np.array(train_data_X)
train_data_X = np.array(train_data_X)

# LabelEncoder for each column !!??
les = []
for i in range(train_data_X.shape[1]):
    le = preprocessing.LabelEncoder()
    # full data
    le.fit(full_X[:, i])
    les.append(le)
    train_data_X[:, i] = le.transform(train_data_X[:, i])

with open('les.pickle', 'wb') as f:
    pickle.dump(les, f, -1)

print(f"{train_data_X.shape[1]} col label encoded.")

train_data_X = train_data_X.astype(int)
train_data_y = np.array(train_data_y)

with open('feature_train_data.pickle', 'wb') as f:
    # object, file, protocol
    pickle.dump(
        (train_data_X, train_data_y), 
        f, -1)
    
    print('features: 1.store_open, 2.store_index, 3.day_of_week, 4.promo, 5.year, 6.month, 7.day, 8. state')

    print('first X and y:')
    print(train_data_X[0], train_data_y[0])
