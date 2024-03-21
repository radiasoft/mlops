from pykern.pkcollections import PKDict
from pykern.pkdebug import pkdlog
import mlflow.server.auth.client

u = mlflow.server.auth.client.AuthServiceClient("http://127.0.0.1:8080").get_user(
    "admin"
)
pkdlog(
    "user_details=",
    PKDict(
        user_id=u.id,
        username=u.username,
        password_hash=u.password_hash,
        is_admin=u.is_admin,
    ),
)
