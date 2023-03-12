# Chat Assistant
Simple Dash interface for the ChatGPT API.  
Disclaimer: This app was created to to explore OpenAI API and is an unofficial project intended for personal learning and research purposes.  
## Current Features
* Runs locally
* [OpenAI won't use data submitted over the API for training and will only retain the data for 30 days](https://platform.openai.com/docs/guides/chat/faq)

![Alt text](/screenshots/app_img.png?raw=true)

### TODO

* Error handling
* Saving of conversations locally
* Switching between gpt-3.5-turbo and other models during a conversation.

## Running locally

These are the steps to get started with the app:
1. Clone the repository.
2. Create the virtual environment using conda. The basic commads are as follows: 
    * Navigate to project folder and run the command below to the create conda environment which reads the environment.yml file.  
    ``` conda env create ```  
    * Activate the virtual environment  with
    ```conda activate chat-env```
    * Install the packages using poetry (retry if it fails)
    ``` poetry install -vvv  ```
    * To update the packages 
   ``` poetry update ```
    * To remove the env
   ``` conda env remove --name chat-env ```
   * The interpreter path can be found by tying  ```which python```

3. Once the environment is activated you can run the app by navigating to the **app** folder and run the command ```python main.py``` . If everything is fine you should see that flask is starting up and that you can request the welcome page on the specified port on localhost.  


### Generate OpenAI API Key

Go to https://platform.openai.com/account/api-keys and click "Create new secret key" and record the key for later.
Add the key in app/config called .env (see .env.example)

## Acknowledgments
This project takes inspiration from:  

* https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-gpt3-chatbot
* https://github.com/lencx/ChatGPT
* https://github.com/borge12/simple-chat
