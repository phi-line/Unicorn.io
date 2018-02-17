
import re

dictionary = {
  "big data": ["scalable", "scalability", "big", "data", "sql", "mongodb", "python","cloud", \
    "mining"],
  "software": ["object","oriented","system","design","scalable","database","systems", \
    "object-oriented","algorithm","software","debugging","debug","architecture", \
    "java","python","c++","application","algorithms","stack"],
  "web": ["es6","es5","eslint","javascript","typescript","ajax","react","reactjs", \
    "angular","angularjs","http","web","website","websites","node","js","html","css","nodejs"],
  "mobile": ["ios","android","objective-c","native","swift","mobile"],
  "hardware": ["arduino","matlab","raspberry","c","c++"],
  "security": ["cyber","security","defense","operating","kernel","thread","process"],
  "finance": ["cryptocurrency","bitcoin","blockchain","trading","quant"]
}

def tokenize(text):
  clean_string = re.sub('[^a-z0-9- ]', ' ', text.lower())
  tokens = clean_string.split()
  return tokens

def index(tokens):
  mp = {}
  for t in tokens:
    for k,v in dictionary.items():
      if t in v:
        mp[k] = mp.get(k, 0) + 1 
  return mp


def main(file_name='outputtext.txt'):
  with open('parse/' + file_name, 'r') as f:
    text = f.read()
    f.close()
  tokenized = tokenize(text)
  indexed = index(tokenized)
  return indexed

if __name__ == "__main__":
  main()