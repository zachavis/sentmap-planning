import ollama
import json
import argparse

def LoadJSON(json_path):
    """Loads JSON as a dictionary"""
    with open(json_path, 'r') as file:
        data = json.load(file)
        return data

def Plan(prompt, model_name):
    response = ollama.chat(model=model_name, messages=[{'role':'user', 'content':prompt}])
    return response['message']['content']

def ParseJSON(scene_json):
    return json.dumps(LoadJSON(scene_json))

def ParseTXT(file_path):
    with open(file_path, 'r') as file:
        content = "".join(file.readlines())
    return content

def main():
    parser = argparse.ArgumentParser(description="Planning over scene JSON.")
    parser.add_argument('-s', '--scene',  type=str, help='Initial scene', default="scene.json")
    parser.add_argument('-p', '--prompt', type=str, help='Task prompt',   default="prompt.txt")
    parser.add_argument('-m', '--model',  type=str, help='Model name',    default="gemma2:9b")
    parser.add_argument('-a', '--api',    type=str, help='Funciton API',  required=False)
    parser.add_argument('-q', '--query',  type=str, help='User query',    required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Enables extra output')
    args = parser.parse_args()
    
    # Build Prompt
    prompt = ParseTXT(args.prompt)
    scene = ParseJSON(args.scene)
    skill_api = ParseTXT(args.api) if args.api else ""
    prompt = prompt.replace('<SCENE_JSON>', scene).replace('<SKILL_API>', skill_api).replace('<USER_QUERY>', args.query)
    if args.verbose:
        print(f"{prompt}")

    # Run LLM inference
    response = Plan(prompt, args.model)
    print(response)

if __name__ == "__main__":
    main()