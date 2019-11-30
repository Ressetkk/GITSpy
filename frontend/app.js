// const githubColors = (() => {
//     var data = {};
    
//     return(data);
// })();
var githubColors = {};
axios.get('https://raw.githubusercontent.com/ozh/github-colors/master/colors.json')
.then(response => {
    githubColors = response.data;
})
.catch(error => {
    console.error(error);
})

var app = new Vue({
    el: '#user',
    data: {
        seen: false,
        avatar_url: null,
        username: null,
        email: null,
        public_repos: null,
    },
    methods: {
        executeRequest: function(username, token) {
            axios.get('/api/getuser', {
                params: {
                    username: username
                },
                headers: {
                    token: token
                }
            })
            .then(response => {
                this.seen = true,
                this.avatar_url = response.data.avatar_url
                this.username ='@' + response.data.username
                this.email = response.data.email
                this.public_repos = 'Repositories: ' + response.data.public_repos
            })
            .catch(error => {
                alert(error)
            })
            .finally(() => this.loading = false)
        }
    }
});

var stats = new Vue({
    el: "#repoStats",
    data: {
        seen: false,
        repos_list: [],
        repos: null,
        repos_stats: {},
    },
    methods: {
        executeRequest: function(username, token) {
            axios.get('/api/getuser/repos', {
                params: {
                    username: username
                },
                headers: {
                    token: token
                }
            })
            .then(response => {
                this.seen = true
                this.repos_list = response.data.repos_list
                this.repos = response.data.repos
                this.repos_stats =  styleStats(response.data.repos_stats, response.data.repos)
            })
            .catch(error => {
                alert(error)
            })
            .finally(() => this.loading = false)
        }
    }
});

function styleStats(stats, allElements) {
    return (stats.map((elem) => {
           return({
                language: elem.language,
                count: elem.count,
                style: {
                    width: (elem.count / allElements) * 100 + "%",
                    'background-color': (function() {
                        try {
                            return (githubColors[elem.language].color)
                        }
                        catch (e) {
                            return '#333'
                        }
                    })()
                }
            });
        })
    );
}

var activity = new Vue({
    el: '#activity',
    data: {
        seen: false,
        items: {
            created_at: '',
            repo: {},
            commits: {}
        }
    },
    methods: {
        executeRequest: function(username, token) {
            axios.get('/api/getuser/activity', {
                params: {
                    username: username
                },
                headers: {
                    token: token
                }
            })
            .then(response => {
                this.seen = true
                this.items = response.data.items
            })
            .catch(error => {
                alert(error)
            })
            .finally(() => this.loading = false)
        }
    }
});
var form = new Vue({
    el: '#searchForm',
    data: {
        username: '',
        token: ''
    },
    methods: {
        processForm: function() {
            app.executeRequest(this.username, this.token)
            stats.executeRequest(this.username,this.token)
            activity.executeRequest(this.username, this.token)
        }
    }
});
