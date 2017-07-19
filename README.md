# autoArchive
>An autobuild ,archive ,and upload to pgyer server script for iOS write by python.
For more information,welcome to my personal tech blog (http://www.liuziyi.win)

![icon](http://www.liuziyi.win/wp-content/uploads/2017/06/Milky-Way-e1497964515420)

# Descprition

- create a folder in your project, named testbuild 
- put autobuild.py into that folder
- put the exportOptions.plist into project
- just workspace available , other types archive is developing...

# Upload

if you want to upload your ipa to pgyer.com , just write UKey and API_KEY in Python Scrpit Variable 'UKey' and 'API_KEY'

# Usage

 - cd into project folder
 - input 'python testbuild/autobuild.py -w projectName.xcworkspace -s projectName'
