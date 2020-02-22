import os
import io
import json
import sys

#base = os.path.normpath("C:/Root/Apps/@V/@Tools/firestore-leveldb-tools/Main/Examples/Example1/2020-02-21T00_55_20_68273/all_namespaces/all_kinds")
base = os.path.normpath(sys.argv[1])

#repoRoot = os.getcwd()
repoRoot = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(repoRoot, 'SDKs/google_appengine'))
sys.path.append(os.path.join(repoRoot, 'SDKs/google-cloud-sdk/lib/third_party'))

from google.appengine.api.files import records
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore

def default(obj):
  """Default JSON serializer."""
  import calendar, datetime

  #print("Obj:" + obj)

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


items = []


outPath = os.path.join(base, 'Data.json')
out = open(outPath, 'w')
#out.write("{")
out.write("[")

for filename in os.listdir(base):
  if not filename.startswith("output-"): continue
  #if not filename.startswith("output-5"): continue
  
  print("Reading from:" + filename)
  #out.write('"' + filename + '": [\n')
  
  inPath = os.path.join(base, filename)
  raw = open(inPath, 'rb')
  reader = records.RecordsReader(raw)
  for recordIndex, record in enumerate(reader):
    entity_proto = entity_pb.EntityProto(contents=record)
    entity = datastore.Entity.FromPb(entity_proto)
    # print entity
    items.append(entity)
    print("Writing " + str(len(items)) + " items to file")
    out.write("\n\t" + json.dumps(entity, default=default, encoding='latin-1') + ",")

  #out.write("]\n\n\n")

#out.write("}")
out.write("]")

out.close()