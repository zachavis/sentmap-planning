# SENT-Map Planning

This is code supporting "SENT-Map: Semantically Enhanced Topological Maps with Foundation Models," presented at the ICRA'25 Workshop on Foundation Models and Neuro-Symbolic AI for Robotics.

[Project Site](https://rpm-lab-umn.github.io/SENT_map/)

[Workshop Site](https://sairlab.org/icra25/)

## Install
To run local planning, first [install and run ollama](https://github.com/ollama/ollama).

Then, install the python module in your desired environment
```
pip install ollama
```
and download your desired model, for example gemma3:27b
```
ollama run gemma3:27b
```

## Planning
Once gemma3:27b (or desired FM) is downloaded, you can plan with:
```
python plan.py "<USER QUERY>"
```
To change the scene json, or planning FM, edit `plan.py`.
