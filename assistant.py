import os
import time

import openai
from dotenv import load_dotenv
from colorama import Fore, Style
from config import ASSISTANT_ID, OPENAI_KEY


def check_run(client, thread_id, run_id):
   while True:
       # Refresh the run object to get the latest status
       run = client.beta.threads.runs.retrieve(
           thread_id=thread_id,
           run_id=run_id
       )

       if run.status == "completed":
           print(f"{Fore.GREEN} Run is completed.{Style.RESET_ALL}")
           break
       elif run.status == "expired":
           print(f"{Fore.RED}Run is expired.{Style.RESET_ALL}")
           break
       else:
           print(f"{Fore.YELLOW} OpenAI: Run is not yet completed. Waiting...{run.status} {Style.RESET_ALL}")
           time.sleep(3)  # Wait for 1 second before checking again


def chat(client, thread, data):
 
       message = client.beta.threads.messages.create(
           thread_id=thread,
           role="user",
           content=data
       )

       run = client.beta.threads.runs.create(
           thread_id=thread,
           assistant_id=ASSISTANT_ID,
           tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
       )

       check_run(client, thread, run.id)

       # Get the latest messages from the thread
       messages = client.beta.threads.messages.list(
           thread_id=thread
       )

       # Get the latest message from the assistant
       assistant_message = messages.data[0].content[0].text.value
       
       #print('messages', messages) 
       print('assistant_message', assistant_message)
   
       return assistant_message    
    



def set_data(data):
       load_dotenv(override=True, dotenv_path=".env")  # take environment variables from .env.
       
       openai.api_key = os.getenv(OPENAI_KEY)
       client = openai.Client(api_key=OPENAI_KEY)

       thread = client.beta.threads.create()

       #chat_loop(client, assistant, thread)
       result = chat(client, thread.id, data)

       json_data = {
            'result': result,
            'thread': thread.id,
            'status': 200
       }

       return json_data 



def set_data_params(data, thread_id):
       load_dotenv(override=True, dotenv_path=".env")  # take environment variables from .env.
       openai.api_key = os.getenv(OPENAI_KEY)
       client = openai.Client(api_key=OPENAI_KEY)

       thread = thread_id 

       result = chat(client, thread, data)
       #print(result)

       json_data = {
              'result': result,
              'thread': thread,
              'status': 200
       } 

      
       return json_data 



