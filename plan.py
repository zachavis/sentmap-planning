import ollama
import json
import re
import sys

llm_model = "gemma3:27b"
scene_json_file = "scene.json" # with SE
# scene_json_file = "scene_noowner.json" # with SE, without ownership
# scene_json_file = "scene_noSE.json" # no SE

try:
    with open(scene_json_file, 'r') as file:
        scene = file.read()
except FileNotFoundError:
    print(f"Error: The scene file '{scene_json_file}' was not found.")

# Check args[1] for query
if len(sys.argv) < 2:
    query = "Get bob's drink and bring it to alice."
else:
    query = sys.argv[1]


prompt = """Environment: 
<SCENE_JSON>

Skill API:
<SKILL_API>

You're a single-armed robot assistant. Your gripper is empty and you're at node_0.
For each query, respond with a sequence of skills which satisfy the query.
You must respect the JSON environment and the JSON skill api.
You must respect the actions at each node.
You can not hold more than one object.
Object ownership is marked with an "owner" tag. No tag means no ownership.
Somebody is at a node if they are in the "people" tag.
"""

api = """{
    "goto_node": {
        "argument": "node_id",
        "description": "The robot navigates to the node with given id"
    },
    "pick": {
        "argument": "object_name",
        "description": "The robot uses its gripper to grasp and hold the given object at its current node"
    },
    "place": {
        "argument": "object_name",
        "description": "The robot places its held object at its current node"
    }
}"""

# Format your prompt
with open(scene_json_file, 'r') as file: scene = json.dumps(json.load(file))
api = json.dumps(json.loads(api))
system_prompt = prompt.replace('<SCENE_JSON>', scene).replace('<SKILL_API>', api)
user_prompt = "Query: <USER_QUERY>".replace('<USER_QUERY>', query)
# print(system_prompt)
# print(user_prompt)
# print("**********")
chat_history = [{'role': 'system','content': system_prompt}, {'role': 'user','content': user_prompt}]


# Query the LLM for a plan
response = ollama.chat(model=llm_model, messages=chat_history, options={"temperature":0.1})
response_text = response['message']['content']
# print(response_text)
# print("**********")

chat_history.append({'role': 'assistant', 'content': response_text})

user_prompt = 'Return a json array of sequential steps in the following format {{"number":step number, "function":function, "argument":argument}} for each step.'
chat_history.append({'role': 'user','content': user_prompt})
response = ollama.chat(model=llm_model, messages=chat_history, options={"temperature":0.1})
response_text = response['message']['content']
# print(response_text)
# print("**********")

# Pull out the full json array ([{step},{step}] from the response (match greedily to get the last closing brace)
match = re.search(r"(\[.*\])", response_text, re.DOTALL)
plan_json_text = match.group(1)

# Convert the JSON string to step-by-step list of actions
try:
    plan_json = json.loads(plan_json_text)
except json.JSONDecodeError as e:
    print(f"LLM response: {response_text}")
    print(f'Extracted JSON: {plan_json_text}')
    print(f"Error decoding JSON: {e}")
    exit(1)
    
# print(f"Plan JSON: {plan_json_text}")
# print(plan_json)
for action in plan_json:
  print(f"{action['number']}. {action['function']}({action['argument']})")