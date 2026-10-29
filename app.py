

import os 
import json

from dotenv import load_dotenv
from google import genai

from weather_tool import get_weather

load_dotenv()

client=genai.client(
    api_key=os.getenv("GEMINI_API_KEY")
)

weather_tool={
    "type":"function", 
    "name":"get_weather",
    "description":("Get the current weather for a city in the world"),
    "parameters":{
        "type":"object",
        "properties":{
            "city":{
                "type":"string",
                "description":"The city to check, such as Nairobi or London."
            }
        },
        "required":["city"]
    }
}

def chat_with_ai(message):

    response=client.interactions.create(
        model="gemini-3.6-flash",input=message,tools=[weather_tool]
                                        )
 
    #look for a tool call requested by Gemini
    for item in response.outputs:
        if item.type=="function_call":
           if item.name =="get_weather":
               arguments=item.arguments
               if isinstance(arguments,str):
                arguments=json.loads(arguments)
               city=arguments["city"]

               #Execute our python weather function
               weather=get_weather(city)

               print("\n Weather tool result: ")
               print(weather)
