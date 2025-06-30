import json
import boto3

# Create Bedrock client (add region if not using default config)
bedrockClient = boto3.client('bedrock-agent')  # Change region as needed

def lambda_handler(event, context):
    print("Inside Lambda Handler")
    print('event:', event)

    dataSourceId = '<data_source_id>'  # Replace with your actual data source ID
    knowledgeBaseId = '<knowledge_base_id>'  # Replace with your actual knowledge base ID

    try:
        response = bedrockClient.start_ingestion_job(
            knowledgeBaseId=knowledgeBaseId,
            dataSourceId=dataSourceId
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        print("Error starting ingestion job:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
