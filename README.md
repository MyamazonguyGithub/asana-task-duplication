# Duplicate Task with Error Handling

## Overview

This script automates the process of duplicating tasks across all Asana project (with error handling). It pulls Asana links from Hubspot for Active Full Service & PPC clients. Those links are then parsed for the board GID will duplicate a specified task to each ASANA board identified.

NOTE: Last 3 lines are commented out to prevent accidental runs. Remove # from last three lines to initiate.

## Features

- Automates the duplication of tasks.
- Handles errors during the duplication process.

## Installation

1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Replace `.env` file location with local files location path. 

   ```bash
   load_dotenv('C:\\Users\\PATH\\asana-task-duplication.env')
   ```

Replace `<Task GID>` with the GID of the task to be duplicated in the `duplicate_checkin_task` function 

   ```bash
   def duplicate_checkin_task(name):
       url = "https://app.asana.com/api/1.0/tasks/<Task GID>/duplicate"
   ```


When ready to create new tasks, uncomment last 3 lines by removing `#` to run. 


   ```bash
        #client_task = duplicate_checkin_task(client['properties']['name'])
        #client_task_gid = client_task['new_task']['gid']
        #add_project(client_task_gid, asana_project_gid)
   ```

`Note: Running after this step will result in the specified task being duplicated across ALL Active Client Asana boards.`

`Avoid improper task creation by testing any modifications with # applied to the lines above.`






Run the script to start the task duplication process:

   ```bash
   python asana-task-duplication.py
   ```

The script uses functions for specific API interactions and error handling tasks.

## Contribution

This is a private repository. To implement changes:

1. **Create a Branch**: Before making your changes, create a new branch from the main branch. Name it appropriately related to the feature or fix you're working on:

    ```bash
    git checkout -b feature/<your-feature-name>
    ```

2. **Make Changes**: Implement your changes or additions in your branch.

3. **Test Your Changes**: Ensure that your changes do not break existing functionality.

4. **Commit Changes**: Add and commit your changes. Make sure your commit messages are clear:

    ```bash
    git add .
    git commit -m "Add a detailed commit message describing the change"
    ```

5. **Push Changes**: Push your branch to the repository:

    ```bash
    git push origin feature/<your-feature-name>
    ```

6. **Open a Pull Request (PR)**: Go to the repository on GitHub, you'll see a 'Compare & pull request' button for your branch. Click it, review the changes, and then create the pull request.

7. **Code Review**: Wait for the internal review process. Make any required updates. The repository manager will merge it once it is approved.

## License

This project is proprietary. Unauthorized copying, modification, distribution, or use is not allowed.
