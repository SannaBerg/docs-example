# CI/CD for the Translator web app

## Introduction

The Continuous Integration and Continuous Delivery (CI/CD) pipeline for the Translator web app automates the build, test, and deploy processes using Azure services. It ensures consistent build environments, verifies functionality through integration tests, and continuously deploys the app to Azure App Service.

## CI/CD components

Files at the root of the repository:
       
  - **`azure-pipelines.yml`**: Defines the CI/CD pipeline, including its stages, jobs, steps, triggers, and configuration.
  - **`Dockerfile`**: Specifies how to build the Docker image, including the Python version, the path to `requirements.txt`, and the app's startup commands.
  - **`requirements.txt`**: Lists the Python packages the app depends on.
  - **`test.xml`**: Documentation XML file used during integration tests.

Azure services:

- **Azure Pipelines**: Builds, tests, and deploys the code as defined in `azure-pipelines.yml`.
- **Azure Key Vault**: Stores the app’s keys and secrets, such as the Foundry Translator Resource API key.
- **Azure Container Registry**: Stores Docker images. Added as a Service Connection to the Azure DevOps project.
- **Azure App Services**: Hosts the web app.

See [Read more](#read-more) for additional details about these services and concepts.

## Pipeline stages

The `azure-pipelines.yml` file defines the pipeline stages.

### Trigger

The pipeline triggers when code is merged to the `main` branch. 

### Stage 1: Build

The pipeline downloads the code and runs `docker build`. If successful, the Docker image is pushed to the Azure Container Registry. If the build fails, the pipeline stops, and you can view the details in the [pipeline logs](#troubleshoot-pipeline-failures).

### Stage 2: Integration test

This stage runs if the build is successful. The `AzureKeyVault@2` task connects to Azure Key Vault and download the required keys as masked environment variables. The pipeline then runs the Docker container locally followed by the tests in the `script` blocks. For information on what each test does, see comments in `azure-pipelines.yml`. If any test fails, the pipeline stops, and you can view the details in the [pipeline logs](#troubleshoot-pipeline-failures). 

### Stage 3: Deployment

After a successful integration test, the pipeline deploys the Docker image to the Azure App Service. 

## Procedures

### Troubleshoot pipeline failures

To identify and fix pipeline failures:

1. Sign in to the **[Azure DevOps](https://dev.azure.com/)** portal. 
2. Select **Pipelines**.
3. Select **translator-azure-pipeline**.
4. In the list of runs, select the failed run, marked with a red X. 
5. In the run summary, select the failed job.
6. In the task list, select the failed task, highlighted in red. The log pane displays the console output.

### Set up notifications for pipeline failures

To receive an email with a direct link to the failed pipeline run:

1. Sign in to the **[Azure DevOps](https://dev.azure.com/)** portal.  
2. Select **Project Settings** > **Notifications**.
3. Select **+ New subscription**.
4. Select **A build fails** as the **Template**, and then select **Next**.
5. Select **Finish**.

### Edit app keys

To update, add, or remove app keys:

1. Sign in to the **[Microsoft Azure](https://portal.azure.com/)** portal.
2. Search for and select **Key Vaults**.
3. Filter for **resource-group-translator** and select the key vault.
4. Do one of the following:
   - **Add a key**: Select **Create a key**.
   - **Update a key**: Select **+ New Version**. 
   - **Remove a key**: Select **Delete**.

### Update build requirements

- **Python version**: Open the `Dockerfile` and update the `FROM python:<version>-slim` parameter.

- **Packages**: Open `requirements.txt` to add, update, or remove package dependencies.

### Add integration tests

Integration test logic is defined in the `azure-pipelines.yml` file.

To test additional files or endpoints:

1. Locate the `script` block that contains the `# Test endpoints` comment.
2. Add the new test in that `script`  block. Follow the `echo` and `curl` pattern used in `"Test 1: Standard XML Translation"` and `"Test 2: Health Check"`.

Example:
```YML
- script: |
   # Test endpoints
   # ... (Docker run logic) ...

   # Tests the translate endpoint passing the test.xml file. Any non-200 HTTP response fails this stage.    
   echo "Test 1: Standard XML Translation"
   curl -X POST http://localhost:8000/translate \
      -H "Content-Type: application/xml" \
      -d @tests/test.xml --fail

   echo "Test 2: Health Check"
   curl -f http://localhost:8000/health || exit 1
```

To test complex logic: 

1. Add a Python script to the `tests` folder in the repository.
2. Add a new `script` block in `azure-pipelines.yml` with commands to install Python on the build agent and run your script after the container starts. Follow the pattern used for `task: UsePythonVersion@0`.

Example:
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

## Read More

- [Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops)
- [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/)
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Azure App Services](https://learn.microsoft.com/en-us/azure/app-service/)
- [Docker, Building an image](https://docs.docker.com/get-started/docker-concepts/building-images/)
