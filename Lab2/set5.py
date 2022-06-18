import json

""" #es 1
json_obj = '{ "Name":"David", "Class":"I", "Age":6 }'
p_obj = json.loads(json_obj)
print(p_obj)
print("\nName: ", p_obj["Name"], "Class: ", p_obj["Class"], "Age: ", p_obj["Age"])
"""
""" #es 2
p2_obj = {"name": "albert", "class": "B", "Age": 5}
print(type(p2_obj))
print(p2_obj)
j_data = json.dumps(p2_obj)
print(j_data)
"""
""" #es4
j_str = {"4": 5, "6": 7, "1": 3, "2": 4}
print("Original String : ", j_str)
print("\nJSON data : ")
print(json.dumps(j_str, sort_keys=True, indent=4))
"""
#es5
with open("../resources/states.json") as f:
    state_data = json.load(f)
print(state_data)
print("original json keys: ", state_data["states"][0].keys())
for state in state_data["states"]:
    del state["area_codes"]
print("modified json keys", state_data["states"][0].keys())
with open("../resources/newstates.json", "w") as f:
    json.dump(state_data, f, indent=2)
