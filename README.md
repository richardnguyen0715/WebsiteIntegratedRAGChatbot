# DV-ClassPro-FinalProject
---
## Quick Guide
1. Install kaggle library: `pip install kaggle`.
2. Get the kaggle API Token to use in data collection step.

   2.1 *Login to Kaggle*:

   - Go to the [Kaggle](https://www.kaggle.com/) homepage and log in to your account.

   2.2 *Download API Token*:

   - Click on your profile picture in the upper right corner and select **"My Account"**.

   - Scroll down to the **"API"** section, then click the **"Create New API Token"** button.

   - A file named `kaggle.json` will be downloaded. This file contains the authentication information (username and API key).

   2.3 *Put `kaggle.json` in the right place*:
    - **Linux/MacOS**:
        - Create a hidden folder `.kaggle` in your root directory (if it doesn't exist already):
           ```bash
           mkdir ~/.kaggle
           ```
      - Move the `kaggle.json` file into the `.kaggle` folder:
           ```bash
           mv /path/to/kaggle.json ~/.kaggle/
           ```
      - Set permissions for the file:
           ```bash
           chmod 600 ~/.kaggle/kaggle.json
               ```
   - **Windows**:
     - Move the `kaggle.json` file into the folder:
       ```
       C:\Users\<YourUsername>\.kaggle\kaggle.json
       ```
     - If the `.kaggle` folder does not exist, create it manually.
3. Run Data Collection: `Source\DataCollection\DataCollection.ipynb`
4. Run Data Preprocessing: `Source\DataPreProcessing\DataPreprocessing.ipynb`
5. Run Data Exploration:\
   5.1 `Source\DataExploration\DataExploration_01.ipynb`\
   5.2 `Source\DataExploration\DataExploration_02.ipynb`\
   5.3 `Source\DataExploration\DataExploration_03.ipynb`
7. Run Dashboard.\
   6.1 `Source\DashboardSource\main.py`

## Repository Introducing:

### **Teamwork Policy:**
    1. Github policy: Rules when making commits on git.
    2. Nameing policy: General naming principles for projects.
### **Dataset folder:**
    1. google.csv: First download dataset.
    2. google_processed.csv: The data set after preprocessing will be used for the next steps.
### **Requirement folder:**
    Requirements to be implemented in this project.
### **Source folder:** 
    1. Libraries: These are libraries that are commonly used for tasks in the process.
    2. Shared_Functions: Functions that are shared by the entire process, such as reading, writing, getting path, etc.
    3. DataCollection&PreProcessing folder:
       3.1 Data Collection: Go through the steps of downloading the dataset to your device.
       3.2 Data Preprocessing: Perform preprocessing tasks such as checking for missing values, checking data correctness,...
    4. Data Exploration folder:
        4.1 DataExploration_01.ipynb - Section 01.
        4.2 DataExploration_02.ipynb - Section 02.
        4.3 DataExploration_03.ipynb - Section 03.
    5. Dashboard:
        5.1 ...
    6. AI Source:
        6.1 ...
