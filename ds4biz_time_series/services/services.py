import io
import re
import shutil
import time
import traceback
from http.cookiejar import request_path

import numpy as np
import pandas as pd
from sanic import Sanic, Blueprint
from sanic_openapi import swagger_blueprint
from sanic_openapi.openapi2 import doc
from sanic_cors import CORS
from urllib.parse import unquote
from pathlib import Path
from sanic.response import raw

# app = Sanic("res")
# swagger_blueprint.url_prefix = "/api"
# app.blueprint(swagger_blueprint)
from ds4biz_time_series.business.training import training_pipeline
from ds4biz_time_series.config.AppConfig import REPO_PATH
from ds4biz_time_series.config.factory_config import FACTORY
from ds4biz_time_series.dao.fs_dao import JSONFSDAO
from ds4biz_time_series.utils.core_utils import load_pipeline, to_dataframe
from ds4biz_time_series.utils.data_utils import preprocessing_data
from ds4biz_time_series.utils.logger_utils import logger
from ds4biz_time_series.utils.ppom_utils import get_pom_major_minor
from sanic.exceptions import SanicException, NotFound

import sanic

from ds4biz_time_series.utils.service_utils import check_predictor_existence, load_params, check_existence
from ds4biz_time_series.utils.serialization_utils import serialize, deserialize
from ds4biz_time_series.utils.service_utils import get_all
from ds4biz_time_series.utils.zip_utils import make_zipfile, import_zipfile

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


### TRANSFORMERS ###

@bp.get("/transformers")
@doc.tag('transformers')
@doc.summary("List objects in 'transformers'")
async def list_transformers(request):
    print("si")
    res = get_all('transformers')
    # save_defaults(repo='transformers')
    return sanic.json(res)


@bp.post("/transformers/<name>")
@doc.tag('transformers')
@doc.summary("Save an object in 'transformers'")
@doc.description('''
    Examples
    --------
    Example 1: 
    obj = {
      "__klass__": "skt.TransformerPipeline",
      "steps": [
         {
          "__klass__": "skt.ExponentTransformer",
          "power":2
        }
      ]
    }
    ~~~~~~~~~
    Example 2: 
    obj = {
      "__klass__": "skt.TransformerPipeline",
      "steps": [
        {
          "__klass__": "skt.Deseasonalizer",
          "model": "multiplicative",
          "sp": 12
        },
         {
          "__klass__": "skt.Deseasonalizer",
          "model": "additive",
          "sp": 3
        }
      ]
    }
    --------
                  ''')
@doc.consumes(doc.JsonBody({}), location="body")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def create_transformer(request, name):
    name = unquote(name)

    if not re.search(r'(?i)^[a-z0-9]([a-z0-9_]*[a-z0-9])?$', name):
        raise SanicException('No special characters (except _ in the middle of name) and whitespaces allowed',
                             status_code=400)
    path = repo_path / 'transformers' / name
    path.mkdir(exist_ok=True, parents=True)
    serialize(path, request.json)

    return sanic.json(f"Transformer '{name}' saved")


@bp.get("/transformers/<name>")
@doc.tag('transformers')
@doc.summary("Display object info from 'transformers'")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def transformers_info(request, name):
    name = unquote(name)

    path = repo_path / 'transformers' / name
    if not path.exists():
        raise SanicException(f"Tranformer '{name}' does not exist!", status_code=400)
    return sanic.json(deserialize(path))


@bp.delete("/transformers/<name>")
@doc.tag('transformers')
@doc.summary("Delete an object from 'transformers'")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def delete_transformer(request, name):
    name = unquote(name)
    path = repo_path / 'transformers' / name
    if not path.exists():
        raise SanicException(f"Tranformer '{name}' does not exist!", status_code=400)
    shutil.rmtree(path)
    return sanic.json(f"Transformer '{name}' deleted")


### MODELS ###

@bp.get("/models")
@doc.tag('models')
@doc.summary("List objects in 'models'")
async def list_models(request):
    # save_defaults(repo='models')
    return sanic.json(get_all('models'))


@bp.post("/models/<name>")
@doc.tag('models')
@doc.summary("Save an object in 'models'")
@doc.description('''
    Examples
    --------
    obj = {"__klass__": "skt.ARIMA"}
    obj = {"__klass__": "skt.NaiveForecaster",
            "strategy": "mean"
            "window_lenght"=12
            "sp"=3}
           ''')
@doc.consumes(doc.JsonBody({}), location="body")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def create_model(request, name):
    name = unquote(name)

    if not re.search(r'(?i)^[a-z0-9]([a-z0-9_]*[a-z0-9])?$', name):
        raise SanicException('No special characters (except _ in the middle of name) and whitespaces allowed',
                             status_code=400)

    path = repo_path / 'models' / name
    path.mkdir(exist_ok=True, parents=True)
    serialize(path, request.json)
    return sanic.json(f"Model '{name}' saved")


@bp.get("/models/<name>")
@doc.tag('models')
@doc.summary("Display object info from 'models'")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def models_info(request, name):
    name = unquote(name)

    path = repo_path / 'models' / name
    if not path.exists():
        raise SanicException(f"Model '{name}' does not exist!", status_code=400)
    return sanic.json(deserialize(path))


@bp.delete("/models/<name>")
@doc.tag('models')
@doc.summary("Delete an object from 'models'")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def delete_model(request, name):
    name = unquote(name)

    path = repo_path / 'models' / name
    if not path.exists():
        raise SanicException(f"Model '{name}' does not exist!", status_code=400)
    shutil.rmtree(path)
    return sanic.json(f'Model "{name}" deleted')


### PREDICTORS ###

@bp.get("/predictors")
@doc.tag('predictors')
@doc.summary("List objects in 'predictors'")
@doc.consumes(doc.Boolean(name='info'))
async def list_predictors(request):
    predictors = get_all('predictors')
    if not request.args.get('info', False):
        return sanic.json(predictors)
    res = []
    for name in predictors:
        try:
            res_tmp = dict(name=name)
            predictor_path = repo_path / 'predictors' / name
            infos = deserialize(predictor_path)
            dao = JSONFSDAO(predictor_path / 'history')
            infos['history'] = len(dao.all())
            #### TODO: aggiungere vere info
            # res_tmp.update(predictor_details(infos, name, 'development', fitting.all(status='alive'), repo_path))
            res.append(res_tmp)
        except:
            logger.debug('TracebackERROR: \n' + traceback.format_exc() + '\n\n')

    return sanic.json(res)


@bp.post("/predictors/<name>")
@doc.tag('predictors')
@doc.summary("Save an object in 'predictors'")
@doc.description('''
<b>model_id:</b> choose one model (see <b>POST /models/{name}</b>)
<b>transformer_id:</b> choose one transformer (see <b>POST /transformers/{name}</b>) or <i>"none"</i> ''')
@doc.consumes(doc.String(name="transformer_id"), location="query")
@doc.consumes(doc.String(name="model_id"), location="query")
@doc.consumes(doc.String(name="description"), location="query")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def create_predictor(request, name):
    name = unquote(name)

    if not re.search(r'(?i)^[a-z0-9]([a-z0-9_]*[a-z0-9])?$', name):
        raise SanicException('No special characters (except _ in the middle of name) and whitespaces allowed',
                             status_code=400)

    predictor_path = repo_path / 'predictors' / name

    check_predictor_existence(predictor_path)
    ### transformer ###
    transformer_id = request.args.get('transformer_id', 'auto')
    model_id = request.args.get('model_id', 'auto')
    blueprint = request.json

    if transformer_id == 'auto':
        # transformer = 'auto'
        raise NotImplementedError
    elif transformer_id == 'none':
        # transformer = {"__klass__": "ds4biz.ct", "transformers": {}, "remainder": "passthrough"}
        raise SanicException("'none' transformer not yet implemented", status_code=501)
    else:
        tpath = repo_path / 'transformers' / transformer_id
        check_existence(tpath, "transformer")
        transformer = deserialize(tpath)
    ### model ###
    if model_id == 'auto':
        # mod = 'auto'
        raise NotImplementedError
    else:
        mpath = repo_path / 'models' / model_id
        check_existence(mpath, "Model")
        mod = deserialize(mpath)
    ### blueprint ###
    if blueprint:
        if blueprint.get('transformer'):
            transf = blueprint['transformer']
            # check_blueprint(transf, step='transformer')
        if blueprint.get('model'):
            mod = blueprint['model']
            # check_blueprint(mod, step='model')

    predictor_path.mkdir(exist_ok=True, parents=True)
    bp = dict(id=name,
              description=request.args.get('description', ''),
              created_on=time.time() * 1000,
              # img=request.args.get('img', 'predictor_base'),
              steps=dict(transformer=transformer, model=mod))
    serialize(predictor_path, bp)
    return sanic.json(f"Predictor '{name}' saved")


@bp.get("/predictors/<name>")
@doc.tag('predictors')
@doc.summary("Display object info from 'predictors'")
@doc.description("""
<b>name:</b> predictor id (see <b>GET /predictors</b>)
<b>details:</b> set to True to get more info
<b>branch:</b> development or master (see /predictors/{name}/release</b>)""")
# @doc.consumes(doc.String(name="branch", choices=['development', 'master']), location="query")
@doc.consumes(doc.Boolean(name="details"), location="query")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def predictors_info(request, name):
    name = unquote(name)

    path = repo_path / 'predictors' / name
    if not path.exists():
        raise SanicException(f'Predictor "{name}" does not exist!', status_code=400)
    infos = deserialize(path)
    details = request.args.get('details', 'false').capitalize
    if not details:
        return sanic.json(infos['steps'])
    ###########todo: SVILUPPARE PARTE SOTTO#

    # branch = request.args.get('branch', 'development')
    # infos = predictor_details(infos, name, branch, fitting.jobs, repo_path)

    return sanic.json(infos)


@bp.delete("/predictors/<name>")
@doc.tag('predictors')
@doc.summary("Delete an object from 'predictor'")
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def delete_predictor(request, name):
    name = unquote(name)

    path = repo_path / 'predictors' / name
    if not path.exists():
        raise SanicException(f'Predictor "{name}" does not exist!', status_code=400)
    # ##TODO: sviluppare questa parte
    # if name in fitting.all('alive'):
    #     dc = fitting.get_by_id(name)['dc']
    #     cd.kill(dc.name)
    #     msg = 'Killed'
    #     fitting.add(name, msg)
    #     send_message(name, msg)
    #     fitting.remove(name)
    #     logger.debug(f'Fitting {name} Killed')
    # else:
    #     cname = list(filter(lambda x: x.endswith('_'+name), cd.containers.keys()))
    #     if cname:
    #         cd.kill(cname[0])
    #         logger.debug(f'Container {cname[0]} Killed')

    shutil.rmtree(path)

    # testset_dao = get_dataset_dao(repo_path=repo_path)
    # testset_dao.set_coll(name)
    # testset_dao.dropcoll()
    # testset_dao.close()

    return sanic.json(f"Predictor '{name}' deleted")


@bp.post("/predictors/<name>/fit")
@doc.tag('predictors')
@doc.summary('Fit an existing predictor')
@doc.description('''
    Examples
    --------
    data = {"data":[{"Date_Time": "01/03/2010  08:20:40" },
                    {"Date_Time": "01/10/2010  08:20:40"},
                    {"Date_Time": "01/17/2010  08:20:40"},
                    {"Date_Time": "01/24/2010  08:20:40"},
                    {"Date_Time": "01/31/2010  08:20:40"},
                    {"Date_Time": "02/07/2010  08:20:40"},
                    {"Date_Time": "02/14/2010  08:20:40"},
                    {"Date_Time": "02/21/2010  08:20:40"},
                    {"Date_Time": "02/28/2010  08:20:40"},
                    {"Date_Time": "03/07/2010  08:20:40"},
                    {"Date_Time": "03/14/2010  08:20:40"},
                    {"Date_Time": "03/21/2010  08:20:40"}],
     "target":[1509634,1581344, 1614204, 1897725, 1759063,1320022, 1559063, 1659063, 1859063, 1551083, 1819012, 1801029]}
    ...................
               ''')
# @doc.consumes(doc.String(name="fit_params"), location="query")
@doc.consumes(doc.JsonBody({'data': doc.List(doc.Dictionary), 'target': doc.List()}), location="body", required=True)
# @doc.consumes(doc.Boolean(name="report"), location="query")
# @doc.consumes(doc.Integer(name="cv"), location="query")
# @doc.consumes(doc.Boolean(name="partial"), location="query")
@doc.consumes(doc.Float(name="test_size"), location="query")
@doc.consumes(doc.String(name="task", choices=[ 'forecasting']), location="query", required=True)#'classification', 'none'
@doc.consumes(doc.Integer(name="forecasting_horizon"), location="query", required=False)
@doc.consumes(doc.String(name="datetime_feature"), location="query", required=True)
@doc.consumes(doc.String(name="datetime_frequency", choices=["Years", "Months", "Days", "hours", "minutes", "seconds"]), required=True)
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def fit(request, name):
    print("fitting")

    name = unquote(name)
    predictor_path = repo_path / 'predictors' / name
    print("predictor: ", predictor_path)
    predictor_blueprint = deserialize(predictor_path)
    print("bp: ",predictor_blueprint)
    dparams = dict(test_size=.2,
                   forecasting_horizon=None,
                   datetime_frequency = "s",
                   # partial=False,
                   fit_params=dict(),
                   # cv=0,
                   # report=False, history_limit=0,
                   task='forecasting',
                   # save_dataset=False
                   )
    params = {**dparams, **load_params(request.args)}
    params["datetime_frequency"] = params["datetime_frequency"][0]

    print("parameters::: ",params)
    data = request.json
    print("data", data)
    try:
        training_pipeline(predictor_blueprint=predictor_blueprint, data=data, **params)
    except Exception as e:
        print(e)
        raise e
    # data: Dict, task: str, test_size:Union[float, int], fit_params:Dict

    # if params.get('partial'):
    #     if predictor_path / 'development' not in list(predictor_path.glob('*')):
    #         raise FitException(f'Predictor "{name}" is not fitted')
    #     else:
    #         if predictor_path / 'development' in list(predictor_path.glob('*')):
    #             raise FitException(f'Predictor "{name}" already fitted')

    return sanic.json(f"Predictor '{name}' correctly fitted")


@bp.post("/predictors/<name>/predict")
@doc.tag('predictors')
@doc.summary('Use an existing predictor to predict data')
@doc.consumes(doc.JsonBody({}), location="body", required=False)
@doc.consumes(doc.Integer(name="forecasting_horizon"), location="query", required=False)
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def predict(request, name):
    name = unquote(name)

    ### check predictor exist ###
    path = repo_path / 'predictors' / name
    branch = "development" #todo: aggiungere a fit e predict parametro branch
    params = {**load_params(request.args)}
    if path / branch not in list(path.glob('*')):
        raise SanicException(f'Predictor "{name}" is not fitted', status_code=400)
    pipeline = load_pipeline(name, branch, repo_path=repo_path)
    data = request.json
    data = to_dataframe(data) if data else None #pd.DataFrame(request.json).fillna(np.nan)

    preds = pipeline.predict(X = data, horizon=params["forecasting_horizon"])#, include_probs=params['include_probs'])
    # if params['include_probs']:
    #     preds = [[[c,float(p)] for c,p in el] for el in preds]
    # else:
    #     preds = preds.tolist()

    return sanic.json(preds)


@bp.post("/predictors/<name>/evaluate")
@doc.tag('predictors')
@doc.summary('Evaluate existing predictors in history')
@doc.consumes(doc.JsonBody({'data': doc.List(doc.Dictionary), 'target': doc.List()}), location="body")
# @doc.consumes(doc.JsonBody({}), location="body", required=False)
# @doc.consumes(doc.Integer(name="forecasting_horizon"), location="query", required=False)
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def evaluate(request, name):
    branch = "development"
    # params = {**load_params(request.args)}
    params = dict()
    params["branch"] = branch
    name = unquote(name)
    body = request.json

    logger.debug("loading predictor pipeline...")
    pipeline = load_pipeline(name, params['branch'], repo_path=repo_path)
    datetime = pipeline.date.strftime('%Y-%m-%d %H:%M:%S.%f')

    logger.debug("pre-processing evaluation data...")
    # y = FACTORY(body['target'])
    data = preprocessing_data(body, datetime_feature="Date_Time", datetime_frequency="M")

    y = data["y"]
    X = data["X"]

    logger.debug("computing forecast report")
    report = pipeline.get_forecast_report(y=y, X=X)
    logger.debug(f"report: {report}")
    res = [{"report_test":  report, "datetime": datetime,
            "task": "forecast"}]
    print("res:::",res)
    return sanic.json(res)



@bp.post("/predictors/import")
@doc.tag('predictors')
@doc.summary('Upload existing predictor')
@doc.consumes(doc.File(name="f"), location="formData", content_type="multipart/form-data", required=True)
async def import_predictor(request):
    path = repo_path / 'predictors'
    file = request.files.get('f')
    if file.name.endswith('.zip'):
        import_zipfile(file, path)
    else:
        raise Exception("Error")
    return sanic.json('Predictor correctly imported')


@bp.get("/predictors/<name>/export")
@doc.tag('predictors')
@doc.summary('Download existing predictor')
@doc.consumes(doc.String(name="name"), location="path", required=True)
async def export_predictor(request, name):
    name = unquote(name)

    file_name = name + '.zip'
    path = repo_path / 'predictors' / name
    buffer = io.BytesIO()
    make_zipfile(buffer, path)
    buffer.seek(0)
    headers = {'Content-Disposition': 'attachment; filename="{}"'.format(file_name)}
    return raw(buffer.getvalue(), headers=headers)


@app.exception(Exception)
async def manage_exception(request, exception):
    if isinstance(exception, SanicException):
        print(dict(error=str(exception)))
        return sanic.json(dict(error=str(exception)), status=exception.status_code)

    e = dict(error=f"{exception.__class__.__name__}: {exception}")

    if isinstance(exception, NotFound):
        return sanic.json(e, status=404)
    status_code = exception.status_code or 500
    logger.error('TracebackERROR: \n' + traceback.format_exc() + '\n\n', exc_info=True)
    return sanic.json(e, status=status_code)


app.blueprint(bp)

app.run("0.0.0.0", port=8087, auto_reload=True)
