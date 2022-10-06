from loko_extensions.model.components import Component, Input, Output, save_extensions, Select, Arg, Dynamic, \
    AsyncSelect

create_predictor_service = ""

delete_predictor_service = ""



################################# ARGS ##################################


predictor_list_service = "http://localhost:9999/routes/ds4biz-time-series/predictors"
transformer_list_service = "http://localhost:9999/routes/ds4biz-time-series/transformers"
model_list_service = "http://localhost:9999/routes/ds4biz-time-series/models"
############################ create args #############################

create_group = "Create Parameters"

predictor = Arg(name="predictor_name", label="Predictor", helper="Choose the name you want to use for your predictor",
                type="text")

transformer = Arg(name="existing_transf", label="Use existing transformer", type="boolean", group=create_group, value="true")
transformer_name = Dynamic(name="transformer_name", label="Transformer", dynamicType="asyncSelect",
                           description="Express the name of the transformer you want to use", parent="existing_transf",
                           condition='{parent}===true', group=create_group)
transformer_def = Dynamic(name="transformer_def", label="Transformer",
                          description="Define the structure of the transformer you want to use", dynamicType="area",
                          parent="existing_transf", condition='{parent}===false', group=create_group)

model = Arg(name="existing_model", label="Use existing model", type="boolean", group=create_group, value="false")
model_name = Dynamic(name="model_name", label="Model", description="Express the name of the model you want to use",
                     parent="existing_model", condition='{parent}===true', group=create_group)
model_def = Dynamic(name="model_def", label="Model", description="Define the structure of the model you want to use",
                    dynamicType="area", parent="existing_model", condition='{parent}===false', group=create_group)

# task = AsyncSelect(name='task', label='Task', url='http://localhost:9999/routes/loko_prescriptor/saro')

create_args = [predictor, transformer, transformer_name, transformer_def, model, model_name, model_def]

############################ delete args #############################


delete_group = "Delete Parameters"

del_predictor = AsyncSelect(name="del_predictor", label="Predictor", url=predictor_list_service, group=delete_group)
del_model = AsyncSelect(name="del_model", label="Model", url=model_list_service, group=delete_group)
del_transformer = AsyncSelect(name="del_transformer", label="Transformer", url=transformer_list_service, group=delete_group)

# task = AsyncSelect(name='task', label='Task', url='http://localhost:9999/routes/loko_prescriptor/saro')


delete_args = [del_transformer, del_model, del_predictor]

###################################################################

args_list = create_args + delete_args

##################### Time SERIES MANAGER ###########################
manager_inputs = [Input(id="create", label="create_predictor", to="create_predictor", service=create_predictor_service),
                  Input(id="delete", label="delete_predictor", service=delete_predictor_service, to="delete_predictor")]

##################### Time SERIES MANAGER ###########################
manager_outputs = [Output(id="create", label="create_predictor"),
                   Output(id="delete", label="delete_predictor")]

ts_manager_component = Component(name="TimeSeries Manager", description="Components that managaes Time Series Models",
                                 args=args_list, inputs=manager_inputs, outputs=manager_outputs)
