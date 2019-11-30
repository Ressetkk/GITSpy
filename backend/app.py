from flask import Flask, request, escape, abort, jsonify
import requests

app = Flask(__name__)

GITHUB_API_URL = 'https://api.github.com'
GITHUB_URL = 'https://github.com'

@app.route("/api/getuser/")
def getUser():
    """
    This method will fetch user information from GitHub API and return desired information
    as JSON.
    """
    username = request.args.get("username", None)
    if username:
        response = _executeRequest("{}/users/{}".format(GITHUB_API_URL, username), request).json()
        userInfo = {
            'email': response['email'],
            'username': response['login'],
            'avatar_url': response['avatar_url'],
            'public_repos': response['public_repos']
        }
        return(userInfo)
    else:
        abort(400, "You must provide a username.")\

@app.route("/api/getuser/repos/")
def getUserRepos():
    username = request.args.get("username", None)
    if username:
        response = _executeRequest("{}/users/{}/repos".format(GITHUB_API_URL, username), request).json()
        reposInfo = {
            'repos_list': list(map(lambda x: ({
                                    'html_url': x['html_url'],
                                    'language': x['language'],
                                    'name': x['name'],
                                    'description': x['description']
                                }), response)),
            'repos': len(response),
            'repos_stats': _generateLanguageStats(response)
        }
        return(reposInfo)
    else:
        abort(400, "You must provide a username.")

@app.route("/api/getuser/activity/")
def getUserActivity():
    username = request.args.get("username", None)
    response = _executeRequest("{}/users/{}/events/public?per_page=100".format(GITHUB_API_URL, username), request).json()
    pushEvents = list(event for event in response if event['type'] == 'PushEvent')
    return (
        {            
            'items': [
                {
                    'created_at': event['created_at'],
                    'repo': {
                        'name':  event['repo']['name'],
                        'url': GITHUB_URL + "/" + event['repo']['name']
                    },
                    'commits': [{
                        'message': commit['message'],
                        'sha': commit['sha'],
                        'url': GITHUB_URL + "/" + event['repo']['name'] + "/commits/" + commit['sha']
                    } for commit in event['payload']['commits']
                ]
            } for event in pushEvents]
        }
    )
@app.route("/")
def init():
    return({'success': True})
    
@app.route("/api/debug/")
def getHostInfo():
    from socket import gethostname
    from os import getenv 
    info = {
        'hostname': gethostname(),
        'app_version': getenv('VERSION')
    }
    return(info)

def _executeRequest(url, request):
    try:
        token = request.headers['token']
        if token == '':
            raise ValueError
        response = requests.get(url=url, headers={ 'Authorization': 'token ' + token})
    except (KeyError, ValueError):
        response = requests.get(url=url)
    _checkResponseStatus(response)
    return(response)

def _checkResponseStatus(response):
    """
    Helper function to check response status from GitHub API
    """
    try:
        response.raise_for_status()
    except(requests.exceptions.HTTPError):
        abort(response.status_code, response.reason)

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

    return([
        {
            'language': lang,
            'count': languageStats[lang]
         } for lang in languageStats])

if __name__ == "__main__":
    app.run()