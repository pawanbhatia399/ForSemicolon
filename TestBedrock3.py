import boto3
import json
from botocore.exceptions import ClientError

def invoke_llama2(bedrock_runtime_client, prompt):
            body = {
                "prompt": prompt,
                "temperature": 0.5,
                "top_p": 0.9,
                "max_gen_len": 100,
            }
            model_id = 'meta.llama2-70b-chat-v1'

            response = bedrock_runtime_client.invoke_model(
                            modelId=model_id, 
                            body=json.dumps(body),
                            contentType = "application/json",
                            accept = "application/json"
            )

            response_body = json.loads(response["body"].read())
            completion = response_body.get("generation")

            return completion

text="""Python is a high-level, general-purpose programming language. Its design philosophy 
emphasizes code readability with the use of significant indentation.

Python consistently ranks as one of the most popular programming languages, and has gained 
widespread use in the machine learning community"""

prompt_data = f"""Please generate questions only for the text given ahead: {text}"""

print(prompt_data)

brt = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)
result = invoke_llama2(brt, "Please generate two questions for the text given ahead: Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.")
print(result)