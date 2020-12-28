from flask import Flask, render_template, request, make_response, send_from_directory, redirect
import random
import string
import os
import time

import multiprocessing as mp

def uuid(n=20):
  return ''.join(random.sample(string.ascii_letters + string.digits, n))
app = Flask(__name__)

ROOT = os.getcwd()
SHAREROOT = os.path.join(ROOT, "shared")

def add_removal(did, internal = 15*60, dir_ = "remove.txt"):
  with open(os.path.join(ROOT, dir_),"a", encoding="utf-8") as f:
    f.write("{} {}\n".format(did, time.time()+internal))

class Share(object):
  def __init__(self, did, internal = 15*60):
    self.did = did
    self.didRoot = os.path.join(SHAREROOT, did)
    os.mkdir(self.didRoot)
    self.txtFile = os.path.join(self.didRoot, "temp.txt")
    add_removal(did, internal=internal)

  def writeFiles(self, files):
    with open(self.txtFile,"w", encoding="utf-8") as f:
      for file_ in files:
        file_.save("{}/{}".format(self.didRoot, file_.filename))
        f.write("{} {}\n".format(file_.filename, "/download/{}/{}".format(self.did, file_.filename)))    

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home", home_status="active")

@app.route('/upload')
def upload_file():
   return render_template('upload.html', title="Upload", upload=True, upload_status = "active")

@app.route('/download')
def download():
   return render_template('download.html', title="Download", download_status = "active")

@app.route('/list_from_code',methods=['GET',"POST"])
def list_from_code():
  if request.method == 'POST':
    did = request.form.get('code')
    return redirect("/listfiles/"+did)
  return render_template('download.html', title="Download",download_status = "active")


@app.route('/listfiles/<did>')
def listfiles(did):
  if not os.path.isfile(SHAREROOT+"/{}/temp.txt".format(did)):
    return render_template('download.html', title="Download", download_status = "active", alertMSG = "Code NOT Valid")
  files=[]
  with open(SHAREROOT+"/{}/temp.txt".format(did),"r", encoding="utf-8") as f:
    for line in f.readlines():
      name, url = line.split(" ")
      files.append((name.strip(),url.strip()))
  return render_template('filelist.html', title="Download", download_status="active", data = {"files":files})

@app.route("/download/<did>/<filename>", methods=['GET'])
def download_file(did,filename):
    response = make_response(send_from_directory(os.path.join(SHAREROOT,did), filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
  if request.method == 'POST':
    try:
      getDid, getTime = request.form.get("did"), request.form.get("time")
      if not getTime:
        getTime = 15
      getTime = int(float(getTime))
      if not getDid: 
        getDid = uuid()
      
      while os.path.isdir(SHAREROOT+"/"+getDid):
        getDid = getDid+uuid(4)
      did = getDid
      share = Share(did, internal=getTime*60)
      share.writeFiles(request.files.getlist('file'))
      return render_template('upload.html', title = "Share", share=True,upload_status = "active", data = {"share_url":"/listfiles/"+did})
    except Exception as e:
      return render_template('upload.html', title="Upload", upload=True, upload_status = "active", alertMSG="Params Not Valid !")

  return render_template('upload.html', title="Upload", upload=True, upload_status = "active")

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)

 
