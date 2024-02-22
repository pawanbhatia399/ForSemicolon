
import boto3
import json
from botocore.exceptions import ClientError
from reportlab.pdfgen import canvas


def process_data(text_data):
    # Process data (you can replace this with your specific backend logic)
    try:
        prompt_data = f"""Please generate only two questions from the sentences/paragraph given ahead: {text_data}. The questions should be generated so that it can be used for exam papers"""
        cleaned_promt =  prompt_data.replace('\n','')
        #test = "Write 2 lines, about India."
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

        #Invoking the Bedrock Model To Get the Answers
        response = bedrock.invoke_model(body=json.dumps(payload),
                                    modelId='meta.llama2-70b-chat-v1',
                                    accept='application/json',
                                    contentType='application/json',
        )

        response_body = json.loads(response.get("body").read())
        response_text = response_body.get("generation")

        result = "The Generated Questions are as below:\n {}".format(response_text)
        
        return result
        
    except ClientError:
        print("Couldn't invoke Llama 2")
        raise

def generate_pdf(result, pdf_filename):
    # Create a PDF file with the result content
    with canvas.Canvas(pdf_filename) as c:
        text_object = c.beginText(100, 700)
        text_object.setFont("Helvetica", 12)
        text_object.textLines(result)
        c.drawText(text_object)

if __name__ == "__main__":
    import sys

    # Retrieve text data from command line arguments
    text_data = sys.argv[1]

    result = process_data(text_data)

    print(result)
