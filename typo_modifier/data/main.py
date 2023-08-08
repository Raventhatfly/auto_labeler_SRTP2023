import json
import os
def main():
     path = os.getcwd()
     print(path)
     question = "Does the perosn look happy?"
     for i in list(os.walk(path)):
          root, dirs, files = i

          for file in files:
               if file[-5:] == '.json':

                    full_path = os.path.join(root,file)
                    print(full_path)
                    content = {}
                    with open(full_path,'r') as f:
                         content = json.load(f)
                         for record in content["breakpoint"]:
                              if(record["question"] == question):
                                   record["question"] = "Does the person look happy?"

                    with open(full_path,'w') as f:
                         json.dump(content,f,indent=1)

if __name__ == '__main__':
    main()