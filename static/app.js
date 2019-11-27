var app = new Vue({
    el: '#output',
    data: {
            // seen: false,
            avatar_url: null,
            username: null,
            email: null,
            public_repos: null,
            repo_stats: {},
    },
    methods: {
        executeRequest: function(name) {
            axios.get('/api/getuser', {
                params: {
                    username: name
                }
            })
            .then(response => {
                // this.seen = true
                this.avatar_url = response.data.avatar_url
                this.username ='@' + response.data.username
                this.email = response.data.email
                this.public_repos = 'Repositories: ' + response.data.public_repos
                this.repo_stats = response.data.repo_stats
            })
            .catch(error => {
                alert(error)
            })
            .finally(() => this.loading = false)
        }
    },
    mounted() {
        
    }
})

var form = new Vue({
    el: '#searchForm',
    data: {
        username: '',
    },
    methods: {
        processForm: function() {
            app.executeRequest(this.username)
        }
    }
})