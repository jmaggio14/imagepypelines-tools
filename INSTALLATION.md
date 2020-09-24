# Developer Installation

#### Points of Contact:

Jeff Maggio   - jmaggio14@gmail.com

Ryan Hartzell - rah3156@rit.edu


## Intro

This document is meant for use by developers who would like to install the project from source. There are many ways to install imagepypelines, imagepypelines-tools and its plugins from source, however we will only show a few known to simplify the process.

## 1) Clone repos

Bear in mind that imagepypelines refers to the ImagePypelines core repo, with access to Blocks and Pipelines, and support for scientific code, while imagepypelines-tools refers to the ImagePypelines *support* repo, which contains numerous helpful scripts and a CLI for starting and testing the ImagePypelines Dashboard or managing ImagePypelines docker containers, to name a few functions.

```bash
git clone "https://github.com/jmaggio14/imagepypelines.git"

git clone "https://github.com/jmaggio14/imagepypelines-tools.git"
```
This will create two directories called imagepypelines and imagepypelines-tools respectively.

## 2) Create virtual environment

Here are two easy ways to set up a virtual environment for running ImagePypelines related applications and scripts:

1) Use the venv module available in Python (make sure to specify which system python to use if you have multiple! i.e. X = 8 if you want to use python3.8)
```bash
# to create the virtual environment
python3.X -m venv venv_ip

# to enter the virtual environment
source venv_ip/bin/activate

# once active you may begin to install dependencies!

# to exit the environment
deactivate
```
2) Use pipenv
```bash
# Need @Jeff to fill this in as I'm still relatively confused by pipenv
```

## 3) Install dependencies

*With your virtual environment active*

Now we'll begin installing the python dependencies for the projects

```bash
cd imagepypelines
pip install -r requirements.txt

cd ../imagepypelines-tools
pip install -r requirements.txt

# navigate back to directory with imagepypelines and imagepypelines-tools in it
cd ..
```

After running these commands, you will have a virtual environment with all things needed to run the projects.

## 4) Install projects

*With your virtual environment active*

```bash
cd imagepypelines
pip install -e setup.py

cd ../imagepypelines-tools
pip install -e setup.py
```

## 5) Verify installation

*With your virtual environment active*

The easiest way to verify installation is to run the dashboard and ping it with a fake pipeline. This will ensure both projects have been installed properly.

In one terminal, run
```bash
cd imagepypelines-tools/imagepypelines-tools

# run the dashboard (localhost:5000 by default)
python app.py
```

Once the dashboard is running on localhost at port 5000, you can view it in your browser. Next we'll ping the dashboard with our test pipeline.

In another terminal, run
```bash
# execute the imagepypelines-tools ping command (current default is 9000 to communicate with dashboard's chatroom)
imagepypelines ping localhost 9000 -i 10000
```

The dashboard should be seeing activity being sent to it by the test pipeline!
