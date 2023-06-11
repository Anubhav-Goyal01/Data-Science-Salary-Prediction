from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from src.entity.prediction import CustomData, PredictionPipeline
from src.entity.artifact_entity import ModelTrainerArtifact


MODEL_DIR = "src/artifact/model_trainer"

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        data = CustomData(
        brand=request.form.get('brand'),
        processor_brand=request.form.get('processor_brand'),
        processor_name=request.form.get('processor_name'),
        processor_gnrtn=request.form.get('processor_gnrtn'),
        ram_gb= request.form.get('ram_gb'),
        ram_type=request.form.get('ram_type'),
        ssd=request.form.get('ssd'),
        hdd=request.form.get('hdd'),
        os=request.form.get('os'),
        os_bit=request.form.get('os_bit'),
        graphic_card_gb= request.form.get('graphic_card_gb'),
        weight=request.form.get('weight'),
        warranty=request.form.get('warranty'),
        touchscreen=request.form.get('touchscreen'),
        msoffice=request.form.get('msoffice'),
        rating=request.form.get('rating'),
        num_ratings=int(request.form.get('n_ratings')),
        num_reviews=int(request.form.get('n_reviews'))
        )

        pred_df = data.get_data_as_data_frame()

        prediction_pipeline = PredictionPipeline(model_dir=MODEL_DIR)
        results = prediction_pipeline.predict(pred_df)
        result_string = f"Predicted price of the laptop is: ₹{round(results[0], 2)}"
        return render_template('index.html',results= result_string)



if __name__ == "__main__":
    app.run(debug= True)