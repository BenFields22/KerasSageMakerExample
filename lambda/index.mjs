import {
  SageMakerRuntimeClient,
  InvokeEndpointCommand,
} from "@aws-sdk/client-sagemaker-runtime";
import AmazonDaxClient from "amazon-dax-client";
import AWS from "aws-sdk";

let daxClient = null;
const dax = new AmazonDaxClient({
  endpoints: ["DAX-cluster-endpoint"],
  region:"your-region",
});
daxClient = new AWS.DynamoDB.DocumentClient({ service: dax });

const sagemakerClient = new SageMakerRuntimeClient({});
//const client = new DynamoDBClient({});
//const dynamo = DynamoDBDocumentClient.from(client);
const dynamo = daxClient;
const tableName = "HotelRates";

function indexOfMax(arr) {
  if (arr.length === 0) {
      return -1;
  }

  var max = arr[0];
  var maxIndex = 0;

  for (var i = 1; i < arr.length; i++) {
      if (arr[i] > max) {
          maxIndex = i;
          max = arr[i];
      }
  }

  return maxIndex;
}

function shuffleArray(array) {
  for (var i = array.length - 1; i >= 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
  }
}

export const handler = async (event, context) => {
  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json",
  };
  var myid = event.id;
  const params = {
    TableName: tableName,
    Key: {
      id: myid,
    },
  };
  body = await dynamo.get(params).promise();
  body = body.Item;
  body = body.values
  //console.log(body);
  const valuesArray = body.values;
  var rates = valuesArray.map(Number);
  shuffleArray(rates);
  //console.log("rates: ",rates);

  //do inference in sagemaker endpoint
  const endpointName = "Sagemaker-inference-endpoint-name";
  const inputPayload = JSON.stringify({ instances: [rates] });
  const command = new InvokeEndpointCommand({
    EndpointName: endpointName,
    ContentType: "application/json",
    Body: inputPayload,
  });
  
  const response = await sagemakerClient.send(command);
  //console.log(response);
  const result = JSON.parse(Buffer.from(response.Body).toString("utf8"));
  var prediction = result.predictions[0].map(Number);
  //console.log(prediction);
  var index = indexOfMax(prediction);
  var bestRate = rates[index];
  body = {
    id: myid,
    bestRate: bestRate,
    allrates: rates,
    prediction: prediction
  };

  return {
    statusCode,
    body,
    headers,
  };
};