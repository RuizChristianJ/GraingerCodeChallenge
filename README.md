# GraingerCodeChallenge

## Scalable ML Solution
## Christian Ruiz

### Tech stack:
 - mlflow
    - Logging hyperparameters 
    - Data version
    - Performance metrics
    - Model registry
    - Should be deployed in a server
 - delta table
    - More robust than CSV files
    - Lineage tracking from raw to curated
    - Table versioning
    - ACID transaction capture
 - drift.py
    - Run on scheduled cadence
    - Check for model and data drift
    - Trigger retraining of model
 - a_b_testing.py
    - Compare the “Staging” stage model to the “Production” stage model registered in mlflow. 
    - Push the “Staging” model to the “Production” stage if it performs better.
 - training.py
    - Train model and register in mlflow “Staging” stage.
 - prediction.py
    - Load the “Production” stage model from mlflow registry
    - Predict on new data.


### Process:

In this particular case, it does not seem like users will be submitting new data for predictions and it would instead be captured in a database or some object storage like S3 (csv’s). A light pipeline to convert the csv files to the delta format would be needed to make the data more robust. A delta table for the raw, untransformed data would be used as input to another pipeline that performs the necessary transformations required for training the model and stores the transformed data in a curated delta table. Delta tables offer table versioning, ACID transaction logging, and table lineage. These features are all valuable for reproducibility of the trained model. 

For training the model, training.py can be run at the start of the process in order to train the model and log all artifacts from the training in the mlflow model registry. This registry should be hosted on a server such that the deployed containers can load the production model via an API. 

In order to move a model to the “Production” stage in the mlflow registry, a_b_testing.py will need to run after training.py finishes. If there is no model in the “Production” stage, then the model in the “Staging” stage should be pushed into the “Production” stage. If there is an existing model in the “Production” stage, then the two models should be compared through some sort of A/B testing and the best performing model should be registered in the “Production” stage.

When new data is made available in the delta table, a batch inference job should be triggered to run which deploys a docker container. This docker container should run prediction.py which loads the “Production” stage model from the mlflow model registry and makes predictions on the new data. The new results should be stored in a delta table or some other storage that can be used for analysis.

Finally, drift.py should be run on a scheduled cadence in order to identify data drift, model drift, or any other factor that could invalidate the current model in the “Production” stage of mlflow. If whatever threshold that is defined in drift.py is met, a job should be triggered to kick off the process of running training.py and a_b_testing.py. 


### Nuances not mentioned in the above process:

Some tools for queues and event triggers would need to be used at multiple stages. 

 - In Databricks I have scheduled jobs that run on a predetermined cadence due to the nature of how and when we receive new data. There are alternative options for queues and events in the cloud for a more on-demand process rather than everything being scheduled ahead of time.

Scaling to deploy multiple containers for large amounts of data. 

 - In Databricks (the alternative to Docker that I am most familiar with) a cluster can be configured in the UI that specifies the virtual machine instance type to use in the cloud for driver and worker nodes as well as the range of worker nodes that you want to allow the cluster to autoscale to. Since I am not completely familiar with Kubernetes and Docker, the above process operates under the assumption that there are similar capabilities as Databricks.
