import numpy as np
import sagemaker
from sagemaker.deserializers import JSONDeserializer
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer

session = sagemaker.Session()
endpoint_name = "tensorflow-inference-endpoint-name"

# Create a generic Predictor
predictor = Predictor(
    endpoint_name=endpoint_name,
    sagemaker_session=session,
    serializer=JSONSerializer(),
    deserializer=JSONDeserializer(),
)
counter = 0
while 1:
    # sleep for 1 second
    import time

    time.sleep(1)
    if counter == 0:
        sample_input = np.array([1, 0, 0, 0])
    elif counter == 1:
        sample_input = np.array([0, 1, 0, 0])
    elif counter == 2:
        sample_input = np.array([0, 0, 1, 0])
    elif counter == 3:
        sample_input = np.array([0, 0, 0, 1])
    predictions = predictor.predict(sample_input)
    print("Raw predictions:", predictions)
    prediction_vector = predictions["predictions"][0]
    print("Predicted class:", np.argmax(prediction_vector))
    print("Success")
    counter += 1
    if counter > 3:
        counter = 0
