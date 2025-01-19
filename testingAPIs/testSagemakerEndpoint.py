import numpy as np
import sagemaker
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

session = sagemaker.Session()
endpoint_name = 'endpoint-name'

# Create a generic Predictor
predictor = Predictor(
    endpoint_name=endpoint_name,
    sagemaker_session=session,
    serializer=JSONSerializer(),
    deserializer=JSONDeserializer()
)
while(1):
    #sleep for 1 second
    import time
    time.sleep(1)
    sample_input = np.random.randint(1,1000,4)
    predictions = predictor.predict(sample_input)
    print("Input: ",sample_input)
    print("Raw predictions:", predictions)
    prediction_vector = predictions['predictions'][0]
    infer = np.argmax(prediction_vector)
    check = np.argmax(sample_input)
    print("Prediction: ", infer )
    print("Max of input: ", check)
    if infer == check:
        print("Correct")
    else:
        print("Incorrect")
    





