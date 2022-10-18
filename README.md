# loko-time-series


This projects, developed in Python, create some [LoKo AI](https://github.com/loko-ai/loko/tree/development) extensions that helps with **Time Series Forecasting**: thanks to the **TimeSeries** component you can train your model, make prediction and test evaluation, with the possibility to save the evaluation metrics in a file. This component works similarly to the Predictor component.



### TimeSeries GUI
It's possible to use the **TimeSeries GUI** to *create* or *delete* your own **Transformer**, **Model** and **Predictors**. Once you have a TimeSeries predictor you can also choose to *export* it, obtaining a zip file, or eventually *import* a TimeSeries predictor that you previously created. 


Each TimeSeries predictor has a status, which can be *"Not Fitted"*, *"Fitted"*, *"Training"* if the training task is started and not yet finished, as shown in the image below.


![image](https://user-images.githubusercontent.com/34518514/196519914-5591be53-0c0f-4b07-af14-8a89373f1e39.png)


Clicking on one of the Predictor/Model/Transformer object of the list, you can see a "blueprint" of the object, namely a json file cointaining the relative informations. The following image shows a predictor object:

![image](https://user-images.githubusercontent.com/34518514/196521263-1ec2ee69-3e56-4278-97cc-493a7740cfbf.png)
