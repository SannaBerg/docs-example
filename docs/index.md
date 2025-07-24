# Connect to the Google Analytics 4 Reporting API

This guide provides a tutorial on how to set up and use the Google Analytics 4 Data API to access your analytics data programmatically.

This is useful if you want to automate data extraction, integrate analytics data into your applications, or perform advanced data analysis.

## Set Up a Google Cloud Project

To use the Google Analytics API, you need a Google Cloud project with appropriate credentials.

To create a Google Cloud project:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).

2. Click on the **Open Project Picker** button ![alt text](images/open-project-picker-button.png) in the top left corner.

3. Click on the **New Project** button ![alt text](images/new-project-button.png).

4. Enter the following information:
   - **Project name**
   - If applicable, your **Organization**.
   - If applicable, a **Location**.

    ![alt text](images/project-configuration.png)

5. Click **Create** to create the project.

    !!! note If you have several Google accounts, make sure you are logged in with the account that has permission to create projects in your organization and that you want to connect the project to.

## Enable the Google Analytics Data API

To enable the Google Analytics Data API for your project:

1. Click on the **Open Project Picker** button ![alt text](images/open-project-picker-button.png) in the top left corner and select your **new project**.

2. Click on the hamburger menu in the top left corner and select **APIs & Services** > **Enable APIs & Services**.

3. Click on the **+ Enable APIs and Services** button.

4. Enter **Google Analytics Data API** in the search bar and select it from the results.

5. Click **Enable** to enable the API for your project.

## Create a Service Account and Keys

API credentials are required to authenticate your requests.

To create a service account and generate a key:

1.  Click on the hamburger menu in the top left corner and select **IAM & Admin** > **Service Accounts**.

2.  Click the **+ Create Service Account** button.

3.  Enter the following information:
    - **Service account name**
    - **Service account ID**
    - **Service account description**
    
4. Click **Create and Continue**.

5.  Optional, set **Permissions**. Give the account the **Owner Permission**.

6.  Optional, set Principals with access to the service account.

7.  Click **Done** to create the service account.

8.  Click on the newly created service account, for example: **example-documentation@exampledocumentation.iam.gserviceaccount.com**.

9.  Click **Add key** > **Create new key** and select **JSON**. A JSON file with the key is downloaded to your computer.

    !!! warning Make sure that you store the key safely. It will have access to all Google Analytics properties that you grant.

## Grant Access to the Service Account

To allow the service account to access your Google Analytics data, you need to grant it access to the Google Analytics property:

1. Open the Google Analytics 4 property that you want to connect to.
2. Click on **Admin** in the bottom left corner.
3. In the **Property** column, click on **Property Access Management**.
4. Click the **+** button to add a new user.
5. Enter the service account client-email address, for example: **example-documentation@exampledocumentation.iam.gserviceaccount.com**.

    !!! note Feel free to share this email account with business partners or other users that you want to give access to you analytics data. There are no secrets or keys included in the email address.  
