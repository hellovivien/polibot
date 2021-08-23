from fastapi import FastAPI
import pickle

app = FastAPI()


@app.get("/{input}")
def predict(input: str):
    tfidf, model = pickle.load(open('model.bin', 'rb'))
    predictions = model.predict(tfidf.transform([input]))
    label = predictions[0]
    return {'text': input, 'label': label}
    

