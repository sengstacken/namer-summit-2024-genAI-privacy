import os
import boto3
import json
import requests
import streamlit as st
from streamlit_cognito_auth import CognitoAuthenticator

pool_id = "us-east-1_zY5zbHuYj"
app_client_id = "4o4m8gg5161fgopqq8au9j9ita"
app_client_secret = "a5nt2pr81lkmee838npjerg9p72pgghp55ahkr64chkc9j07ip8"
kb_id = "K1ILUHJIMQ"
lambda_function_arn = 'arn:aws:lambda:us-east-1:850754977538:function:namer-850754977538-lambda-function'
dynamo_table = 'namer-850754977538-User_corpus_list_association'

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

def get_user_sub(userpoolid, username):
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

def get_corpus_ids(user_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.query(
        TableName=dynamo_table,
        KeyConditionExpression='user_id = :user_id',
        ExpressionAttributeValues={
            ':user_id': {'S': user_id}
        }
    )
    print(response)
    corpus_id_list = []  # Initialize the list
    for item in response['Items']:
        corpus_ids = item.get('corpus_id_list', {}).get('L', [])
        corpus_id_list.extend([corpus_id['S'] for corpus_id in corpus_ids])
    return corpus_id_list

def search_transcript(user_id, kb_id, text, corpus_ids):
    # Initialize the Lambda client
    lambda_client = boto3.client('lambda')

    # Payload for the Lambda function
    payload = json.dumps({
        "userId": sub,
        "knowledgeBaseId": kb_id,
        "text": text, 
        "corpusIds": corpus_ids
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
corpus_ids = get_corpus_ids(sub)
print(corpus_ids)

# Application Front

with st.sidebar:
    st.header("User Information")
    st.markdown("## User")
    st.text(authenticator.get_username())
    st.markdown("## User Id")
    st.text(sub)
    # selected_patient = st.selectbox("Select a patient (or 'All' for all patients)", ['All'] + patient_ids)
    st.button("Logout", "logout_btn", on_click=logout)

st.header("Corpus Search Tool")

# Text input for the search query
query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        # Perform search
        corpus_ids_filter = corpus_ids
        results = search_transcript(sub, kb_id, query, corpus_ids_filter)
        print(results)
        if results:
            st.subheader("Search Results:")
            st.markdown(results, unsafe_allow_html=True)
        else:
            st.write("No matching results found in corpus.")
    else:
        st.write("Please enter a search query.")
