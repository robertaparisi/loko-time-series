import re
import shutil
import time
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
from ds4biz_time_series.dao.fs_dao import JSONFSDAO
from ds4biz_time_series.utils.logger_utils import logger
from ds4biz_time_series.utils.ppom_utils import get_pom_major_minor
from sanic.exceptions import SanicException, NotFound

import sanic

from ds4biz_time_series.utils.service_utils import check_predictor_existence
from ds4biz_time_series.utils.serialization_utils import serialize, deserialize
from ds4biz_time_series.utils.service_utils import get_all

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
    obj = {{
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
<b>model_id:</b> choose one model (see <b>POST /models/{name}</b>) or <i>"auto"</i>
<font color="#800000"><b>AUTOML parameters must be set in the previous service!</b></font>
<b>transformer_id:</b> choose one transformer (see <b>POST /transformers/{name}</b>) or <i>"auto"</i> or <i>"none"</i> ''')
@doc.consumes(doc.JsonBody({}), location="body")
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
        raise NotImplementedError
    else:
        tpath = repo_path / 'transformers' / transformer_id
        transformer = deserialize(tpath)
    ### model ###
    if model_id == 'auto':
        # mod = 'auto'
        raise NotImplementedError
    else:
        mpath = repo_path / 'models' / model_id
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

    e = dict(error=f"{exception.__class__.__name__}: {exception}")

    if isinstance(exception, NotFound):
        return sanic.json(e, status=404)
    status_code = exception.status_code or 500
    logger.error('TracebackERROR: \n' + traceback.format_exc() + '\n\n', exc_info=True)
    return sanic.json(e, status=status_code)


app.blueprint(bp)

app.run("0.0.0.0", port=8087, auto_reload=True)