# CI/CD for the Lingo web app

## Introduction

Continuous Integration and Continuous Delivery (CI/CD) for the Lingo web app automates the build, test, and deploy processes using Azure DevOps. This ensures consistent build environments, verifies functionality through integration tests, and deploys the app to Azure App Service.

## CI/CD components

- **Azure Key Vault**: Stores keys used by the app, such as Foundry Translator Resource API keys.

- **Dockerfile**: A list of instructions used to build the Docker image. It contains the Python version, the path to `requirements.txt`, and instructions for starting the app.
- **`requirements.txt`**: List of Python packages the app depends on.
- **Azure Container Registry**: Stores Docker images. It is added as a Service Connection to the Azure DevOps project.
- **`test.xml`**: Documentation XML file used during integration tests.
- **Azure App Services**: Host for the web app.
- **`azure-pipelines.yml`**: Defines the build and deployment steps. 
- **Azure Pipeline**: Builds, tests, and deploys your code as defined in **`azure-pipelines.yml`**.

## Pipeline stages

The **`azure-pipelines.yml`** file at the root of the repository defines the pipeline stages.

### Trigger

The pipeline triggers when code merges to the **main** branch. 

### Stage 1: Build

The pipeline downloads the code and runs `docker build`. If successful, the Docker image is pushed to the Azure Container Registry. If the build fails, the pipeline stops, and you can view the details in the error logs.

### Stage 2: Integration test

This stage runs if the build is successful. The `AzureKeyVault@2` task connects to Azure Key Vault to download keys as masked environment variables. The pipeline runs the Docker container locally and calls the local server to translate the **`test.xml`** file. If the test fail, the pipeline stops. Any non-200 HTTP response code fails the stage, you can view the details in the error logs.

### Stage 3: Deployment

After a successful integration test, the pipeline deploys the Docker image to the Azure App Service. 

## Procedures

### View error logs

1. Select **Pipelines** and select the **lingo-azure-pipeline**.
2. In the list of runs, select the failed run marked with a red X. 
3. In the run summary, select the failed job. For example, RunTest. 
4. In the task list, select the failed task, highlighted in red. The log pane displays the console output.

### Set up notifications

To recive an email with a direct link to the error log on failure:
1. Go to **Azure DevOps portal**. 
2. Select **Project Settings** > **Notifications**.
3. Select **New subscription**, and then select **A build fails**. 

### Edit keys

1. Go to **Azure Portal**.
2. Search for and select **Key Vaults**.
3. Filter for **resource-group-lingo** and select the key vault.
4. Do one of the following:
   - To add a key, select **Create a key**.
   - To update a key, select **+ New Version**. 
   - To remove a key, select **Delete**.

### Update build requirements

- **Python version**: Open the **`Dockerfile`** and update the `FROM python:<version>-slim` parameter.

- **Packages**: Open **`requirements.txt`** to add, update, or remove package dependencies.

### Add integration tests

Integration test logic is defined in the **`azure-pipelines.yml`** file.

To expand testing:

- To test a different file or endpoint, append a new command to your existing script block.
   
     ```YML
     - script: |
             # ... (previous docker run logic) ...
   
             echo "Test 1: Standard XML Translation"
             curl -X POST http://localhost:8000/translate \
                 -H "Content-Type: application/xml" \
                 -d @tests/sample.xml --fail
   
             echo "Test 2: Health Check"
             curl -f http://localhost:8000/health || exit 1
     ```

- To test complex logic, add a Python script to the **`tests`** folder. Update the **`azure-pipelines.yml`**  to install Python on the build agent and run the script after the container starts.
   
     ```YML
     - task: UsePythonVersion@0
           inputs:
             versionSpec: '3.x'
   
         - script: |
             # Start container as before
             docker run -d -p 8000:8000 --name test-app -e API_KEY=$(TRANSLATION-API-KEY) $(image)
             sleep 10
             
             # Install dependencies and run the script
             pip install requests
             python tests/integration_test.py
           displayName: 'Run Python Integration Tests'
     ```
