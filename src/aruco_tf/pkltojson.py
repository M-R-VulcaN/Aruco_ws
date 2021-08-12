import pickle

# with open('calib_mtx.pkl', 'rb') as f:
#     mtx = pickle.load(f)
# with open('calib_dist.pkl', 'rb') as f:
#     dist = pickle.load(f)

# print(type(dist),' dist: ',dist)
# print(type(dist),' mtx: ',mtx)


# import json

# # Writing a JSON file
# with open('mtx.json', 'w') as f:
#     json.dump(mtx.tolist(), f)

# # Reading a JSON file
# with open('mtx.json', 'r') as f:
#     data = json.load(f)
#     print("data:", data)


import json
from json import JSONEncoder
import numpy

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

with open('calib_mtx.pkl', 'rb') as f:
    numpyArrayOne = pickle.load(f)
# numpyArrayOne = numpy.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])

# Serialization
numpyData = {"array": numpyArrayOne}
encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
print("Printing JSON serialized NumPy array")
print(encodedNumpyData)

# Deserialization
print("Decode JSON serialized NumPy array")
decodedArrays = json.loads(encodedNumpyData)

finalNumpyArray = numpy.asarray(decodedArrays["array"])
print("NumPy Array")
print(finalNumpyArray)

# # Writing a JSON file
# with open('mtx.json', 'w') as f:
#     json.dump(finalNumpyArray, f)

# # Reading a JSON file
# with open('mtx.json', 'r') as encodedNumpyData:
#     decodedArrays = json.load(encodedNumpyData)
# print("data:", decodedArrays)

# numpyData = {"array": numpyArrayOne}
# encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
# print("Printing JSON serialized NumPy array")
# print(encodedNumpyData)

# # Deserialization
# print("Decode JSON serialized NumPy array")
# decodedArrays = json.loads(encodedNumpyData)

# finalNumpyArray = numpy.asarray(decodedArrays["array"])
# print("NumPy Array")
# print(finalNumpyArray)