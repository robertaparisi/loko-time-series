
app = Sanic("res")
swagger_blueprint.url_prefix = "/api"
app.blueprint(swagger_blueprint)


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