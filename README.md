# AWS Workshop: Privacy-Preserving RAG Architecture with Amazon Bedrock

## Objective

In this workshop, we will guide participants through the process of developing a **Privacy-Preserving Retrieval-Augmented Generation (RAG) architecture** using **Amazon Bedrock Knowledge Bases**. The architecture will demonstrate key concepts of securing and managing access to data and services in a cloud-native environment. Specifically, we will focus on:

- **Metadata Filtering for Access Control:** We will show how to apply metadata-based filtering to ensure that document retrieval is restricted to only those documents that each user is authorized to access.
- **VPC Endpoint Integration:** Participants will learn how to connect their VPC and associated resources to communicate directly with the Bedrock API using VPC endpoints. This ensures that all API calls remain private within your VPC and do not traverse the public internet.

By the end of the workshop, participants will have hands-on experience with securely integrating a Bedrock Knowledge Base into a VPC architecture that maintains user privacy and access control at both the data and network levels.

---

## Pre-Provisioned Infrastructure

The following AWS resources have been pre-provisioned in your account:

- **IAM Roles:**
  - **Participant Execution Role:** This role will be used to execute various workshop actions.
  - **Lambda Function Execution Role:** Provides the permissions needed for Lambda functions to access other AWS services.
  - **Knowledge Base Role:** Grants access to the Amazon Bedrock Knowledge Base for managing and retrieving documents.

- **VPC (Virtual Private Cloud):**
  - **Internet Gateway** for internet access.
  - **Public Subnet x2** for resources that require public access.
  - **Private Subnet x2** for internal resources.
  - **NAT Gateway** for secure outbound internet access from private subnets.
  - **Route Tables** for configuring network traffic in each subnet.
  - **Security Groups** to control inbound and outbound traffic at the subnet and VPC levels.
  - **VPC Endpoint Security Group** for restricting access to VPC endpoints.

- **AWS Services:**
  - **SageMaker Notebook:** Used in this workshop to access a Jupyter Notebook interface. We are not utilizing SageMaker’s training, processing, or inference functionalities.
  - **Cognito User Pool:** For user authentication and access control.
  - **DynamoDB Table:** To store metadata and other data relevant to the workshop.
  - **S3 Bucket:** For storing documents and resources that will be accessed by the knowledge base.
  - **Lambda Function:** For executing serverless actions during the workshop.

---

## Workshop Steps

### Step 1: Configure Model Access on Amazon Bedrock

In this step, we will configure model access to ensure you have access to the necessary machine learning models for document retrieval and processing.

1. Navigate to the **Bedrock** homepage within the AWS Console.
2. From the left-hand navigation pane, select **Model access**.
3. Click on **Modify model access** and select the following models:
   - **Titan Text Embeddings V2**
   - **Claude 3 Sonnet**
4. Click **Next**, then **Submit**.
5. After submitting, refresh the page. Model access should be granted within approximately 60 seconds.

### Step 2: Access the SageMaker Notebook

The SageMaker Notebook will be used to interact with the pre-provisioned Jupyter notebook, which contains the code and instructions for developing the privacy-preserving RAG architecture.

1. Navigate to the **SageMaker** homepage within the AWS Console.
2. From the left navigation pane, select **Notebooks**.
3. Under **Actions**, click **Open JupyterLab**. This will open a new tab with the SageMaker-hosted Jupyter environment.
4. In the file explorer, double-click on the `kb-end-to-end.ipynb` notebook to open and begin interacting with the notebook.

---

## Architecture Details

### 1. Privacy-Preserving Retrieval-Augmented Generation (RAG)

In this architecture, we will use **Amazon Bedrock Knowledge Bases** to develop a retrieval-augmented generation system that respects user privacy. The primary method for protecting privacy is through **metadata filtering**. Each document stored in the Knowledge Base will be tagged with metadata specifying the users or groups who have access to that document. During retrieval, the system will apply filters to ensure that only documents a user is authorized to access will be returned.

Key benefits of this approach:

- **Fine-grained Access Control:** Metadata allows for highly specific rules to control document visibility, reducing the risk of unauthorized access.
- **Scalability:** This architecture scales well across different user roles and document sets.

### 2. VPC Endpoint for Amazon Bedrock API

We will configure a **VPC Endpoint** to allow the VPC and its associated resources (like the Lambda function, SageMaker notebook, etc.) to communicate directly with the Bedrock API. This configuration ensures that:

- All traffic between your resources and the Bedrock API remains within your VPC, adding a layer of privacy and security.
- No public internet exposure is required to access Bedrock services.

---

## Conclusion

By the end of this workshop, you will have successfully built a privacy-preserving RAG architecture using Amazon Bedrock Knowledge Bases. You will understand how to apply metadata-based filtering for access control, securely connect your VPC resources to the Bedrock API, and use VPC endpoint policies to further secure access to the API.

Feel free to explore the SageMaker notebook and experiment with the different components of this architecture to deepen your understanding of the privacy and security features within the AWS ecosystem.
