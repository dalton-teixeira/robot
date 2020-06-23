import json
import requests
import sys
import yaml
import xml.etree.ElementTree as ET
import os
from xml.sax.saxutils import unescape

print("Run this script using your personal TM4J access API Key. Follow the link to get yours: https://support.smartbear.com/tm4j-cloud/docs/api-and-test-automation/generating-access-keys.html")

test_case_status = {}
tm4j_folders = []
tm4j_tcs = []
robot_suites = []
settings = {}
with open(r'settings.yml') as settings_file:
    settings = yaml.load(settings_file, Loader=yaml.FullLoader)

tree = ET.parse(os.path.join(settings["robot report folder"], "output.xml"))
xml_output_root = tree.getroot()

addon = {"base_url": 'https://avst.connect.adaptavist.com/atm-addon/rest/tests/2.0', "search_api": 'testcase/search',
         "Autorization": 'JWT {}'.format(settings["access key"])}

api = {"base_url": 'https://api.adaptavist.io/tm4j/v2'}
headers = {'content-type': 'application/json',
           'Accept': 'application/json, text/plain, */*',
           'Authorization': 'Bearer {}'.format(settings["access key"])}


def quit_error(message):
    print("Oops! There was an error: {0}".format(message))
    sys.exit(0)


def check_response(response):
    if int(response.get('statusCode', 0)) == 401:
        quit_error("Unauthorized. {0}".format(response['message']))
    if int(response.get('errorCode', 0)) == 500 or int(response.get('errorCode', 0) == 400):
        quit_error("{0}. Response {1}".format(response['message'], response))
    return response


def get_folder_name(id):
    if id is None:
        return None
    for tm4j_folder in tm4j_folders:
        if tm4j_folder["id"] == id:
            return tm4j_folder["name"]
    return None


def get_tm4j_folders(cache=True):
    if cache and len(tm4j_folders) > 0:
        return tm4j_folders

    params = 'projectKey={projectKey}&maxResults={maxResults}&folderType={folderType}'.format(
        projectKey=settings["project key"],
        maxResults=500,
        folderType="TEST_CASE")
    full_url = "{base_url}/folders".format(base_url=api["base_url"])
    response = requests.get(url=full_url, params=params, headers=headers)
    response = json.loads(response.content)
    response = check_response(response)
    for folder in response["values"]:
        tm4j_folders.append(folder)
    return tm4j_folders


def get_tm4j_test_cases():

    params = 'projectKey={projectKey}&maxResults={maxResults}&archived=false'.format(
                                                                      projectKey=settings["project key"],
                                                                      maxResults=10000)

    full_url = "{base_url}/testcases".format(base_url=api["base_url"])
    r = requests.get(url=full_url, params=params, headers=headers)
    response = json.loads(r.content)
    response = check_response(response)
    for _tc in response["values"]:
        # get_tc_status(_tc["status"]["self"])
        _tc["name"] = unescape(_tc["name"], {"&apos;": "'", "&quot;": '"'})
        tm4j_tcs.append(_tc)

    return tm4j_tcs


def get_tc_status(link):
    if test_case_status.get(link, False):
        return test_case_status[link]
    response = requests.get(url=link, headers=headers)
    response = json.loads(response.content)
    test_case_status[link] = response["name"]
    return test_case_status[link]


def get_tcs_from_results_file():
    result = []
    with open(r'../../robot-reports/TEST-outputxunit.xml') as report_file:
        report = report_file.readlines()
        for line in report:
            if line.startswith("<testcase "):
                tc_name = line.split(' name="')[1].split(' time="')[0].rstrip('"').replace("&quot;", '"')
                result.append(tc_name)
    return result


def create_folder(path):
    parent = None
    folder = get_tm4j_folder_by_path(path)
    if folder is None:

        if len(path) > 1:
            parent = get_tm4j_folder_by_path(path[:-1])["id"]
        if len(path) >= 1:
            name = path.copy().pop()
        else:
            name = "ROBOT"

        full_url = "{base_url}/folders".format(base_url=api["base_url"])
        response = requests.post(url=full_url, headers=headers,
                                 json={"name": name,
                                       "folderType": "TEST_CASE",
                                       "projectKey": settings["project key"],
                                       "parentId": parent})
        response = json.loads(response.content)
        response = check_response(response)
        tm4j_folders = get_tm4j_folders(cache=False)
        folder = get_tm4j_folder_by_path(path)
    return folder


def create_test(name, parent=None, tags=[]):
    new_tc = {"name": name,
              "projectKey": settings["project key"],
              "componentId": settings["java component id"],
              "statusName": settings["test status name"],
              "folderId": parent,
              "labels": tags,
              "priorityName": "high"
              }

    full_url = "{base_url}/testcases".format(base_url=api["base_url"])

    response = requests.post(url=full_url, headers=headers,
                             json=new_tc)
    response = json.loads(response.content)
    response = check_response(response)

    return response


def get_suites_from_output():
    result = list(xml_output_root.iter(tag="suite"))
    if len(robot_suites) > 0:
        return robot_suites

    for item in result:
        id = item.attrib.get("id", None)
        if id is not None:
            parent = "-".join(id.split("-")[:-1])
            if len(parent) == 0:
                parent = None
            robot_suites.append({"id": id, "parent": parent, "name": item.attrib["name"]})

    return robot_suites


def get_tcs_from_output():

    result = list(xml_output_root.iter(tag="test"))
    tests = []
    for item in result:
        id = item.attrib.get("id", None)
        if id is not None:
            parent = "-".join(id.split("-")[:-1])
            if len(parent) == 0:
                parent = None
            tests.append({"id": id, "parent": parent, "name": unescape(item.attrib["name"])})
    return tests


def get_robot_suite_by_id(id):
    suite_list = get_suites_from_output()
    for suite in suite_list:
        if suite["id"] == id:
            return suite


def check_if_tc_is_in_tm4j(name):
    for tm4j_tc in tm4j_tcs:
        if name.replace("Scenario: ", "") == tm4j_tc["name"].replace("Scenario: ", ""):
            return True
        if name == tm4j_tc["name"]:
            return True

    return False


def create_folder_structure_in_tm4j(robot_folder_id):
    folder_path = get_folder_path_by_robot_suite_id(robot_folder_id)
    folder_path.insert(0, "ROBOT")
    count = 1
    folder = None
    for _i in folder_path:
        folder = create_folder(folder_path[:count])
        count = count + 1
    return folder


def check_folder_exists_in_tm4j(folder_name, parent):
    tm4j_folders = get_tm4j_folders()
    for tm4j_folder in tm4j_folders:
        if folder_name == tm4j_folder["name"]:
            if parent == get_folder_name(tm4j_folder["parentId"]):
                return tm4j_folder
    return None


def get_tm4j_folder_by_path(_folder_path):
    folders_found = []
    parent = None

    for folder_name in _folder_path:
        result = check_folder_exists_in_tm4j(folder_name, parent)
        if result is not None:
            folders_found.append(result)
        parent = folder_name
    if len(folders_found) != len(_folder_path):
        return None
    return folders_found.pop()


def update_tm4j():
    for robot_tc in robot_tcs:
        tc_is_not_created = not check_if_tc_is_in_tm4j(robot_tc["name"])
        if tc_is_not_created:
            folder = create_folder_structure_in_tm4j(robot_tc["parent"])
            create_test(robot_tc["name"], folder["id"])


def get_folder_path_by_robot_suite_id(suite_id):
    path = []
    _ids = suite_id.split("-")
    _id = _ids.pop(0)
    path.append(get_robot_suite_by_id(_id)["name"])
    for _split_id in _ids:
        _id = "{0}-{1}".format(_id, _split_id)
        path.append(get_robot_suite_by_id(_id)["name"])
    return path


test_cases = get_tm4j_test_cases()
robot_suites = get_suites_from_output()
robot_tcs = get_tcs_from_output()

update_tm4j()

# test = get_suites_from_output()
# print(test)
# test = get_folder_path_by_robot_suite_id("s1-s25-s2")
# print(test)
# tm4j_folders = get_tm4j_folders()
# test = get_tm4j_folder_by_path(test)
# print(test)
#


def create_test_cycle():
    cycle = {
        "version": 1,
            "executions":[
            {
                "source":"CalculatorSumTest.mappedToTestCaseNameAndPass",
                "result":"Passed",
                "testCase": {
                    "name": "Mapped to Test Case Name and Pass"
                }
            }
        ]
    }

# robot = get_or_create_test()
# print(robot)
# def get_tags_by_tc(name):
#     result = []
#
#     return result
#
# get_tags_by_tc(name)
#
#
# folder_id = create_folder(folder_name='robots')
# print(folder_id["id"])

# curl 'https://avst.connect.adaptavist.com/atm-addon/rest/tests/2.0/testcase' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://avst.connect.adaptavist.com/' -H 'X-Requested-With: XMLHttpRequest' -H 'Content-Type: application/json;charset=utf-8' -H 'Authorization: JWT eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqaXJhOjZlZWE2NTY5LWI5ZmItNGIyZS1hOGRlLTZlNmQxN2I0ZmZlZSIsInJvbGUiOiJCUk9XU0VSIiwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJjb250ZXh0Ijp7InVzZXIiOnsiYWNjb3VudElkIjoiNWRmY2RmOTU5YTE0MjUwY2I2OWYzNTJkIn19LCJleHAiOjE1ODkyNjg5MDAsImlhdCI6MTU4OTIyNTcwMH0.C85LK4-yvT5gbTcXbCrpxZvmuk0vL-KyBZYePDt6ROs' -H 'jira-project-id: 16104' -H 'Origin: https://avst.connect.adaptavist.com' -H 'Connection: keep-alive' -H 'Cookie: _ga=GA1.2.1138281209.1589221984; _gid=GA1.2.623498350.1589221984' --data-raw '{"projectId":16104,"name":"[ROBOT] test","owner":"5dfcdf959a14250cb69f352d","folderId":718175,"statusId":597040,"priorityId":597043,"customFieldValues":[{"customFieldId":9654,"intValue":22419},{"customFieldId":9655,"intValue":22423},{"customFieldId":9657,"intValue":22445},{"customFieldId":9658,"intValue":22451},{"customFieldId":9661,"intValue":35},{"customFieldId":9663,"booleanValue":true}],"testScript":{"stepByStepScript":{"steps":[{"index":0,"description":"","expectedResult":"","customFieldValueIndex":{},"customFieldValues":[]}]}}}'
#
# curl 'https://avst.connect.adaptavist.com/atm-addon/rest/tests/2.0/testcase/5345789' -X PUT -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://avst.connect.adaptavist.com/' -H 'X-Requested-With: XMLHttpRequest' -H 'Content-Type: application/json;charset=utf-8' -H 'Authorization: JWT eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqaXJhOjZlZWE2NTY5LWI5ZmItNGIyZS1hOGRlLTZlNmQxN2I0ZmZlZSIsInJvbGUiOiJCUk9XU0VSIiwiaXNzIjoiY29tLmthbm9haC50ZXN0LW1hbmFnZXIiLCJjb250ZXh0Ijp7InVzZXIiOnsiYWNjb3VudElkIjoiNWRmY2RmOTU5YTE0MjUwY2I2OWYzNTJkIn19LCJleHAiOjE1ODkyNjg5MDAsImlhdCI6MTU4OTIyNTcwMH0.C85LK4-yvT5gbTcXbCrpxZvmuk0vL-KyBZYePDt6ROs' -H 'jira-project-id: 16104' -H 'Origin: https://avst.connect.adaptavist.com' -H 'Connection: keep-alive' -H 'Cookie: _ga=GA1.2.1138281209.1589221984; _gid=GA1.2.623498350.1589221984' --data-raw '{"id":5345789,"projectId":16104,"testScript":{"plainTextScript":{"text":""}},"parameters":[]}'
#
