# KerasSageMakerExample
Example project that demonstrates a full-stack application where a frontend drives selection of an ID. A button makes a call to API Gateway passing the selected ID which then uses lambda to call DAX for caching for a DynamoDB table. The table simply stores arrays of ratings aligned to the ID number. Once pulled the array is passed to a custom Keras model trained for argmax (index of max element). The inference endpoint returns the position of the max value and then the lambda function uses this to select the best rating. The rating is returned to the client along with all the relevent data from each step for verification. 

![architecture digram](https://github.com/BenFields22/KerasSageMakerExample/blob/main/architecture.png)
![app ui](https://github.com/BenFields22/KerasSageMakerExample/blob/main/AppUI.png)
