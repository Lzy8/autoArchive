import os
import subprocess
import argparse
import requests

API_URL = "https://qiniu-storage.pgyer.com/apiv1/app/upload"
UKey = "aa91cfbb99619dbb99a79a60ef61ba86"
API_KEY = "de01fc6cbb5d02c954cf561e996658b9"
DOWNLOAD_URL = "http://www.pgyer.com"

def isUpload():
	if UKey is '' or API_KEY is '':
		return False
	else:
		return True

def parserJSON(responseObject):
	resultCode = responseObject['code']
	if resultCode == 0:
		downUrl = DOWNLOAD_URL +"/"+responseObject['data']['appShortcutUrl']
		print "Upload Success"
		print "DownUrl is:" + downUrl
		print responseObject['data']['appDescription']
	else:
		print "Upload Fail!"
		print "Reason:"+responseObject['message']	

def uploadIPA(path,message):
	print "zy_ipaPath:"+path
	path = os.path.expanduser(path)
	path = unicode(path,"utf-8")
	file = {'file' : open(path,'rb')}
	header = {'enctype' :'multipart/form-data'}
	params = {'uKey':UKey,'_api_key':API_KEY,'installType':1,'password':'','updateDescription':message}
	print "U.P.L.O.A.D.I.N.G....PLEASE..WAIT"

	result = requests.post(API_URL,data = params ,files = file, headers = header)
	if result.status_code == requests.codes.ok:
		responseObject = result.json()
		parserJSON(responseObject)
	else:
		print "zy_upload failed,http errorcode:"+result.status_code

def getExportPath(scheme):
	dateCmd = 'date "+/%Y-%m-%d_%H-%M-%S"'
	process = subprocess.Popen(dateCmd,stdout = subprocess.PIPE, shell = True)
	(stdoutdata,stderrdata) = process.communicate()
	path = "~/Desktop/%s%s" %(scheme,stdoutdata.strip())
	return path

def clearArchive(archivePath):
	cmd = "rm -r %s" %(archivePath)
	process = subprocess.Popen(cmd,shell = True)
	process.wait()
	print "zy_archiveFile removed"

def exportArchive(scheme,archivePath):
	exportPath = getExportPath(scheme)
	exprortCmd = "xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist testbuild/exportOptions.plist" %(archivePath,exportPath)
	process = subprocess.Popen(exprortCmd,shell = True)
	process.wait()

	if process.returncode == 0:
		print "zy_exportArchive success,Path:%s" %(exportPath)
		return exportPath
	else:
		print "zy_exportArchive failed"
		return exportPath

def getBuildArchivePath(archiveName):
	process = subprocess.Popen('pwd',stdout = subprocess.PIPE)
	(stdoutdata,stderrdata) = process.communicate()
	archiveFullName = "%s.xcarchive" %(archiveName)
	archivePath = stdoutdata.strip() + "/" + archiveFullName
	return archivePath

def buildWorkspace(workspace,scheme,message):
	archivePath = getBuildArchivePath(scheme)
	print "zy_archivePath:" + archivePath
	archiveCmd = "xcodebuild -workspace %s -scheme %s -configuration Debug archive -archivePath %s -destination generic/platform=iOS" %(workspace,scheme,archivePath)
	process = subprocess.Popen(archiveCmd,shell = True)
	process.wait()

	code = process.returncode

	if code == 0:
		print "zy_archive %s success" %(workspace)
		ipaPath = exportArchive(scheme,archivePath)
		clearArchive(archivePath)
		if isUpload():
			ipaFullPath = ipaPath + '/' + scheme +'.ipa'
			uploadIPA(ipaFullPath,message)
	else:
		print "zy_archive %s failed" %(workspace)
		clearArchive(archivePath)

def xcbuild(dictionary):
	buildWorkspace(dictionary.workspace,dictionary.scheme,dictionary.message)

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-w','--workspace',help = 'input name of workspace needs to be built')
	parser.add_argument('-s','--scheme',help = 'input name of scheme needs to be built')
	parser.add_argument('-m','--message',help = 'message for build',default = 'archive')
	hashMap = parser.parse_args()
	xcbuild(hashMap)

if __name__ == '__main__':
	main()




