### Install Android Studio And Android SDK:
- Download Android Studio from "https://developer.android.com/studio?gclid=EAIaIQobChMI6Z2LhJ7p5AIVwQorCh11NAdNEAAYASAAEgIzUPD_BwE" it will ask uou for android sdk path, after providing path it will download android sdk over that path.

### Install Node:
- sudo apt-get install curl
- curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
- sudo apt-get install -y nodejs 
- To check node and npm version: node -v, npm -v

### Install Appium:
- sudo npm install -g appium
- npm install wd
- npm install appium-doctor -g

### Install JAVA 8:
- sudo apt-get purge openjdk-\*
- sudo apt install openjdk-8-jre-headless

### Add Android SDK and JAVA PATH to bashrc File Data
- export ANDROID_HOME=$HOME/Android/Sdk (your android sdk path)
- export PATH=$PATH:$ANDROID_HOME/tools
- export PATH=$PATH:$ANDROID_HOME/platform-tools
- export PATH=$PATH:$ANDROID_HOME/tools/bin
- export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
- export PATH=$PATH:$JAVA_HOME/bin

### Install Robot Framework Appium Library
- pip3 install robotframework-appiumlibrary
