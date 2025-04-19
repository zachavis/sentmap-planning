import ollama
import re
import json


def extract_json(text):
    plan_json_text = re.search(r"\{.*\}", text, re.DOTALL)
    return plan_json_text.group(0)

query = "get raj's belongings and bring them to karthik."

model_name = "gemma2:9b"

prompt = '''<SCENE_JSON>
You're an assistant. For each query, use the JSON scene file and respond with a json object with sequential steps in the following format {"number":{"function", "arguments"}} for each step you will call.
You must always goto a node between pick and place. You must place an object before you can pick a new object. You may only use the functions in the api, and you must respect the allowed_actions at each node.
Example:
{
"1": {"function": goto_node, "arguments": "node_100"},
"2": {"function": pick, "arguments": "golf club"},
"3": {"function": goto_node, "arguments": "node_101"},
"4": {"function": place, "arguments": "golf club"},
}
Function API:
<SKILL_API>
Query: <USER_QUERY>'''

api = '''skill_name: goto_node
arguments: node_id
description: The robot navigates to the node with given id
skill_name: pick_object
arguments: object_name
description: The robot uses its gripper to grasp and hold the given object
skill_name: place_object
arguments: object_name
description: The robot places its held object at its current node
skill_name: open
arguments: None
description: The robot opens the node'''

with open("scene.json", 'r') as file: scene = file.read()
prompt = prompt.replace('<SCENE_JSON>', scene).replace('<SKILL_API>', api).replace('<USER_QUERY>', query)
response = ollama.chat(model=model_name, messages=[{'role': 'user','content': prompt,}])
response_json = extract_json(response['message']['content'])
# print(response['message']['content'])

# Convert the JSON string to step-by-step list of actions
try:
    plan_json = json.loads(response_json)
except json.JSONDecodeError as e:
    print(f"LLM response: {response['message']['content']}")
    print(f"Error decoding JSON: {e}")
    exit(1)
    
for step, action in plan_json.items():
    function = action['function']
    arguments = action['arguments']
    print(f"Step {step}: {function}({arguments})")
