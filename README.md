# loko-time-series


This projects, developed in Python, create some [LoKo AI](https://github.com/loko-ai/loko/tree/development) extensions that helps with **Time Series Forecasting**. 


### Component

#### TimeSeries


Thanks to the **TimeSeries** component you can train your model, make prediction and test evaluation, with the possibility to save the evaluation metrics in a file. This component works similarly to the Predictor component.


![image](https://user-images.githubusercontent.com/34518514/196521744-7a0d543f-5f7f-4ac1-9847-ab4fcec1fc48.png)


In order to **fit** the model you need to specify the predictor to use, as well as the parameters *"Datetime Feature"* and *"Datetime Frequency"* otherwise the training will not start and an error will be raised.

To make **prediction**, you have to specify both the name of the predictor to use and the forecasting horizon. 

In order to **evaluate** new data instead it's not required to specify anything other than the predictor to use. If you decide to save the metrics, you can find a json file, with a .eval extension and the name you specified in the proper field (namely *"Evaluation file name"*), in the path "data/ts_evaluation", as shown in the image below.

![image](https://user-images.githubusercontent.com/34518514/196524919-865e3456-003f-4cf6-b5ae-4d15533399d1.png)


### Example Flow


Opening Loko AI, you can find the Tab **TimeSeriesForecasting**, where you can find two examples of forecasting, one that do not use covariates for the training and one that use them.


![image](https://user-images.githubusercontent.com/34518514/196522275-ffcfb7f2-9776-4747-a02e-9916b3e58fef.png)


Down below is shown an example of how you can fill the component parameters

![image](https://user-images.githubusercontent.com/34518514/196522586-7da8cf09-69f7-42e2-9d3b-2f6205a163a2.png)




### TimeSeries GUI
It's possible to use the **TimeSeries GUI** to *create* or *delete* your own **Transformer**, **Model** and **Predictors**. Once you have a TimeSeries predictor you can also choose to *export* it, obtaining a zip file, or eventually *import* a TimeSeries predictor that you previously created. 


Each TimeSeries predictor has a status, which can be *"Not Fitted"*, *"Fitted"*, *"Training"* if the training task is started and not yet finished, as shown in the image below.


![image](https://user-images.githubusercontent.com/34518514/196519914-5591be53-0c0f-4b07-af14-8a89373f1e39.png)


Clicking on one of the Predictor/Model/Transformer object of the list, you can see a "blueprint" of the object, namely a json file cointaining the relative informations. The following image shows a predictor object:

![image](https://user-images.githubusercontent.com/34518514/196521263-1ec2ee69-3e56-4278-97cc-493a7740cfbf.png)
