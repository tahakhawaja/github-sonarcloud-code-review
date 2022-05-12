# GitHub Code Review (Python)

This docker application uses SonarCloud and GitHub to conduct code reviews on all public repositories for a given GitHub user. The application takes a GitHub user name, forks all public repositories of that user and conducts an analysis in SonarCloud to retrieve the number of bugs, code smells, and vulnerabilities. 

1. The first service 


## Installation

Before cloning the project if an App password has not already be created, go to Personal Settings and select App passwords under Access Management. Select Create app password, create a name for the Label, select all Permissions and click Create. Use this newly created App password along with the Bitbucket email account to verify your login details when cloning projects. 

- clone this repo

- install docker according to OS instructions

		windows pro/enterprise: https://docs.docker.com/docker-for-windows/install/
		windows home:
			install docker toolbox: 
			https://docs.docker.com/toolbox/overview/
			enable hyper-v/virtualization on your machine:
			first make sure it is enabled on your machine through BIOS settings: https://2nwiki.2n.cz/pages/viewpage.action?pageId=75202968
			then if it is enabled through bios, enable it through settings on your machine.
			https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v
		mac: https://docs.docker.com/docker-for-mac/install/
		ubuntu: https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1

- cd into container_content, this folder contains required files and config to build up a docker image

- copy `config.py.example` to `config.py` and **modify** the file to include your credentials. Refer to the steps below for accessing those credentials. 

- Go onto https://sonarcloud.io/ and login with your GitHub account. After logging in, click the "Account" icon on the top right, go to "My Account", select "Security" at the top, and generate a new token. You can give this token any name. Copy this token and input the token into `config.py` where it says "SONARCLOUD_API_KEY".
    Note it must be of the form `SONARCLOUD_API_KEY` = "<the key>"

- Go onto your GitHub account, click on the icon at the top right, go to "Settings", on the bottom left, select "Developer settings", then select "Personal access tokens" on the left and generate a new token. When generating the access token, give it any name, select all scopes, and set the expiration to "no expiration". Copy this personal access token go to `config.py` and **modify** to enter your "GITHUB_API_KEY".
    Note it must be of the form `GITHUB_API_KEY` = "<the key>"

- Go into `config.py` file and **modify** to enter your "GITHUB_USERNAME" and "GITHUB_PASSWORD" that was used to create the SonarCloud account and GitHub Personal access token.
    Note it must be of the form `GITHUB_USERNAME` = "<the key>"
    Note it must be of the form `GITHUB_PASSWORD` = "<the key>"


- build the image

		docker build -t python_code_review . 
	
- check that image successfull installed

		docker images
		
	it should list our <image_name> (python\_code\_review)
	
- run the image 

		docker run -i -t -d -p 8080:8080 --name python_code_review python_code_review 

the container should run the Python app at `http://localhost:8080` test with `curl -o - http://localhost:8080/ppcad`

- if curl fails then try http://localhost:8080/ppcad` from web browser

- to stop the container

		docker stop python_code_review
		

- to rebuild the container after making an internal change run from /container_content/

		docker stop python_code_review
		docker rmi python_code_review
		docker rm python_code_review
		docker rmi -f $(docker images -f "dangling=true" -q)
		docker build -t python_code_review . 
		docker run -i -t -d -p 8080:8080 --name python_code_review python_code_review

## API Paths

### ID only (global rank)

**GET /<string:username>**

e.g. `http://localhost:8080/ppcad`

##### Sample Response

```
{
    {'user@gmail.com': {'BUG': 25, 'CODE_SMELL': 91, 'VULNERABILITY': 0}}
}
```
