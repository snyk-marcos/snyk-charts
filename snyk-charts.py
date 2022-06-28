import os
import requests
import time
import json
from getpass import getpass
import plotly.graph_objects as go


if not os.path.exists("images"):
    os.mkdir("images")

def main():
    orgId = input("Please input your organization's ID:")
    apiToken = getpass(prompt='Please input your token:')

    endpoint = "https://snyk.io/api/v1/reporting/counts/issues?from=2022-05-01&to=2022-06-27&groupBy=severity"

    # endpoint = "https://snyk.io/api/v1/reporting/counts/issues?from=" + 2017-07-01 + "&to=" + 2017-07-03 + "&groupBy=severity"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token ' + apiToken
    }

    values = json.dumps({
        "filters": {
            "orgs": [orgId],
            "severity": [
            "critical",
            "high",
            "medium",
            "low"
            ],
            "types": [
            "vuln",
            "license",
            "configuration"
            ],
            "languages": [
            "node",
            "javascript",
            "ruby",
            "java",
            "scala",
            "python",
            "golang",
            "php",
            "dotnet",
            "swift-objective-c",
            "elixir",
            "docker",
            "linux",
            "dockerfile",
            "terraform",
            "kubernetes",
            "helm",
            "cloudformation"
            ],
            "projects": [],
            "ignored": False,
            "patched": False,
            "fixable": False,
            "isUpgradable": False,
            "isPatchable": False,
            "isPinnable": False,
            "priorityScore": {
            "min": 0,
            "max": 1000
            }
        }
    }, indent=4)


    request = requests.request("POST", endpoint, headers=headers, data=values)
    response = request.json()

    time_period = []

    low_count = []
    medium_count = [] 
    high_count = []
    critical_count = []

    while response['results']:
        result = response['results'].pop()
        date = result['day']
        time_period.append(date)
        severity = result['severity']
        critical_count.append(severity['critical'])
        high_count.append(severity['high'])
        medium_count.append(severity['medium'])
        low_count.append(severity['low'])

    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=time_period, y=low_count, name='Low',
                             line=dict(color='gray', width=4)))
    fig.add_trace(go.Scatter(x=time_period, y=medium_count, name = 'Medium',
                             line=dict(color='burlywood', width=4)))
    fig.add_trace(go.Scatter(x=time_period, y=high_count, name = 'High',
                             line=dict(color='coral', width=4)))
    fig.add_trace(go.Scatter(x=time_period, y=critical_count, name = 'Critical',
                             line=dict(color='crimson', width=4)))

    # Edit the layout
    fig.update_layout(title='Issues over time',
                       xaxis_title='Month',
                       yaxis_title='Issues')

    ts = str(time.time())
    ts = ts.replace(".","")

    fig.write_image("images/" + ts + "chart.png")
    fig.show()

if __name__ == "__main__":
  main()