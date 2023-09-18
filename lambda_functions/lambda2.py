import json
import sagemaker
import base64
from sagemaker.predictor import Predictor
from sagemaker.serializers import IdentitySerializer

ENDPOINT = "image-classification-2023-09-15-16-30-07-441"

def lambda_handler(event, context):
    try:
        print("Received event:", event)
        print("Event body type:", type(event['body']))

        if type(event['body']) == str:
            event['body'] = json.loads(event['body'])

        if 'body' in event and 'image_data' in event['body']:
            image_data = event['body']['image_data']
            image = base64.b64decode(image_data)

            predictor = Predictor(
                endpoint_name=ENDPOINT,
                sagemaker_session=sagemaker.Session()
            )
            predictor.serializer = IdentitySerializer("image/png")

            inferences = predictor.predict(image)

            event["body"]["inferences"] = inferences.decode('utf-8')
            return {
                'statusCode': 200,
                'body': json.dumps(event)
            }
        else:
            print("Keys not found in event")
            return {
                'statusCode': 400,
                'body': 'Keys not found in event'
            }
    except Exception as e:
        print("An error occurred:", e)
        return {
            'statusCode': 500,
            'body': str(e)
        }
