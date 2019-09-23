- Android sdk (android studio)
- android home path (bashrc)

NODE:
- sudo apt-get install curl
- curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
- sudo apt-get install -y nodejs (node -v, npm -v)

APPIUM:
- sudo npm install -g appium
- npm install wd
- npm install appium-doctor -g

JAVA:
- sudo apt-get purge openjdk-\*
- sudo apt install openjdk-8-jre-headless
- java home path (bashrc)


BASHRC File Data:
- export ANDROID_HOME=$HOME/Android/Sdk
- export PATH=$PATH:$ANDROID_HOME/tools
- export PATH=$PATH:$ANDROID_HOME/platform-tools
- export PATH=$PATH:$ANDROID_HOME/tools/bin
- export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
- export PATH=$PATH:$JAVA_HOME/bin


pip3 install robotframework-appiumlibrary
