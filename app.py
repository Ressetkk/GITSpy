from flask import Flask, request, escape, abort, jsonify
import requests

app = Flask(__name__)

GITHUB_API_URL = 'https://api.github.com'
USERS_ENDPOINT = '/users'
REPOS_ENDPOINT = '/repos'

@app.route("/api/getuser/")
def getUserInfo():
    """
    This method will fetch user information from GitHub API and return desired information
    as JSON.
    """
    username = request.args.get("username", None)
    if username:
        endpoint = "{}/{}".format(GITHUB_API_URL + USERS_ENDPOINT, username)
        response = _executeRequest(endpoint).json()
        reposResponse = _getReposInfo(_executeRequest(response['repos_url']).json())
        userInfo = {
            'email': response['email'],
            'username': response['login'],
            'avatar_url': response['avatar_url'],
            'repos': reposResponse,
            'repo_stats': _generateLanguageStats(reposResponse),
            'public_repos': response['public_repos']
        }
        return(userInfo)
    else:
        abort(400, "You must provide username.")\

@app.route("/api/login")
def login():
    pass

@app.route("/api/getuser/activity")
def getUserActivity():
    username = request.args.get("username", None)
    endpoint = "{}/{}".format(GITHUB_API_URL + USERS_ENDPOINT, username)
    response = _executeRequest(endpoint + "/events/public").json()
    return(jsonify(list(event for event in response if event['type'] == 'PushEvent')))

@app.route("/api/debug")
def getHostInfo():
    from socket import gethostname
    info = {
        'hostname': gethostname()
    }
    return(info)

def _executeRequest(url):
    response = requests.get(url=url)
    _checkResponseStatus(response)
    return(response)

def _getReposInfo(response):
    response = response
    reposInfo = list(map(_buildReposJson, response))
    return(reposInfo)

def _checkResponseStatus(response):
    """
    Helper function to check response status from GitHub API
    """
    try:
        response.raise_for_status()
    except(requests.exceptions.HTTPError):
        abort(response.status_code, response.reason)

def _buildReposJson(jsonObj):
    """
    Helper function to build JSONObject with Repository information
    """
    return({
        'html_url': jsonObj['html_url'],
        'language': jsonObj['language'],
        'name': jsonObj['name'],
        'description': jsonObj['description']
    })

def _generateLanguageStats(repos):
    """
    For each repository check how many language occurencies there is and write statistics.
    IN: Repository JSONList
    OUT: JSONObject with occurencies
    """
    languageStats = {}
    for repo in repos:
        lang = repo['language']
        if lang == None:
            lang = "Not specified"
        if lang in languageStats:
            languageStats[lang] += 1
        else:
            languageStats[lang] = 1
    return(languageStats)

if __name__ == "__main__":
    app.run()