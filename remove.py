import os
import time
import shutil
ROOT = os.getcwd()
SHAREROOT = os.path.join(ROOT, "shared")

def remove(dir_ = "remove.txt"):
    data =[]
    if os.path.isfile(os.path.join(ROOT, dir_)):
        with open(os.path.join(ROOT, dir_),"r", encoding="utf-8") as f:
            for line in f.readlines():
                did, t = line.split()
                did, t = did.strip(), float(t.strip())
                if t < time.time():
                    shutil.rmtree(os.path.join(SHAREROOT, did), True)
                else :
                    data.append(line)
                    
        with open(os.path.join(ROOT, dir_),"w", encoding="utf-8") as f:
            f.write("".join(data))

if __name__ == "__main__":
    remove()