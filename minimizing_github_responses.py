"""Example of minimizing the size of a GitHub API response.
"""
import json
from dougerino import github_rest_api

def minimizing_demo():
    """Typical size reduction is 80-90%, so worth doing for most scenarios.
    """
    github_response = github_rest_api(endpoint='/repos/microsoft/typescript')
    jsondata = json.loads(github_response.text)
    print('>>> GitHub API response = {0} bytes'.format(len(str(jsondata))))
    print(jsondata)

    # remove fields named *_url, these aren't needed for analysis/reporting
    no_urls = {key:value for (key, value) in jsondata.items()
               if not key.endswith('url')}
    print('>>> URLs removed = {0} bytes'.format(len(str(no_urls))))
    print(no_urls)

    # replace embedded entites with just their name instead of a dictionary
    logins_only = dict()
    for (key, value) in no_urls.items():
        if isinstance(value, dict) and 'login' in value:
            logins_only[key] = value['login']
        else:
            logins_only[key] = value
    print('>>> embedded entites replaced with name only = {0} bytes'.
          format(len(str(logins_only))))
    print(logins_only)

if __name__ == '__main__':
    minimizing_demo()
