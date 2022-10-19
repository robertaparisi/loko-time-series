# loko-time-series


This projects, developed in Python, create some [LoKo AI](https://github.com/loko-ai/loko/tree/development) extensions that helps with **Time Series Forecasting**. 


## Components

### :chart_with_upwards_trend:	 TimeSeries


Thanks to the **TimeSeries** component you can train your model, make prediction and test evaluation, with the possibility to save the evaluation metrics in a file. This component works similarly to the Predictor component.


![image](https://user-images.githubusercontent.com/34518514/196521744-7a0d543f-5f7f-4ac1-9847-ab4fcec1fc48.png)


In order to **fit** the model you need to specify the predictor to use, as well as the parameters *"Datetime Feature"* and *"Datetime Frequency"* otherwise the training will not start and an error will be raised.

To make **prediction**, you have to specify both the name of the predictor to use and the forecasting horizon. 

In order to **evaluate** new data instead it's not required to specify anything other than the predictor to use. If you decide to save the metrics, you can find a json file, with a .eval extension and the name you specified in the proper field (namely *"Evaluation file name"*), in the path "data/ts_evaluation", as shown in the image below.

![image](https://user-images.githubusercontent.com/34518514/196524919-865e3456-003f-4cf6-b5ae-4d15533399d1.png)

### TimeSeriesManager



This component allows to manage your TimeSeries objects directly from a flow. 

![image](https://user-images.githubusercontent.com/34518514/196581535-ad1a33a1-c322-4384-81f4-45581a01d8ed.png)

Specifically it's possible to **create** new TimeSeries predictor, either by using existing transformer/model or by creating one on the moment, specifying their blueprint of the object. To know more on how to create a predictor, you can find more information in the **Example Flow** section. 


It's then possible to delete one or more TimeSeries objects at the same time, by entering all the names of the ones you want to delete inside the field of the *"Delete Parameters"* tabs.


####[image_to_insert]


Finally you can also have information about a TimeSeries object, choosing in the *"Info Parameters"* the object type and name you want to know more about. As output of the component, you will have the blueprint of the object.





## :cyclone:	 Example Flow


Opening Loko AI, you can find the Tab **TimeSeriesForecasting**, where you can find two examples of forecasting, one that do not use covariates for the training and one that use them.


![image](https://user-images.githubusercontent.com/34518514/196522275-ffcfb7f2-9776-4747-a02e-9916b3e58fef.png)


Down below is shown an example of how you can fill the component parameters

![image](https://user-images.githubusercontent.com/34518514/196522586-7da8cf09-69f7-42e2-9d3b-2f6205a163a2.png)

The next figure show a flow that helps you to manage your TimeSeries objects directly from a flow:

![image](https://user-images.githubusercontent.com/34518514/196581629-bfe72313-2086-49d4-bd2e-3e0dc1d4f09d.png)

As it's shown in the figure above, there are 3 *Trigger* component each of which is linked to a TimeSeries Manager input. While on for the deleting and get information tasks you just have to explicit the desired object, in order to create a predictor, as previously stated, you can either enter an existing object name for transformer and/or model or either choose to directly define a new transformer and/or model, using their blueprint.


####[image_to_insert]
As shown in the image above, in the example, we decided to define a new Model blueprint, which basically is a json object, with 

- a fixed key "\_\_klass\_\_", that will have as value the sktime forecasting algorithm path chosen;
- other couple of key, value representing the hyper-parameter of that module, as the key *"strategy"* and the value *"mean"* for the NaiveForecaster algorithm. 



## :writing_hand:	 TimeSeries GUI
It's possible to use the **TimeSeries GUI** to *create* or *delete* your own **Transformer**, **Model** and **Predictors**. Once you have a TimeSeries predictor you can also choose to *export* it, obtaining a zip file, or eventually *import* a TimeSeries predictor that you previously created. 


Each TimeSeries predictor has a status, which can be *"Not Fitted"*, *"Fitted"*, *"Training"* if the training task is started and not yet finished, as shown in the image below.


![image](https://user-images.githubusercontent.com/34518514/196519914-5591be53-0c0f-4b07-af14-8a89373f1e39.png)


Clicking on one of the Predictor/Model/Transformer object of the list, you can see a "blueprint" of the object, namely a json file cointaining the relative informations. The following image shows a predictor object:

![image](https://user-images.githubusercontent.com/34518514/196521263-1ec2ee69-3e56-4278-97cc-493a7740cfbf.png)




## :computer: USE CASE

It's finally available a small use case in the tab **BrandonTest**, which shows how to fit, predict, and evaluate the model using a small sample of real world data.

![image](https://user-images.githubusercontent.com/34518514/196579422-94472817-bfe0-4f81-9034-e2fdf900bc2c.png)

