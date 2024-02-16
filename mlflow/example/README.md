### Using mlflow with pytorch

`pytorch-iris-classification.py` is an example script to show the
basics of working with mlflow and pytorch.

In order to run the example you will need run the mlflow tracking server.
In production this will be a service run by the software team. For this
example you can run it yourself:
```bash
pip install mlflow
mlflow server --host 0.0.0.0 --port 8080
```

The important pieces of `pytorch-iris-classification.py` are the uses of
mlflow. Here is an overview of the pieces:

- `mlflow.set_tracking_uri`: Establish a connection with the mlflow
server (aka "Tracking Server"). Logged values will be stored on this
server.
- `mlflow.set_experiment`: Set a name for the experiment. An experiment
will be created on the tracking server if one with this name doesn't
already exist.
- `with mlflow.start_run`: Start an mlflow "run". An experiment can
contain zero or more runs. A run is one pass of training a model.
Within a run you can log things like the parameters  used for training
and accuracy metrics.
- `mlflow.log_params`: Log the parameters used for training the model
to the mlflow server.
- `mlflow.log_metric`: Log the accuracy metric of the model to the
mlflow server.


For more in-depth information on mlflow their docs are your best
resource https://mlflow.org/docs/latest/index.html.
