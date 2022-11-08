from youtubesearchpython import Video, ResultMode
from colors import colorOf, dataset

import numpy as np
import matplotlib.pyplot as plt
import requests
import pickle
import warnings
warnings.filterwarnings("ignore")

def predictCategoryFor(url):
    try:

        video = Video.getInfo(url, mode = ResultMode.json)

        text = [video["title"] + " " + video["description"]]
        
        categories = sorted(list(dataset.keys()))

        education_model = pickle.load(open("./models/educated_model.pkl", "rb"))
        education_prediction = education_model.predict(text)[0]

        if education_prediction == 0:
            
            category_classifier = pickle.load(open("./models/cat_model.pkl", "rb"))
            category_prediction = categories[category_classifier.predict(text)[0]]
            
            sub_cat_clf = pickle.load(open(f"./models/{category_prediction.lower().replace(' ', '_')}_model.pkl", "rb"))
            sub_cat_pred = sub_cat_clf.predict_proba(text)[0]
            sub_cat_pred *= 100
            subs = sorted(dataset[category_prediction])

            return ("Educational", category_prediction, subs, sub_cat_pred)
        
        else:

            return ("Non Educational", "", [], [])
    
    except:
        return ("There must be an error in getting the title and description of the video.", "", [], [])


# print(predictCategoryFor(url="https://www.youtube.com/watch?v=bdCX8Nb_2Mg"))

