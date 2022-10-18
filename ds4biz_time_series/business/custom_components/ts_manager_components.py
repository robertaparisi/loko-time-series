from loko_extensions.model.components import Component, Input, Output, save_extensions, Select, Arg, Dynamic, \
    AsyncSelect

create_predictor_service = "loko-services/create_predictor"

delete_predictor_service = "loko-services/delete_objs"
info_predictor_service = "loko-services/info_obj"

################################# ARGS ##################################


predictor_list_service = "http://localhost:9999/routes/ds4biz-time-series/predictors"
transformer_list_service = "http://localhost:9999/routes/ds4biz-time-series/transformers"
model_list_service = "http://localhost:9999/routes/ds4biz-time-series/models"
############################ create args #############################

create_group = "Create Parameters"

predictor = Arg(name="predictor_name", label="Predictor", helper="Choose the name you want to use for your predictor",
                type="text", group=create_group)
description = Arg(name="description", label="Description", helper="Add a description for your predictor, if you want",
                type="area", group=create_group)
# objs = Arg(name="existing_objs", label="Use existing & model", type="boolean", group=create_group,
#                   value="true")
# transformer_name = Dynamic(name="transformer_id", label="Transformer", dynamicType="asyncSelect",
#                            description="Express the name of the transformer you want to use", parent="existing_objs",
#                            condition='{parent}===true', group=create_group, url=transformer_list_service)
# model_name = Dynamic(name="model_id", label="Model", description="Express the name of the model you want to use",
#                      dynamicType="asyncSelect", parent="existing_objs", condition='{parent}===true',
#                      group=create_group,
#                      url=model_list_service)
# predictor_bp = Dynamic(name="blueprint", label="Blueprint", description="Define the blueprint of the predictor you want to use",
#                     dynamicType="area", parent="existing_objs", condition='{parent}===false', group=create_group)
transformer = Arg(name="existing_transf", label="Use existing transformer", type="boolean", group=create_group,
                  value="true")
transformer_name = Dynamic(name="transformer_id", label="Transformer", dynamicType="asyncSelect",
                           description="Express the name of the transformer you want to use", parent="existing_transf",
                           condition='{parent}===true', group=create_group, url=transformer_list_service)
transformer_def = Dynamic(name="transformer_bp", label="Transformer",
                          description="Define the structure of the transformer you want to use", dynamicType="area",
                          parent="existing_transf", condition='{parent}===false', group=create_group)

model = Arg(name="existing_model", label="Use existing model", type="boolean", group=create_group, value="false")
model_name = Dynamic(name="model_id", label="Model", description="Express the name of the model you want to use",
                     dynamicType="asyncSelect", parent="existing_model", condition='{parent}===true',
                     group=create_group,
                     url=model_list_service)
model_def = Dynamic(name="model_bp", label="Model", description="Define the structure of the model you want to use",
                    dynamicType="area", parent="existing_model", condition='{parent}===false', group=create_group)

# task = AsyncSelect(name='task', label='Task', url='http://localhost:9999/routes/loko_prescriptor/saro')

create_args = [predictor, description, transformer, transformer_name, transformer_def, model, model_name, model_def]
# create_args = [predictor, objs, transformer_name, model_name, predictor_bp]

############################ delete args #############################


delete_group = "Delete Parameters"

del_predictor = AsyncSelect(name="del_predictor", label="Predictor", url=predictor_list_service, group=delete_group)
del_model = AsyncSelect(name="del_model", label="Model", url=model_list_service, group=delete_group)
del_transformer = AsyncSelect(name="del_transformer", label="Transformer", url=transformer_list_service,
                              group=delete_group)

# task = AsyncSelect(name='task', label='Task', url='http://localhost:9999/routes/loko_prescriptor/saro')


delete_args = [del_transformer, del_model, del_predictor]

############################ info args #############################


info_group = "Info Parameters"
info_obj = Select(name="info_obj", label="Object", options=["Predictor", "Transformer", "Model"],
                  helper="Select the object you want to have info on.", group=info_group)
info_predictor = Dynamic(name="info_obj_name", label="Predictor", dynamicType="asyncSelect", parent="info_obj",
                         description="Select the name of the predictor you want to know about",
                         condition='{parent}==="Predictor"', url=predictor_list_service, group=info_group)
info_model = Dynamic(name="info_obj_name", label="Model", dynamicType="asyncSelect", parent="info_obj",
                         description="Select the name of the model you want to know about",
                         condition='{parent}==="Model"', url=model_list_service, group=info_group)
info_transformer = Dynamic(name="info_obj_name", label="Transformer", dynamicType="asyncSelect", parent="info_obj",
                         description="Select the name of the transformer you want to know about",
                         condition='{parent}==="Transformer"', url=transformer_list_service, group=info_group)


# task = AsyncSelect(name='task', label='Task', url='http://localhost:9999/routes/loko_prescriptor/saro')


info_args = [info_obj, info_predictor, info_model, info_transformer]

###################################################################

args_list = create_args + delete_args + info_args

##################### Time SERIES MANAGER ###########################
manager_inputs = [Input(id="create", label="create_predictor", to="create", service=create_predictor_service),
                  Input(id="delete", label="delete_objects", service=delete_predictor_service, to="delete"),
                  Input(id="info", label="info_object", service=info_predictor_service, to="info")]

##################### Time SERIES MANAGER ###########################
manager_outputs = [Output(id="create", label="create_predictor"),
                   Output(id="delete", label="delete_objects"),
                   Output(id="info", label="info_object")]

ts_manager_component = Component(name="TimeSeries Manager", description="Components that managaes Time Series Models",
                                 args=args_list, inputs=manager_inputs, outputs=manager_outputs, icon="RiFileSettingsFill")



""" tf_i
{
  "__klass__": "sktime.transformations.compose.TransformerPipeline",
  "steps": [
    {
      "__klass__": "sktime.transformations.series.detrend.Deseasonalizer",
      "model": "multiplicative",
      "sp": 12
    },
    {
      "__klass__": "sktime.transformations.series.detrend.Deseasonalizer",
      "model": "additive",
      "sp": 3
    }
  ]
}"""