## MLflow

### To run the server for development
```bash
# must set default-artifact-root when setting --no-server-artifacts
docker run --rm -it -v $PWD/mlflow:/mlflow --network=host 'radiasoft/mlops' bash -c 'cd /mlflow/db && MLFLOW_AUTH_CONFIG_PATH=/mlflow/basic-auth.ini mlflow server --host 0.0.0.0 --port 8080 --app-name basic-auth --backend-store-uri "sqlite:///backend-store.db" --no-serve-artifacts --default-artifact-root /mlflow/db'

```

### Basics
Try the example notebook [from the mlflow website](https://mlflow.org/docs/latest/getting-started/intro-quickstart/notebooks/index.html) to get a basic idea of experiment tracking with mlflow.


### MLflow server
Under the workding directory where the mlflow server is started it creates a variety of directories (mlartifacts, mlruns, etc.). These are the db for the server.

`mlflow server --host 0.0.0.0 --port 8080'` # This is the mlflow "tracking server" https://mlflow.org/docs/latest/tracking/server.html

`--backend-store-uri` # This is where experiment and run metadata are stored. Things like params used for tuning. This data is "small" (can be stored in a sql db). For us something like `sqlite:///backend-store.sqlite` is probably sufficient to start.
https://mlflow.org/docs/latest/tracking/server.html#backend-store

`--default-artifact-root` # This is a default uri one can set for where artifacts are logged. The mlflow docs are pretty confusing about what this is actually setting and whether or not it makes sense for our use case. From testing, it seems to not be needed. Since we have `--serve-artifacts` set (the default) mlflow automatically uses the `mlflow-artifacts:/` uri root which I think is what we want. It then stores the artifacts on the local filesystem where the server is running.
https://mlflow.org/docs/latest/tracking/artifacts-stores.html#setting-a-default-artifact-location-for-logging This doc says the path will be set to a path in the local filesystem (where the ml is running). In practice I haven't found this to be true. It is only true when tracking_uri is NOT set which isn't the case for us.



`--artifacts-destination` # This configures the backend where artifacts are stored. Requests for artifacts are then proxied through the tracking server to this destination (ex `s3://my-bucket`). The default is to use the local filesystem which is probably sufficient for us to start.
In client code they can say `mlflow-artifacts:/` which resolves to the backend location (ex `s3://my-bucket`). This allows clients to not have to hardcode paths that may change in the future.
https://mlflow.org/docs/latest/tracking/server.html#using-the-tracking-server-for-proxied-artifact-access

`--no-serve-artifacts --default-artifact-root` # This configures the tracking server to not proxy artifacts. Instead clients connect to the tracking server just to recieve the url of the artifact root. Then they directly connect to the artifact root. Probably not necessary for us to start but may be useful if there is slowness in the future.
https://mlflow.org/docs/latest/tracking/server.html#use-tracking-server-w-o-proxying-artifacts-access



Security:
https://mlflow.org/docs/latest/tracking/server.html#tracking-auth
People recommend running a different instance of mlflow for each "team" https://github.com/mlflow/mlflow/issues/724#issuecomment-1476673236 . There current permissions model doesn't allow specifying anything like a "group" for a user so they can only access a certain set of experiments. Also, https://www.reddit.com/r/mlops/comments/11zldyz/how_do_you_handle_auth_permissions_for_mlflow/.
There auth model does allow specifying perms on a per experiment basis. So, we could have an admin create all experiments and then give a set of users access to them. The downside is that users will need to go through an admin to create new experiments. A bit clunky but maybe that would work to allow users from different projects to share one tracking server. The other downside is that the artifact store will have the same path. So, if we wanted to mount the artifact store to something like jupyter we would have to manage mounts on a per user/experiment basis which would be painful (ex give user1 access to experiment a, b, c and give user2 access to experiment a, x, y). We could write scripts to manage this work https://mlflow.org/docs/latest/auth/index.html#managing-permissions


### Auth
The MLflow server can be configured with basic-auth (`--app-name basic-auth`).

You can create a configuration file to setup auth defaults (ex admin user/pass) https://mlflow.org/docs/latest/auth/index.html#configuration. You can specify the path to this by supplying `$MLFLOW_AUTH_CONFIG_PATH` when starting the server.

Users will need to create a credentials file with their username/password https://mlflow.org/docs/latest/auth/index.html#using-credentials-file

Admins need to first create users. This can be done by visiting http://<tracking_url>/signup or by generating them using a python script https://mlflow.org/docs/latest/auth/index.html#managing-permissions


### MLflow Projects
These are akin to virtualenv's that let you package up a project so it can be reproduced elsewhere. They aren't for grouping experiments as one might think.
