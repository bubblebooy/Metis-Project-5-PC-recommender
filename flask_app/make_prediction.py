import pickle
# import pandas as pd
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD

from recommender import Recommender

# from autoencoder import create_autoencoder
# autoencoder_model = create_autoencoder(weights = 'autoencoder.h5')

combined = pickle.load(open("combined.plk","rb"))
cleaned = pickle.load(open("cleaned.plk","rb"))

svd = np.load('svd.npy')
tsne = np.load('tsne.npy')
ward_predict = np.load('ward_predict.npy')
k_predict = np.load('k_predict.npy')

scaler_reg = pickle.load(open('scaler_reg.plk',"rb"))
reg_cols = ['GPU Effective Memory Clock Rate','GPU Core Clock Rate','Core Count',
                 'Core Clock','Boost Clock','TDP','L2 Cache','L3 Cache','Lithography',
                 'GB','storage_count','Memory','Power Supply','Video Card_count','Video Card_memory']

# create a function to take in user-entered amounts and apply the model

def cluster_plot(build = None, recommendations = None, plot_type = 'svd', c = 'k_predict'):
    if c == 'ward_predict':
        c = ward_predict
    elif c == 'k_predict':
        c = k_predict
    elif c == 'cpu_clock':
        c = cleaned['Boost Clock']
    elif c == 'cpu':
        c = cleaned['Manufacturer']
    else: #c == 'price'
        c = np.clip(cleaned['price_build'],0,5000)

    build_index = combined['build_url'].reset_index().set_index('build_url')

    if plot_type == 'svd':
        plt.clf()
        plt.scatter(svd[:,0],svd[:,1], c = c, cmap = 'jet')
        plt.xlim(-2.8,10)

        if recommendations is not None:
            index = build_index.loc[recommendations][:10]
            plt.scatter(svd[index,0],svd[index,1], color = (1, .1, .1),marker = 'X', s = 60, edgecolors = 'black')
        if build is not None:
            index = build_index.loc[build]
            plt.scatter(svd[index,0],svd[index,1], color ="red", marker = 'X', s = 120, edgecolors = 'white')


    else:
        plt.clf()
        plt.scatter(tsne[:,0],tsne[:,1], c = c, cmap = 'jet')

        if recommendations is not None:
            index = build_index.loc[recommendations][:10]
            plt.scatter(tsne[index,0],tsne[index,1], color = (1, .1, .1),marker = 'X', s = 60, edgecolors = 'black')
        if build is not None:
            index = build_index.loc[build]
            plt.scatter(tsne[index,0],tsne[index,1], color ="red", marker = 'X', s = 120, edgecolors = 'white')



    plt.savefig('static/cluster_plot.png')

def get_build_list(combined = combined):

    return combined.set_index('build_url')['name_build'].to_dict()

def get_build_details(build, combined = combined):

    return combined.set_index('build_url').loc[build].to_dict()

def get_recommendations(builds, clean = cleaned, svd = None, encoder = False):
    clean = clean.drop_duplicates()
    print(clean)

    preprocessors = [StandardScaler()]
    if svd is not None and svd:
        svd = int(svd)
        svd = min([40,svd])
        preprocessors= [TruncatedSVD(svd)]
        clean[reg_cols] = scaler_reg.transform(clean[reg_cols])

    # if encoder is not None and encoder:
    #     #drop
    #     #scale

    #     predict = autoencoder_model.predict(clean.loc[builds] )

    #     #unscale
    #     #rename and combine columns

    recommender = Recommender(drop_columns = ['Date Published','price_build','number_ratings','avg_rating','storage_price'],
                              preprocessors = preprocessors,
                          # feature_weights = {'Core Clock' : 10},
                         )
    recommender.fit(clean)
    return recommender.recommend(clean.loc[builds])

def price_mask(builds, min = 0, max = np.inf, clean = cleaned):
    clean = clean.drop_duplicates()

    builds = builds[(clean.loc[builds]['price_build'] > min) & (clean.loc[builds]['price_build'] < max)]
    return builds
