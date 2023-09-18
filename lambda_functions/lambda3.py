import json

# Define threshold for filtering inferences
THRESHOLD = .85

def lambda_handler(event, context):
    try:
        print(f"Full event: {event}")
        print(f"Event type: {type(event)}")
        print(f"Event body: {event.get('body', 'Body is empty')}")

        body = json.loads(event.get("body", "{}"))
        inner_body_data = body.get("body", "{}")
        
        if isinstance(inner_body_data, str):
            inner_body = json.loads(inner_body_data)
        else:
            inner_body = inner_body_data
        
        inferences = inner_body.get("inferences", [])
        
        # Convert the inferences string to a list of floats
        if isinstance(inferences, str):
            inferences = json.loads(inferences)
        
        print(f"Initial inferences: {inferences}, type: {type(inferences)}")
        
        # Check if any values in our inferences are above THRESHOLD
        if not inferences:
            raise Exception("NO_INFERENCES_FOUND")
        elif not any(float(value) >= THRESHOLD for value in inferences):
            raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
            
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Event: {event}")
        return {
            'statusCode': 500,
            'body': f"JSONDecodeError: {e}"
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
