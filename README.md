# Koodausta ja kisailua 2023 backend development repository

Short explanations about how to set up and run the server and tests using VSCode or PyCharm:

## VSCode:

### Creating virtual environment and adding requirements

- Install Python (recommended 3.11 for development)
- Open project in VSCode
- Ensure you have installed the python-extension and activated it
- Open command palette (`Ctrl + Shift + p`)
- Input `Python: Create environment`
- Choose the environment you want to use (venv recommended)
- Choose the interpreter you want to use (python 3.11 recommended)
- Run `pip install -r requirements.txt`

### Running tests

- Run `behave`

### Running the app

- Run `uvicorn src.routes:app --reload`

### Re-activating venv if necessary

- Run `./venv/Scripts/Activate.bat`

## PyCharm:

### Opening project

- Clone the repository and open the folder with PyCharm
- Choose the python interpreter you want to use (python 3.11 recommended)
- PyCharm creates venv and recognizes dependencies automatically

### Running tests

- Go to configurations `Add configuration` or `Edit configurations` (top right, use dropdown if configurations exist)
- From top-left in the pop-up window, choose "+" -> "behave"
- Set `features` as the feature file folder (and add a name to the configuration if you want to)
- Save and run the configuration

### Running the app

- Go to configurations `Add configuration` or Edit configurations (top right, use dropdown if configurations exist)
- From top-left in the pop-up window, choose "+" -> "FastAPI"
- Set `src.routes` as the application file (and add a name to the configuration if you want to)
- Save and run the configuration