import pickle
import numpy
from models import *
from sklearn.preprocessing import OneHotEncoder
import sys
sys.setrecursionlimit(10000)


def sample(X, y, n):
    '''random samples'''
    num_row = X.shape[0]
    indices = numpy.random.randint(num_row, size=n)
    return X[indices, :], y[indices]


def evaluate_models(models, X, y):
    assert(min(y) > 0)
    guessed_sales = numpy.array([model.guess(X) for model in models])
    mean_sales = guessed_sales.mean(axis=0)
    relative_err = numpy.absolute((y - mean_sales) / y)
    result = numpy.sum(relative_err) / len(y)
    return result


# start
numpy.random.seed(123)
train_ratio = 0.9
shuffle_data = False
one_hot_as_input = False

embeddings_as_input = False

# set save_embeddings to True to create this file
save_embeddings = True
saved_embeddings_fname = "embeddings.pickle"

(X, y) = pickle.load(open('feature_train_data.pickle', 'rb'))
num_records = len(X)
train_size = int(train_ratio * num_records)

if shuffle_data:
    print("Using shuffled data")
    sh = numpy.arange(X.shape[0])
    numpy.random.shuffle(sh)
    X = X[sh]
    y = y[sh]

if embeddings_as_input:
    print("Using learned embeddings as input")
    X = embed_features(X, saved_embeddings_fname)

if one_hot_as_input:
    print("Using one-hot encoding as input")
    enc = OneHotEncoder(sparse=False)
    enc.fit(X)
    X = enc.transform(X)


X_train = X[:train_size]
X_val = X[train_size:]
y_train = y[:train_size]
y_val = y[train_size:]

# Simulate data sparsity
X_train, y_train = sample(X_train, y_train, 200000)
print("Number of samples used for training: " + str(y_train.shape[0]))

models = []
N_MODEL = 1

print("Fitting NN_with_EntityEmbedding...")
for i in range(N_MODEL):
    models.append(NN_with_EntityEmbedding(X_train, y_train, X_val, y_val))

# TODO: bug
# print("Fitting NN...")
# for i in range(5):
#     models.append(NN(X_train, y_train, X_val, y_val))

print("Fitting RF...around 1.5min")
# models.append(RF(X_train, y_train, X_val, y_val))

print("Fitting KNN...fast")
# models.append(KNN(X_train, y_train, X_val, y_val))

print("Fitting XGBoost...iterative")
# models.append(XGBoost(X_train, y_train, X_val, y_val))

#TODO: no in report, taking too long 5min no print log
print("Fitting SVM...")
# models.append(SVM(X_train, y_train, X_val, y_val))

# Turn on if using NN-with-embedding
if save_embeddings:
    model = models[0].model
    store_embedding = model.get_layer('store_embedding').get_weights()[0]
    dow_embedding = model.get_layer('dow_embedding').get_weights()[0]
    year_embedding = model.get_layer('year_embedding').get_weights()[0]
    month_embedding = model.get_layer('month_embedding').get_weights()[0]
    day_embedding = model.get_layer('day_embedding').get_weights()[0]
    german_states_embedding = model.get_layer('state_embedding').get_weights()[0]
    
    with open(saved_embeddings_fname, 'wb') as f:
        pickle.dump([store_embedding, dow_embedding, year_embedding,
                     month_embedding, day_embedding, german_states_embedding], f, -1)

print("Evaluate combined models...")
print("Training error...")
r_train = evaluate_models(models, X_train, y_train)
print(r_train)

print("Validation error...")
r_val = evaluate_models(models, X_val, y_val)
print(r_val)
