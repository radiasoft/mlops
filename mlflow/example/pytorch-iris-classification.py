"""Pytorch neural network to classify iris species with mlflow logging

Adapted from https://www.kaggle.com/code/mohitchaitanya/simple-iris-dataset-classification-using-pytorch/notebook
"""
from pykern.pkcollections import PKDict
from pykern.pkdebug import pkdlog
import mlflow
import numpy
import pandas
import sklearn.model_selection
import sklearn.preprocessing
import torch
import torch.nn


class NeuralNetworkClassificationModel(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.input_layer = torch.nn.Linear(input_dim, 128)
        self.hidden_layer1 = torch.nn.Linear(128, 64)
        self.output_layer = torch.nn.Linear(64, output_dim)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        out = self.relu(self.input_layer(x))
        out = self.relu(self.hidden_layer1(out))
        out = self.output_layer(out)
        return out


def get_accuracy_multiclass(predicted, original):
    p = predicted.numpy()
    o = original.numpy()
    r = []
    for i in range(len(p)):
        r.append(numpy.argmax(p[i]))
    r = numpy.array(r)
    c = 0
    for i in range(len(o)):
        if r[i] == o[i]:
            c += 1
    return c / len(r)


def get_scaled_data_as_tensors():
    d = pandas.read_csv("./iris.csv", index_col=0)
    # Map iris species name to numerical id's
    d["Species"] = d["Species"].map(
        {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}
    )
    # Split train and test data
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        d.drop(["Species"], axis=1).values,
        d["Species"].values,
        test_size=0.30,
        random_state=42,
    )

    # Scale the data
    s = sklearn.preprocessing.StandardScaler()
    X_train = s.fit_transform(X_train)
    X_test = s.transform(X_test)

    # Convert from ndarray to Torch Tensor
    return (
        torch.FloatTensor(X_train),
        torch.FloatTensor(X_test),
        torch.LongTensor(y_train),
        torch.LongTensor(y_test),
    )


def main():
    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    mlflow.set_experiment("Iris Classification")
    with mlflow.start_run():
        # 4 inputs (sepal_length, sepal_width, petal_length, petal_width)
        # 3 output types (setosa, versicolor and virginica)
        m = NeuralNetworkClassificationModel(4, 3)

        p = PKDict(
            criterion=torch.nn.CrossEntropyLoss(),
            learning_rate=0.02,
            num_epochs=1000,
        )
        p.pkupdate(optimizer=torch.optim.Adam(m.parameters(), lr=p.learning_rate))
        # Log the parameters used
        mlflow.log_params(p)
        X_train, X_test, y_train, y_test = get_scaled_data_as_tensors()
        train_network(
            m,
            p.optimizer,
            p.criterion,
            p.num_epochs,
            X_train,
            y_train,
        )
        with torch.no_grad():
            for n, p, a in (
                ("Training", X_train, y_train),
                ("Testing", X_test, y_test),
            ):
                t = f"{n} Accuracy"
                r = round(get_accuracy_multiclass(m(p), a) * 100, 3)
                # Log the accuracy of the model
                mlflow.log_metric(t, r)
                pkdlog(f"{t}: {r}")


def train_network(
    model,
    optimizer,
    criterion,
    num_epochs,
    X_train,
    y_train,
):
    for _ in range(num_epochs):
        optimizer.zero_grad()
        l = criterion(model(X_train), y_train)
        l.backward()
        optimizer.step()


main()
