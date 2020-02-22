import os
import io
import json
import sys

# command-line arguments
backupFolder = os.path.normpath(sys.argv[1])

#repoRoot = os.getcwd()
repoRoot = os.path.dirname(os.path.realpath(__file__))

# import google sdks
sys.path.append(os.path.join(repoRoot, 'SDKs/google_appengine'))
sys.path.append(os.path.join(repoRoot, 'SDKs/google-cloud-sdk/lib/third_party'))
from google.appengine.api.files import records
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore

def GetCollectionInJSONTreeForProtoEntity(jsonTree, entity_proto):
  result = jsonTree
  for element in entity_proto.key().path().element_list():
    nextKey = None
    if element.has_type(): nextKey = element.type()
    elif element.has_name(): nextKey = element.name()
    #elif element.has_id(): nextKey = element.id()

    if nextKey is not None:
      if nextKey not in result:
        result[nextKey] = {}
      result = result[nextKey]
  return result
'''
def GetCollectionOfProtoEntity(entity_proto):
  # reverse path-elements, so we always get last collection
  for element in entity_proto.key().path().element_list():
    if element.has_type(): return element.type()
'''
def GetKeyOfProtoEntity(entity_proto):
  # reverse path-elements, so we always get last key
  for element in reversed(entity_proto.key().path().element_list()):
    if element.has_name(): return element.name()
    #if element.has_id(): return element.id()
def GetValueOfProtoEntity(entity_proto):
  return datastore.Entity.FromPb(entity_proto)

def Start():
  jsonTree = {}
  items = []

  for filename in os.listdir(backupFolder):
    if not filename.startswith("output-"): continue
    print("Reading from:" + filename)
    
    inPath = os.path.join(backupFolder, filename)
    raw = open(inPath, 'rb')
    reader = records.RecordsReader(raw)
    for recordIndex, record in enumerate(reader):
      entity_proto = entity_pb.EntityProto(contents=record)

      #collection = GetCollectionOfProtoEntity(entity_proto)
      collectionInJSONTree = GetCollectionInJSONTreeForProtoEntity(jsonTree, entity_proto)
      key = GetKeyOfProtoEntity(entity_proto)
      entity = GetValueOfProtoEntity(entity_proto)

      collectionInJSONTree[key] = entity
      items.append(entity) # also add to flat list, so we know the total item count

      print("Parsing document #" + str(len(items)))
      
  outPath = os.path.join(backupFolder, 'Data.json')
  out = open(outPath, 'w')
  out.write(json.dumps(jsonTree, default=JsonSerializeFunc, encoding='latin-1', indent=2))
  out.close()
  print("JSON file written to: " + outPath)

def JsonSerializeFunc(obj):
  import calendar, datetime

  if isinstance(obj, datetime.datetime):
    if obj.utcoffset() is not None:
      obj = obj - obj.utcoffset()
    millis = int(
      calendar.timegm(obj.timetuple()) * 1000 +
      obj.microsecond / 1000
    )
    return millis
  #raise TypeError('Not sure how to serialize %s' % (obj,))
  return str(obj)

Start()