import requests
from slackbot.settings import JENKINS_URL, JENKINS_USER, JENKINS_TOKEN, JENKINS_JOBS_TOKENS


class Jenkins:
    JENKINS_COMMANDS = [
        "run_job"
    ]

    def run_job(self, params):

        return "Job started"

    def _get(self, url):
        r = requests.get(url, auth=(JENKINS_USER, JENKINS_TOKEN))
        return r

    def _post(self, url):
        r = requests.post(url, auth=(JENKINS_USER, JENKINS_TOKEN))
        return r

    def run(self, params):
        job_name = params.split(maxsplit=1)[0]
        url = "{}/job/{}/build?token=aaaaa".format(JENKINS_URL, job_name)
        r = requests.get(url, auth=(JENKINS_USER, JENKINS_TOKEN))
        if r.ok:
            return "Job: {} started.".format(job_name)
        else:
            return "Job: {} start failed.".format(job_name)

    def job(self, params):
        if not params:
            return "This command require parameters."
        if len(params.split(maxsplit=1)) < 2:
            jobs_command = params
            if jobs_command == 'all':
                url = "{}/api/python".format(JENKINS_URL)
                r = self._get(url)
                job_list = []
                for job in eval(r.content)['jobs']:
                    job_list.append(job['name'])
                return "Full job list:\n {}".format("\n ".join(job_list))
            else:
                return "Jenkins job command unknown."
        else:
            job_name, job_command = params.split(maxsplit=1)
            if job_command == 'run':
                url = "{}/job/{}/build?token={}".format(JENKINS_URL, job_name, JENKINS_JOBS_TOKENS[job_name])
                r = self._get(url)
                if r.ok:
                    job_url = r.headers._store['location'][1]
                    return "Job: {} started. Link: {}".format(job_name, job_url)
                else:
                    return "Job: {} start failed. Reason: {}".format(job_name, r.reason)

            elif job_command == 'status':
                url = "{}/job/{}/api/python".format(JENKINS_URL, job_name)
                r = self._get(url)
                if not r.ok:
                    return "This job not defined or jenkins failed."
                content = eval(r.content)
                healthReport = "healthReport: {}".format(
                    content['healthReport'][0]['description'] if content['healthReport'] else "description not defined")
                lastCompletedBuild = "lastCompletedBuild number: {}".format(
                    content['lastCompletedBuild']['number'] if content['lastCompletedBuild'] else "number not defined")
                lastBuild = "lastBuild number: {}".format(
                    content['lastBuild']['number'] if content['lastBuild'] else "number not defined")
                lastStableBuild = "lastStableBuild number: {}".format(
                    content['lastStableBuild']['number'] if content['lastStableBuild'] else "number not defined")
                lastFailedBuild = "lastFailedBuild number: {}".format(
                    content['lastFailedBuild']['number'] if content['lastFailedBuild'] else "number not defined")
                lastUnstableBuild = "lastUnstableBuild number: {}".format(
                    content['lastUnstableBuild']['number'] if content['lastUnstableBuild'] else "number not defined")
                return "\n"+"\n".join([healthReport, lastCompletedBuild, lastBuild,
                                 lastStableBuild, lastFailedBuild, lastUnstableBuild])
            elif job_command == "status=last":
                url = "{}/job/{}/lastBuild/api/python".format(JENKINS_URL, job_name)
                r = self._get(url)
                if not r.ok:
                    return "This job not defined or jenkins failed."
                content = eval(r.content)
                fullDisplayName = "Job name: {}".format(content['fullDisplayName'])
                if content['building']:
                    status = "Job status: BUILDING".format(content['result'])
                else:
                    status = "Job status: {}".format(content['result'])
                duration = "Job duration: {}ms".format(content['duration'])
                return "\n" + "\n".join([fullDisplayName, status, duration])

            elif job_command.startswith("status="):
                job_number = job_command.split("=")[1]
                url = "{}/job/{}/{}/api/python".format(JENKINS_URL, job_name, job_number)
                r = self._get(url)
                if not r.ok:
                    return "This job not defined or jenkins failed."
                content = eval(r.content)
                fullDisplayName = "Job name: {}".format(content['fullDisplayName'])
                result = "Job result: {}".format(content['result'])
                duration = "Job duration: {}ms".format(content['duration'])
                return "\n" + "\n".join([fullDisplayName, result, duration])

            else:
                return "Jenkins job command unknown."


