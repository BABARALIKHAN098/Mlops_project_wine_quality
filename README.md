# Wine Quality Prediction

An end-to-end MLOps project that trains an ElasticNet model to estimate the
quality score of red wine from its laboratory measurements. The project
includes a modular training pipeline, model evaluation artifacts, and a Flask
web application for interactive predictions.

## Application preview

### Wine measurement form

Enter the 11 laboratory measurements and submit them to the trained model.

![Wine quality prediction form](<screenshot of projectUi/Screenshot 2026-10-17 230222.png>)

### Prediction result

The application displays the estimated wine quality score after prediction.

![Wine quality prediction result](<screenshot of projectUi/Screenshot 2026-10-17 230315.png>)

## Features

- Red wine quality prediction using an ElasticNet regression model.
- Flask interface for entering wine measurements and viewing predictions.
- Reproducible pipeline stages for ingestion, validation, transformation,
  training, and evaluation.
- Configuration-driven data and artifact paths.
- Saved model, transformed datasets, validation status, and evaluation metrics
  under `artifacts/`.
- Logging for pipeline execution and errors.

## Project structure

```text
.
├── app.py                         # Flask application
├── main.py                        # Training and evaluation pipeline
├── params.yaml                    # Model and training parameters
├── schema.yaml                    # Dataset schema and target definition
├── config/config.yaml             # Data and artifact configuration
├── template/                      # Flask HTML templates
├── src/Mlops_project_quality_predictor/
│   ├── components/                # Pipeline component implementations
│   ├── config/                    # Configuration helpers
│   ├── entity/                    # Configuration entities
│   ├── pipeline/                  # Pipeline orchestration
│   └── utils/                     # Shared utilities and logging
├── artifacts/                     # Generated datasets, model, and metrics
├── research/                      # Exploratory and pipeline notebooks
└── screenshot of projectUi/       # Application screenshots
```

## Input features

The prediction form accepts these 11 measurements:

1. Fixed acidity
2. Volatile acidity
3. Citric acid
4. Residual sugar
5. Chlorides
6. Free sulfur dioxide
7. Total sulfur dioxide
8. Density
9. pH
10. Sulphates
11. Alcohol

The model returns an estimated `quality` score.

## Deploy to Vercel

The Flask prediction application is configured as a Vercel Python serverless
function. The trained model in
`artifacts/model_trainer/model.joblib` is included in the deployment; training
is intentionally kept as a local/offline pipeline because Vercel functions
have ephemeral filesystems and request time limits.

1. Push the repository to GitHub.
2. In [Vercel](https://vercel.com/new), select **Import Git Repository** and
   choose this repository.
3. Keep the repository root as the project root. No build command is required;
   `vercel.json` selects the Python runtime and routes all requests to
   `app.py`.
4. Select **Deploy**. After deployment, open the generated URL and submit the
   prediction form.

The same deployment can be created from the Vercel CLI:

```powershell
npm install --global vercel
vercel
vercel --prod
```

## Getting started

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements-dev.txt
```

`requirements.txt` contains only the runtime dependencies needed by the
prediction application and Vercel. `requirements-dev.txt` adds the training
pipeline and notebook dependencies.

### 3. Run the training pipeline

The pipeline downloads and ingests the dataset, validates the schema,
transforms the data, trains the model, and writes evaluation metrics.

```powershell
python main.py
```

Generated outputs include:

- `artifacts/data_ingestion/winequality-red.csv`
- `artifacts/data_transformation/train.csv`
- `artifacts/data_transformation/test.csv`
- `artifacts/model_trainer/model.joblib`
- `artifacts/model_evaluation/metrics.json`

### 4. Start the prediction web application locally

```powershell
python app.py
```

Open <http://localhost:8080> in a browser. Enter the wine measurements and
select **Predict quality** to receive a prediction.

## API routes

| Route | Method | Description |
| --- | --- | --- |
| `/` | `GET` | Displays the prediction form |
| `/predict` | `GET`, `POST` | Displays the form or predicts wine quality |

## Dataset

The pipeline uses the red wine quality dataset. Its expected columns and types
are defined in [`schema.yaml`](schema.yaml), with `quality` as the target
column.

## License

This project is provided for learning and demonstration purposes.
