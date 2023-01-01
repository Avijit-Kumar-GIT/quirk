import os
import openai
from dotenv import find_dotenv, load_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

openai.api_key = env.get("OPENAI_API_KEY")

def generateSoftware(prompt1):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Generate a list of no-code software apps and why in order to build the following idea: {}. \n \n  ".format(prompt1),
      temperature=0.7,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response['choices'][0]['text']

def generateInsights(prompt1):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Does the following tech stack present any challenges and provide insights on whether any softwares need to be changed: {} \n \n  ".format(prompt1),
      temperature=0.7,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response['choices'][0]['text']


# def blogSectionExpander(prompt1):
#     response = openai.Completion.create(
#       engine="text-davinci-003",
#       prompt="Expand the blog section in to a detailed professional , witty and clever explanation.\n\n {}".format(prompt1),
#       temperature=0.7,
#       max_tokens=200,
#       top_p=1,
#       frequency_penalty=0,
#       presence_penalty=0
#     )

#     return response['choices'][0]['text']