import boto3
import json

bedrock = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)

input = {
 "modelId": "meta.llama2-70b-chat-v1",
 "contentType": "application/json",
 "accept": "application/json",
 "body": "{\"prompt\":\"Write 2 lines, about India.\",\"max_gen_len\":100,\"temperature\":0.5,\"top_p\":0.9}"
}

# body=input["body"],
# modelId=input["modelId"],
# accept=input["accept"],
# contentType=input["contentType"]
# print(body)
# print(modelId)
# print(accept)
# print(contentType)

#Commented below for testing
response = bedrock.invoke_model(body='{"prompt":"Please generate questions the given text below:Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.Python consistently ranks as one of the most popular programming languages, and has gained widespread use in the machine learning community","max_gen_len":512,"temperature":0.5,"top_p":0.9}',
                                modelId='meta.llama2-70b-chat-v1',
                                accept='application/json',
                                contentType='application/json')

response_body = json.loads(response['body'].read())
print(response_body)