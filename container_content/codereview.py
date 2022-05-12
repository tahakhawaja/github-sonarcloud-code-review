# importing necessary libraries
import github3
from github3 import login
from http.server import executable
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from sonarqube import SonarCloudClient
from sonarqube import SonarQubeClient
from config import GITHUB_API_KEY, SONARCLOUD_API_KEY, GITHUB_USERNAME, GITHUB_PASSWORD
sonar = SonarCloudClient(sonarcloud_url="https://sonarcloud.io", token=SONARCLOUD_API_KEY)

# Login using a personal access token
github = github3.login(token=GITHUB_API_KEY)

# forking all public repositories for given user
def ForkRepos(username):
    for repository in github.repositories_by(username):
        repository.create_fork()
    time.sleep(5)


# Conducting code review in SonarCloud on all repositories 
def SonarAnalysis():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('https://sonarcloud.io/')
    githubclick = driver.find_element_by_xpath('//*[@id="gatsby-focus-wrapper"]/div/div/div[2]/div[1]/div/div/div/a[1]')
    githubclick.click()
    githubusername = driver.find_element_by_xpath('//*[@id="login_field"]')
    githubusername.send_keys(GITHUB_USERNAME)
    githubpassword = driver.find_element_by_xpath('//*[@id="password"]')
    githubpassword.send_keys(GITHUB_PASSWORD)
    githubsigninclick = driver.find_element_by_xpath('//*[@id="login"]/div[3]/form/div/input[12]')
    githubsigninclick.click()
    time.sleep(5)
    plussign = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div/nav/div/div/ul[1]/li[3]/button')
    plussign.click()
    analyzeprojects = driver.find_element_by_xpath('//*[@id="global-navigation"]/div/div/ul[1]/li[3]/div/ul/li[1]/a')
    analyzeprojects.click()
    time.sleep(5)
    selectallrepos = driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div[1]/div/div[1]/a/i')
    selectallrepos.click()
    time.sleep(5)
    reposetup = driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div[2]/div/form/div[2]/div[2]/button')
    reposetup.click()
    time.sleep(300)

def GetCodeReview():
    analyzed_repos = list(sonar.favorites.search_favorites())
    analyzed_repo_list = []
    for i in range(len(analyzed_repos)):
        repos = analyzed_repos[i]
        analyzed_repo_list.append(repos["key"])

    repo_review = {}
    for repo_name in analyzed_repo_list:
        analysis = list(sonar.issues.search_issues(componentKeys=repo_name))
        a = {}
        for i in range(len(analysis)):
            item = analysis[i]
            if item["author"] in a:
                a[item["author"]][item["type"]] = a[item["author"]][item["type"]] + 1                
            else:
                a[item["author"]] = {"BUG":0, "CODE_SMELL":0, "VULNERABILITY":0}
                a[item["author"]][item["type"]] = 1      
        repo_review[repo_name] = a
    return repo_review


def getreview(username):
    ForkRepos(username)
    SonarAnalysis()
    analyzed_repos = list(sonar.favorites.search_favorites())
    analyzed_repo_list = []
    for i in range(len(analyzed_repos)):
        repos = analyzed_repos[i]
        analyzed_repo_list.append(repos["key"])

    repo_review = {}
    for repo_name in analyzed_repo_list:
        analysis = list(sonar.issues.search_issues(componentKeys=repo_name))
        a = {}
        for i in range(len(analysis)):
            item = analysis[i]
            if item["author"] in a:
                a[item["author"]][item["type"]] = a[item["author"]][item["type"]] + 1                
            else:
                a[item["author"]] = {"BUG":0, "CODE_SMELL":0, "VULNERABILITY":0}
                a[item["author"]][item["type"]] = 1      
        repo_review[repo_name] = a
    return repo_review