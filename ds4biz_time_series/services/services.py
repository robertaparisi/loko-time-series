import re
import traceback

from sanic import Sanic, Blueprint
from sanic_openapi import swagger_blueprint
from sanic_openapi.openapi2 import doc
from sanic_cors import CORS
from urllib.parse import unquote
from pathlib import Path

# app = Sanic("res")
# swagger_blueprint.url_prefix = "/api"
# app.blueprint(swagger_blueprint)
from ds4biz_time_series.config.AppConfig import REPO_PATH
from ds4biz_time_series.utils.logger_utils import logger
from ds4biz_time_series.utils.ppom_utils import get_pom_major_minor
from sanic.exceptions import SanicException, NotFound

import sanic

from ds4biz_time_series.utils.serialization_utils import serialize

repo_path = Path(REPO_PATH)

def get_app(name):
    app = Sanic(name)
    swagger_blueprint.url_prefix = "/api"
    app.blueprint(swagger_blueprint)
    return app

name = "time_series"
app = get_app(name)
bp = Blueprint("default", url_prefix=f"ds4biz/time_series/{get_pom_major_minor()}")
app.config["API_VERSION"] = get_pom_major_minor()
app.config["API_TITLE"] = name
# app.config["REQUEST_MAX_SIZE"] = 20000000000 ## POI TOGLIERE!!
CORS(app)


@bp.post("/transformers/<name>")
@doc.tag('transformers')
@doc.summary("Save an object in 'transformers'")
@doc.description('''
    Examples
    --------
    obj = {"__klass__": "ds4biz.ct", "transformers": {"text": {"__klass__": "sk.HashingVectorizer"}}}
    obj = {
          "__klass__": "ds4biz.ct",
          "transformers": {
            "text": {
              "__klass__": "sk.TfidfVectorizer",
              "ngram_range": [
                1,
                2
              ],
              "max_df": 0.9,
              "min_df": 0.01
            }
          }
        }
    # "text" is the column name!

    obj = {"__klass__": "sk.ColumnTransformer", 
                "transformers": [["cat", {"__klass__": "sk.Pipeline",
                            "steps": [["imputer", {"__klass__": "sk.SimpleImputer",
                                                   "strategy": "most_frequent"}],
                                      ["onehot", {"__klass__": "sk.OneHotEncoder",
                                                  "handle_unknown": "ignore"}]]},
                  ["contratto_presente", "tipologia_documento"]],
                  ["text_0", {"__klass__": "sk.Pipeline",
                             "steps": [["tfidf", {"__klass__": "sk.TfidfVectorizer",
                                                  "max_features": 100}]]},
                  "testo_breve"],
                  ["num", {"__klass__": "sk.Pipeline",
                          "steps": [["normalizer", {"__klass__": "sk.StandardScaler"}],
                                    ["imputer", {"__klass__": "sk.KNNImputer"}]]},
                  ["gross_value_computed", "net_price_computer", "quantity"]]]}
                  ''')
@doc.consumes(doc.JsonBody({}), location="body")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def create_transformer(request, name):
    name = unquote(name)

    if not re.search(r'(?i)^[a-z0-9]([a-z0-9_]*[a-z0-9])?$', name):
        raise SanicException('No special characters (except _ in the middle of name) and whitespaces allowed',
                             status_code=400)

    path = repo_path / 'transformers' / name
    path.mkdir(exist_ok=True)
    serialize(path, request.json)
    return sanic.json(f'Transformer "{name}" saved')

@app.post("/fit")
@doc.summary('Fit an existing predictor')
@doc.consumes(doc.Integer(name="forecasting_window"), location="path", required=True)
async def fit(request):
    return "fit"

@app.post("/predict")
@doc.summary('Use an existing predictor')
async def predict(request):
    return "predict"


@app.post("/evaluate")
@doc.summary('Evaluate existing predictors in history')
async def evaluate(request):
    return "evaluate"

@app.exception(Exception)
async def manage_exception(request, exception):
    if isinstance(exception, SanicException):
        print(dict(error=str(exception)))
        return sanic.json(dict(error=str(exception)), status=exception.status_code)

    e = dict(error=f'{exception.__class__.__name__}: {exception}')
    if isinstance(exception, NotFound):
        return sanic.json(e, status=404)
    status_code = exception.status_code or 500
    logger.error('TracebackERROR: \n' + traceback.format_exc() + '\n\n', exc_info=True)
    return sanic.json(e, status=status_code)


app.blueprint(bp)

app.run("0.0.0.0", port=8087, auto_reload=True)