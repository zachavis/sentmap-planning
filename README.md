# SENT-Map Planning

## Install
To run local planning, first [install and run ollama](https://github.com/ollama/ollama).

Then, install the python module in your desired environment
```
pip install ollama
```
and download your desired model, for example gemma2:9b
```
ollama run gemma2:9b
```

## Run single-file planning
For rapid development, a single-file allows quick iteration:
```
python plan_dev.py
```
or with json-verified planning:
```
python plan_dev_json.py
```

## Run multi-file planning:
Track your prompts, scenes, and skill APIs as files:
```
python plan.py --prompt prompt.txt --model gemma2:9b --api api.txt --scene scene.json --verbose --query "get me a fork. Place picked items with me at node 2."
```
or equivalently, assuming default file names:
```
python plan.py -q "get me a fork. Place picked items with me at node 2." -a api.txt -m gemma2:9b -v
```
