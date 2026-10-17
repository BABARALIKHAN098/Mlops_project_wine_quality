from flask import Flask, render_template, request
import subprocess
import sys
import numpy as np
from src.Mlops_project_quality_predictor.pipeline.prediction_pipeline import PredictionPipeline

# Create the Flask application
app = Flask(__name__, template_folder="template")

# Load the model ONCE when the app starts, instead of on every request
# (loading a model from disk each time is slow)
pipeline = PredictionPipeline()


@app.route("/", methods=["GET"])  # FIX: `methods` (plural) and uppercase "GET"
def homepage():
    """Show the home page with the input form."""
    return render_template("index.html")


@app.route("/train", methods=["GET"])  # FIX: `methods` (plural)
def training():
    """Run the training pipeline by executing main.py."""
    # subprocess.run lets us check whether training actually succeeded
    # sys.executable makes sure the same Python interpreter is used
    result = subprocess.run([sys.executable, "main.py"])

    # returncode 0 means the script finished without errors
    if result.returncode == 0:
        return "Training successful"  # FIX: spelling
    return "Training failed", 500


@app.route("/predict", methods=["POST", "GET"])
def predict_route():  # FIX: clearer name than `index`
    """Take the form values, run the model, and show the prediction."""

    # If the user opens /predict directly (GET), just show the form
    if request.method == "GET":
        return render_template("index.html")

    # Otherwise the form was submitted (POST), so make a prediction
    try:
        # Read each field from the form and convert it to float. The keys must
        # match the name attributes in template/index.html.
        feature_names = [
            "fixed_acidity", "volatile_acidity", "citric_acid",
            "residual_sugar", "chlorides", "free_sulfur_dioxide",
            "total_sulfur_dioxide", "density", "pH", "sulphates", "alcohol",
        ]
        values = [float(request.form[name]) for name in feature_names]

        # Put the values in the same order as the training features
        # and reshape to 2D because scikit-learn expects a row of features.
        data = np.array(values).reshape(1, len(feature_names))

        # FIX: actually call the model's predict method
        # (before, `predict` was an undefined name)
        prediction = pipeline.predict(data)

        # prediction is an array, so take the first value
        return render_template("result.html", prediction=str(prediction[0]), values=request.form)

    except Exception as e:
        print(f"Prediction error: {e}")
        return render_template(
            "index.html",
            error="Please enter a valid number for every field and try again.",
            form_values=request.form,
        ), 400


if __name__ == "__main__":
    # FIX: `port` instead of `post`
    # host="0.0.0.0" makes the app reachable from other machines (needed for Docker/cloud)
    app.run(host="0.0.0.0", port=8080)