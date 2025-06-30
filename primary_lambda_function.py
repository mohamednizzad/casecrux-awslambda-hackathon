import json
import boto3

bedrock_client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        #body = json.loads(event['body'])
        #user_question = body.get("query", "")
        user_question = event.get("query")

        print(user_question)

        response = bedrock_client.retrieve_and_generate(
            input={'text': user_question},
            retrieveAndGenerateConfiguration={
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': '<knowledgebaseid>',
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2:1'
                },
                'type': 'KNOWLEDGE_BASE'
            }
        )

        output = {
            "answer": response["output"]["text"],
            "context": response.get("citations", [{}])[0].get("retrievedReferences", [{}])[0].get("content", {}).get("text", ""),
            "doc_url": response.get("citations", [{}])[0].get("retrievedReferences", [{}])[0].get("location", {}).get("s3Location", {}).get("uri", "")
        }

        return {
            'statusCode': 200,
            'body': json.dumps(output)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
