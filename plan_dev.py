import ollama

query = "get raj's belongings and bring them to karthik."

model_name = "gemma2:9b"

prompt = '''<SCENE_JSON>
You're an assistant. For each query, use the JSON scene file and reply with the functions from the API which satisfy the query.
You must always goto a node between pick and place. You must place an object before you can pick a new object. You may only use the functions in the api, and you must respect the allowed_actions at each node.
Example:
goto_node("node_100")
pick("golf club")
goto_node("node_101")
place("golf club")
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
print(response['message']['content'])