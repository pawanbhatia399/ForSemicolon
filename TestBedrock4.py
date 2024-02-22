import boto3
import json
from botocore.exceptions import ClientError

text="""My Name is Pawan, I live in Chinchwad, I have completed my Graduation, I am currently working in a company names ABC Limited"""
prompt_data = f"""Please generate only two questions from the sentences/paragraph given ahead: {text}. The questions should be generated so that it can be used for exam papers"""

cleaned_promt =  prompt_data.replace('\n','')

bedrock = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)
payload = {
    "prompt": cleaned_promt,
    "max_gen_len": 512,
    "temperature": 0.5,
    "top_p":0.9
}
model_Id_string = f'"meta.llama2-70b-chat-v1"'

#print(model_Id_string)
#Invoking the Bedrock Model To Get the Answers
response = bedrock.invoke_model(body=json.dumps(payload),
                                modelId='meta.llama2-70b-chat-v1',
                                accept='application/json',
                                contentType='application/json',
)

response_body = json.loads(response.get("body").read())
response_text = response_body.get("generation")
print(response_text)

