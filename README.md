# IDS706_assignment_02

[![Repository for assignment 2](https://github.com/tonantzin-real/IDS706_assignment_02/actions/workflows/main.yml/badge.svg)](https://github.com/tonantzin-real/IDS706_assignment_02/actions/workflows/main.yml)

This is a repository for [assignment 2](https://canvas.duke.edu/courses/60978/assignments/282604), [assignment 3](https://canvas.duke.edu/courses/60978/assignments/283786) and [assignment 4](https://canvas.duke.edu/courses/60978/assignments/287231):

> Choose a beginner-friendly dataset from sources like Kaggle or public APIs. Perform basic data analysis using Pandas and Polars. This includes:
> 1. importing data
> 2. inspecting it
> 3. applying filters and groupings
> 4. exploring a ML algorithm
> 5. visualizing it

### <ins>DATA</ins>

The data I chose is [**H-1B Employer Data Hub**](https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub?utm_source=chatgpt.com), it comes from the U.S. Citizenship and Immigration Services (USCIS). This database includes:

> data from fiscal year 2009 through fiscal year 2025 (quarter 3) on employers who have submitted petitions to employ H-1B nonimmigrant workers.

> The H-1B Employer Data Hub has data on the first decisions USCIS makes on petitions for initial and continuing employment.

More information about the dataset can be found [here](https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub/understanding-our-h-1b-employer-data-hub).

 I selected the information from fiscal year 2022 until 2025 (Q3).


### <ins>WHAT DID I DO?</ins>
- I cleaned the column names and imputed missing values depending on the column dtype 
> None of the variables had more than 1% of missing values
- For each variable, I looked at its .describe()
- I dropped certain columns
- I cleaned `Industry_NAICS_Code` and saved the result in another column
- I calculated how many approvals and denials there were by fiscal year. I considered all the columns that contained `_Approval` and `_Denial`
> The approval rate for each year was over 96%. This number caught my eye but due to time restrictions I didn't look at it further


![Approval Rate by Fiscal Year](img/lineplot_rate_Approval_Rate.png)

> This was done using **pandas**
- I looked at the Approval Rate for each fiscal year for North Carolina, California and New York
> The 3 states increased their approval rate in 2024

> This was done using **polars**
- For the **modeling** part I ran a simple Random Forest with ChatGPT's help
> The 4 metrics I calculated (accuracy, precision, recall, f1) had a value of 54%-55%

## Assignment 3
The instructions were:
> This assignment is the second part of your two-week project. You will now focus on making your data analysis project reproducible and testable. You’ll write basic unit tests for your data analysis functions and set up a development environment using either Dev Container or Docker. It should be in the same Github Repository you created last week.

1. **Test Coverage:** Includes meaningful unit and system tests that validate core functions such as data loading, filtering, grouping, preprocessing, and machine learning model behavior, with clear structure and edge case handling. Make sure all tests pass.


This was done previously and all the tests passed:

![Passed tests!](img/passed_tests.png)


2. **Dev Environment Setup:** A fully functional Dev Container or Docker setup (3 bonus points for both Docker and Dev Container), with requirement file, devcontainer.json/Docker files, ensuring all dependencies correctly installed and clear instructions for building, running, and using the environment.

The steps for de dev environment setup are the following:


### I. Creating a dev container
**Purpose:** Set up a consistent development environment using Docker containers
1. Press `Cmd + Shift + P` and search for **Dev Containers: Add Dev Container Configuration Files**
2. Select **Add configuration to workspace**
3. Select **Python 3**
4. Select the default Python version (press enter)
5. Select additional features if needed (or nothing)
6. Select optional files to include (or nothing)

> 📁 This creates a `.devcontainer` folder with `devcontainer.json` - the development environment configuration

![devcontainer.json](img/devcontainer_json.png)


### II. Opening the dev container
**Purpose:** Launch and work within the Docker-based *development* environment
1. Click the blue arrows in the lower-left corner of VS Code
2. Select **Reopen in Container**
> This will allow us to *reopen* the container, now in Docker (it will look the same)
> Conversely, once we are in Docker we can reopen the container locally by doing `Cmd + Shift + P` and selecting **Dev Containers: Reopen Folder Locally**
3. Wait for the container to build and start
> VS Code automatically handles the Docker image building and container creation process in the background
> The first time may take several minutes as it downloads the base image and installs dependencies
Subsequent openings will be much faster due to Docker's layer caching

Now on Docker we can see our Container (e.g., `angry_noyce`)
![Container](img/container_docker.png)

### III. Creating a Dockerfile
**Purpose:** Create a production-ready container configuration for deployment
1. Press `Cmd + Shift + P` and select **Containers: Add Docker Files to Workspace**
2. Select **Python: General** in Select Application Platform
3. Select **test_analysis.py** or the main.py for Choose The App's Entry Point
4. Select **No** for Include optional Docker Compose Files
> 🐳 This creates a Dockerfile in your project root - your production container blueprint

### IV. Building an image from Dockerfile
**Purpose:** Create and *deploy* the application as a standalone Docker container
1. In the terminal run `docker build -t image-name .` (e.g., `ids_assignment_3` in our case)
> *Builds a Docker image from your Dockerfile instructions*
3. Run `docker run -d -p 8088:3000 --name container-name image-name` (e.g., `my_container` in our case)
> *Launch a container from your built image with specific settings*
> 🚀 Flags explanation:
> - **-d:** Run in detached mode (background process)
> - **-p 8088:3000:** Map host port 8088 to container port 3000
> - **--name:** Assign a recognizable name to your container

Now the production container is running:
![Created container](img/container_created.png)

And we verified successful execution:
![Container worked](img/container_worked.png)


## Assignment 4

The instructions were:
> This assignment is the second part of your two-week project. You will now focus on making your data analysis project reproducible and testable. You’ll write basic unit tests for your data analysis functions and set up a development environment using either Dev Container or Docker. It should be in the same Github Repository you created last week.

![CI workflow works!](img/workflow_works.png)