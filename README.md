# autoArchive
an autobuild ,archive ,and upload to pgyer server script for iOS write by python

# Descprition

- create a folder in your project, named testbuild 
- put autobuild into that folder
- put the exportOptions.plist into project
- just workspace available , other types archive is developing...

# Upload

if you want to upload your ipa to pgyer.com , just write UKey and API_KEY in Python Scrpit Variable 'UKey' adn 'API_KEY'

# Usage

 - cd into project folder
 - input 'python testbuild/autobuild.py -w projectName.xcworkspace -s projectName'
