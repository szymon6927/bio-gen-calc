import os
import secrets

import joblib
from flask import current_app
from werkzeug.utils import secure_filename

from app.ampc.config import AMPC_MODELS_UPLOAD_PATH


class Model:
    @staticmethod
    def export_model(id, model_key, model_type, model):
        random_hex = secrets.token_hex(4)
        filename = f"{id}_{random_hex}_{model_type}_{secure_filename(model_key)}"

        path = os.path.join(current_app.root_path, AMPC_MODELS_UPLOAD_PATH, filename)
        joblib.dump(model, path)

        return filename
