from youtubesearchpython import Transcript, Video, ResultMode
import pickle
from stqdm import stqdm

def eduContentPrediction(url):
    segments = Transcript.get(url)["segments"]
    E = 0
    NonE = 0
    education_model = pickle.load(open("./models/educated_model.pkl", "rb"))

    timer = stqdm(segments)

    for segment in timer:
        timer.set_description("☕️ Have a coffee, while we apply our model on the video transcript.  ")
        text = [str(segment["text"])]
        text_prediction = education_model.predict(text)[0]
        if text_prediction == 0:
            E += 1
        else:
            NonE += 1

    return "The {:.2f}% portion of this video is educational.".format(E*100/(E+NonE))

# print(educationRange("https://www.youtube.com/watch?v=OTuph9pJWU4"))