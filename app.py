import os
import boto3
import json
import requests
import streamlit as st
from streamlit_cognito_auth import CognitoAuthenticator

pool_id = "us-east-1_OclJDKfTS"
app_client_id = "55fpc1q7dcneeu8qhruseuo16l"
app_client_secret = "1ib69uim5fl3slv3rfbgdbkaotjcg6n4hpv470bt98b8v3078deo"
kb_id = "WJO2HHGBTS"
lambda_function_arn = 'arn:aws:lambda:us-east-1:431615879134:function:kbs5b8a05f8-lambda-function'
dynamo_table = 'kbs5b8a05f8_doctor_patient_list_association'

authenticator = CognitoAuthenticator(
    pool_id=pool_id,
    app_client_id=app_client_id,
    app_client_secret= app_client_secret,
    use_cookies=False
)

is_logged_in = authenticator.login()

if not is_logged_in:
    st.stop()

def logout():
    authenticator.logout()

def get_user_sub(user_pool_id, username):
    cognito_client = boto3.client('cognito-idp')
    try:
        response = cognito_client.admin_get_user(
            UserPoolId=pool_id,
            Username=authenticator.get_username()
        )
        sub = None
        for attr in response['UserAttributes']:
            if attr['Name'] == 'sub':
                sub = attr['Value']
                break
        return sub
    except cognito_client.exceptions.UserNotFoundException:
        print("User not found.")
        return None

def get_patient_ids(doctor_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.query(
        TableName=dynamo_table,
        KeyConditionExpression='doctor_id = :doctor_id',
        ExpressionAttributeValues={
            ':doctor_id': {'S': doctor_id}
        }
    )
    print(response)
    patient_id_list = []  # Initialize the list
    for item in response['Items']:
        patient_ids = item.get('patient_id_list', {}).get('L', [])
        patient_id_list.extend([patient_id['S'] for patient_id in patient_ids])
    return patient_id_list

def search_transcript(doctor_id, kb_id, text, patient_ids):
    # Initialize the Lambda client
    lambda_client = boto3.client('lambda')

    # Payload for the Lambda function
    payload = json.dumps({
        "doctorId": sub,
        "knowledgeBaseId": kb_id,
        "text": text, 
        "patientIds": patient_ids
    }).encode('utf-8')

    try:
        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=lambda_function_arn,
            InvocationType='RequestResponse',
            Payload=payload
        )

        # Process the response
        if response['StatusCode'] == 200:
            response_payload = json.loads(response['Payload'].read().decode('utf-8'))
            return response_payload
        else:
            # Handle error response
            return {'error': 'Failed to fetch data'}

    except Exception as e:
        # Handle exception
        return {'error': str(e)}

sub = get_user_sub(pool_id, authenticator.get_username())
print(sub)
patient_ids = get_patient_ids(sub)
print(patient_ids)

# Application Front

with st.sidebar:
    st.header("User Information")
    st.markdown("## Doctor")
    st.text(authenticator.get_username())
    st.markdown("## Doctor Id")
    st.text(sub)
    selected_patient = st.selectbox("Select a patient (or 'All' for all patients)", ['All'] + patient_ids)
    st.button("Logout", "logout_btn", on_click=logout)

st.header("Transcript Search Tool")

# Text input for the search query
query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        # Perform search
        patient_ids_filter = [selected_patient] if selected_patient != 'All' else patient_ids
        results = search_transcript(sub, kb_id, query, patient_ids_filter)
        print(results)
        if results:
            st.subheader("Search Results:")
            st.markdown(results["body"], unsafe_allow_html=True)
        else:
            st.write("No matching results found.")
    else:
        st.write("Please enter a search query.")
