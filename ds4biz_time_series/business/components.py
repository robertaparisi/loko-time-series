from loko_extensions.model.components import Component, Input, Output, save_extensions, Select, Arg, Dynamic

predict_service = "loko-services/predictors/predict"
fit_service = "loko-services/predictors/fit"
evaluate_service = "loko-services/predictors/evaluate"

#########################   ARGS     ###########################

#### FIT ARGS
pred_name = Arg(name="predictor_name", label="Predictor Name", type="text",
                helper="Digit the name of the predictor you want to use")

# task = Select(name="task", label="Task", options=["Forecasting","Classification"], group="fit")

fh = Arg(name="forecasting_horizon", label="Forecasting Horizon", type="number", group="fit", value=1)
dt_feature = Arg(name="datetime_feature", label="Datetime Feature", type="text",
                 helper="Name of the feature to use as date-time reference", group="fit")
dt_frequency = Arg(name="datetime_frequency", label="Datetime Frequency", type="text",
                   helper="Time frequence required for the model ", group="fit")
report = Arg(name="report", label="Compute metrics report", type="boolean", group="fit", value="false")
test_size = Dynamic(name="test_size", label="Test Size", parent="report", condition="{parent}===true",
                    dynamicType="number", group="fit", value=30)

fit_args = [dt_feature, dt_frequency, fh, report, test_size]
#### PREDICT ARGS

fh_pred = Arg(name="forecasting_horizon", label="Forecasting Horizon", type="numeric", group="predict", value=1)

# Arg(name= , label= , type= , group= "predict" )

predict_args = [fh_pred]
#### EVALUATE ARGS

report_eval = Arg(name="save_eval_report", label="Save metrics report", type="boolean", group="evaluate", value="false")

evaluate_args = [report_eval]

args_list = [pred_name] + fit_args + predict_args + evaluate_args
#########################   INPUT   ###########################
inp = [Input(id="fit", label="fit", to="fit", service=fit_service, ),
       Input(id="predict", label="predict", service=predict_service, to="predict"),
       Input(id="evaluate", label="evaluate", to="evaluate", service=evaluate_service)]

#########################   OUTPUT   ###########################

out = [Output(id="fit", label="fit"), Output(id="predict", label="predict"), Output(id="evaluate", label="evaluate")]

#########################   COMPONENT   ###########################

c1 = Component(name="time-series", description="TimeSeries components", inputs=inp,
               outputs=out, args=args_list, configured=False)

save_extensions([c1], path="../extensions")
