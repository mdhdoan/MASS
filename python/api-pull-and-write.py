import json
from os import link
import urllib.request
import urllib.error

def api_to_json(url):
    response_body = urllib.request.urlopen(url).read()
    return json.loads(response_body)

def api_write_to_json(type, general_json, file_name):
    print('Processing: ', type)
    full_data = {}
    for jdata in general_json:
        print('.', flush = True)
        try:
            url = 'https://www.monitoringresources.org/api/v1/' + type + '/' + str(jdata['id'])
            details = api_to_json(url)
            full_data[jdata['id']] = details
        except urllib.error.HTTPError:
            print('Error HTTPError')
    json_data = json.dumps(full_data, indent=2)
    with open(file_name, 'w') as json_file:
        json_file.write(json_data)

# list_of_links = [designs_link, methods_link, projects_link, programs_link, protocols_link, repositories_link, study_designs_link]
# jdata_list = [designs_jdata, methods_jdata, projects_jdata, programs_jdata, protocols_jdata, repositories_jdata, study_designs_jdata]

if __name__ == "__main__":
    # designs_link = 'https://www.monitoringresources.org/api/v1/designs'
    # designs_jdata = api_to_json(designs_link)
    # designs_full_jdata = api_write_to_json('designs', designs_jdata, 'sample_designs_jdata.json')

    # methods_link ='https://www.monitoringresources.org/api/v1/methods'
    # methods_jdata = api_to_json(methods_link)
    # methods_full_jdata = api_write_to_json('methods', methods_jdata, 'methods_jdata.json')

    # projects_link = 'https://www.monitoringresources.org/api/v1/projects'
    # projects_jdata = api_to_json(projects_link)
    # projects_full_jdata = api_write_to_json('projects', projects_jdata, 'projects_jdata.json')

    programs_link = 'https://www.monitoringresources.org/api/v1/programs'
    programs_jdata = api_to_json(programs_link)
    programs_full_jdata = api_write_to_json('programs', programs_jdata, 'programs_jdata.json')

    protocols_link = 'https://www.monitoringresources.org/api/v1/protocols'
    protocols_jdata = api_to_json(protocols_link)
    protocols_full_jdata = api_write_to_json('protocols', protocols_jdata, 'protocols_jdata.json')

    repositories_link = 'https://www.monitoringresources.org/api/v1/repositories'
    repositories_jdata = api_to_json(repositories_link)
    repositories_full_jdata = api_write_to_json('repositories', repositories_jdata, 'repositories_jdata.json')

    study_designs_link = 'https://www.monitoringresources.org/api/v1/studydesigns'
    study_designs_jdata = api_to_json(study_designs_link)
    study_designs_full_jdata = api_write_to_json('studydesigns', repositories_jdata, 'studydesigns_jdata.json')