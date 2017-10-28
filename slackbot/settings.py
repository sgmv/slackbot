### SLACK parameters
SLACK_API_TOKEN = 'xoxb-251530744194-pxeryltwEYhRjbcy2CgTPJH4'
SLACK_API_URL = 'https://slack.com/api/'
SLACK_PROVIDERS = ['jenkins', 'saltstack']

### LOG configuration
LOG_FILE = '/tmp/slackbot.log'
LOG_LEVEL = 'DEBUG'
LOG_REQUESTS = False


### Jenkins
JENKINS_URL = 'http://192.168.122.244:8080'
JENKINS_USER = 'admin'
JENKINS_TOKEN = '9938c09e0eb92da13117415e31340801'
JENKINS_JOBS_TOKENS = {
    "test": "aaaaa",
    "test_failed": "aaaaa",
    "bla": "aaaaa"
}


### SaltStack
SALTSTACK_URL = 'http://192.168.122.244:8000/'
SALTSTACK_USER = 'tester'
SALTSTACK_PASSWORD = 'tester'