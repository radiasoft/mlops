from pykern.pkdebug import pkdlog
import mlflow

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
pkdlog("Artifact uri: {}", mlflow.get_artifact_uri())
pkdlog(
    "Artifact uri with path: {}",
    mlflow.get_artifact_uri(artifact_path="features/features.txt"),
)
