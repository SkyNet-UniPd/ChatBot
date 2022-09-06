# SkyNet Chatbot
Progetto Ingegneria del Software 2021-2022, gruppo SkyNet
# PoC SkyNetChatbot

SkyNet Chatbot

## Requirments 
1. Python 3.7.9
2. Node.js and NPM

## Install Packages

Command to install all Python and Node dependencies, to run only when package.json or requirments.txt changes.

```
npm install -g yarn
yarn install 
```

## Launch the Chatbot 

While in Development (locally) on Linux and Mac:

```
yarn run dev 
```

On Windows:
```
yarn run devwin
```

## Execute Tests

Command to run all tests present in the Django Project

```
python3 manage.py test
```

To run the tests specifically within an app module

```
python3 manage.py test specific_test
```
