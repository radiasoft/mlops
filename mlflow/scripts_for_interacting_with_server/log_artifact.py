import mlflow

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
with open("features.txt", "w") as f:
    f.write("rooms, zipcode, median_price, school_rating, transport")
with mlflow.start_run():
    mlflow.log_artifact("features.txt", artifact_path="features")
