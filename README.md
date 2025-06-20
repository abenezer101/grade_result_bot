# Project Documentation

## Project Structure

- **.gitignore**: Specifies intentionally untracked files that Git should ignore.
- **Dockerfile**: Contains instructions to build a Docker image for the project, enabling containerization.
- **LICENSE**: Contains the licensing information for the project, typically specifying how the software can be used and distributed.
- **proc.file**: Declares the commands that are run by the application's dynos on Heroku.
- **python_version_v2.py**: A Python script, likely the main application file or a significant module. (Further analysis of the file content would be needed for a more specific description).
- **requirements.txt**: Lists the Python packages that the project depends on, along with their versions. This file is used to install the necessary dependencies.

## Application Build and Execution Flow

### Dockerfile: Setting up the Environment

The `Dockerfile` is responsible for creating a consistent and reproducible environment for the application. It performs the following steps:

- **Base Image**: It starts from the official `python:3.10` image, providing a Python 3.10 runtime environment.
- **System Updates and Git Installation**: It updates the package lists (`apt update`), upgrades installed packages (`apt upgrade -y`), and installs Git (`apt install git -y`).
- **Dependency Management**:
    - It copies the `requirements.txt` file into the image (`COPY requirements.txt /requirements.txt`).
    - It then installs the Python dependencies listed in `requirements.txt` using pip (`pip install -U pip && pip install -U -r requirements.txt`). The `-U` flag ensures pip itself and the packages are upgraded to their latest versions.
- **Working Directory**: It sets the working directory within the container to `./` (`WORKDIR ./`), meaning subsequent commands will be run from this location.
- **Copying Application Code**: It copies all files from the host machine's current directory (where the Docker build is executed) into the container's working directory (`COPY . .`).
- **Running the Application**: The `CMD ["python", "python_version_v2.py"]` instruction specifies the default command to execute when a container is run from this image. It starts the Python application by running the `python_version_v2.py` script.

### python_version_v2.py: Application Logic

This script contains the core logic for a Telegram bot that interacts with a MySQL database and also includes a basic Flask web application.

#### Telegram Bot Functionality:

- **Initialization**: A Telegram bot is initialized using `telebot.TeleBot` with a specific bot token.
- **Command Handlers**:
    - `/start`: Welcomes the user and displays a custom keyboard with options: 'View grade', 'Help', 'Stats', 'About'. It also adds the user's ID to a `users` set, likely for tracking active users.
    - `/contact_support`: Provides a contact username for support.
    - `/view_grade`: Instructs the user on the format to enter their credentials and subject to view their grade.
    - `/help`: Explains how to use the bot, the required personal details for viewing grades, and how to contact support.
- **Text Message Handlers**:
    - 'View grade': Similar to the `/view_grade` command, it prompts the user for their information.
    - 'Help': Similar to the `/help` command, it provides usage instructions.
    - 'Stats': Displays the number of users currently interacting with the bot (based on the `users` set).
    - 'About': Provides a brief description of the bot's purpose and its creators.
- **User Tracking**: The `users` set is used to keep track of unique user IDs that have interacted with the bot via the `/start` command.

#### Database Interaction:

- **Connection**: The script establishes a connection to a MySQL database hosted on `db4free.net` using the `mysql.connector` library. It uses specific credentials and database name (`opisgradedb`).
- **`fetch_user_result` Function**: This function takes `username`, `password`, and `subject` as input. It constructs and executes an SQL query to select user data from a table named `users` based on these credentials. It returns the first matching row found.
- **Grade Fetching Message Handler**: A message handler (using `regexp=r"^(\w+)\s+(.+)\s+(\w+)$"`) is set up to process messages that match the pattern of three space-separated words (presumably username, password, and subject).
    - It sends a "Please wait" message.
    - It calls `fetch_user_result` to query the database.
    - If credentials are incorrect, it informs the user.
    - If successful, it replies with the user's grade for the specified subject (retrieved from the 4th column, index 3, of the database result: `result[3]`).
    - It then deletes the "Please wait" message.
- **Bot Polling**: `bot.polling()` starts the Telegram bot, continuously checking for new messages.

#### Flask Application:

- **Initialization**: A basic Flask web application is initialized: `app = Flask(__name__)`.
- **`/` Route**: This route (`@app.route('/')`) is defined to return a simple 'Hello World!' string when accessed. This is often used for health checks or as a basic landing page.
- **`/setwebhook` Route**: This route (`@app.route('/setwebhook', methods=['GET', 'POST'])`) is intended to set up a webhook for the Telegram bot. When called, it attempts to set the bot's webhook URL using `bot.setWebhook()`. The `URL` variable used in the original code (`'{URL}/{HOOK}'.format(URL=host, HOOK=bot)`) seems to have a typo (`host` is not defined in that scope, likely meant to be the `URL` variable defined earlier: `"https://opis-results-bot.vercel.app/"`). The `HOOK` part also seems to be incorrectly using the `bot` object itself instead of the bot token.
- **`/{bot_token}` Route (Likely intended for Webhook Updates)**: The route `@app.route('/{}'.format(bot), methods=['GET', 'POST'])` appears to be an attempt to create a dynamic route based on the bot object. However, `format(bot)` would result in the string representation of the `telebot.TeleBot` object, which is not the bot token. This route is likely intended to be `@app.route('/<YOUR_BOT_TOKEN>')` or similar, where Telegram would send updates if a webhook were correctly set up. The handler `respond()` tries to process incoming JSON updates from Telegram. The line `setup().process_update(update)` seems to be a placeholder or an error, as `setup()` is not defined in the provided script.

## How to Run the Application

### Using Docker

The application is containerized using Docker, which simplifies deployment and ensures a consistent environment.

1.  **Build the Docker Image**:
    Navigate to the project's root directory (where the `Dockerfile` is located) and run the following command in your terminal:
    ```bash
    docker build -t opis-results-bot .
    ```
    (You can replace `opis-results-bot` with your preferred image name).

2.  **Run the Docker Container**:
    Once the image is built, you can run the application in a container using:
    ```bash
    docker run opis-results-bot
    ```
    This will start the application, and the Telegram bot should become active. The Flask application will also be running, but its accessibility will depend on how ports are managed if you were to expose them (not explicitly configured in the current `Dockerfile` for external access beyond the container).

### Deployment (Heroku)

The presence of a `proc.file` in the project suggests that it is prepared for deployment on Heroku. The `proc.file` contains:

### Author :

Abenezer Abera

```
bot: python_version_v2.py
```

This line tells Heroku to declare a process type named `bot` and run it using the command `python python_version_v2.py`. When deploying to Heroku, the platform will use this file to understand how to start your application. The `bot` process will execute the main Python script, starting both the Telegram bot and the Flask web server components.
