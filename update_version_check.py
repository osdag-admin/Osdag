######################### UpDateNotifi ################
import urllib.request
import requests
import re
from PyQt5.QtWidgets import QMessageBox,QMainWindow
import sys

# class Update():
#     def __init__(self):
#         super().__init__()
#         self.old_version=self.get_current_version()
#         # msg = self.notifi()
#
#     def notifi(self):
#         try:
#             url = "https://raw.githubusercontent.com/osdag-admin/Osdag/master/README.md"
#             file = urllib.request.urlopen(url)
#             version = 'not found'
#             for line in file:
#                 decoded_line = line.decode("utf-8")
#                 match = re.search(r'Download the latest release version (\S+)', decoded_line)
#                 if match:
#                     version = match.group(1)
#                     version = version.split("<")[0]
#                     break
#             # decoded_line = line.decode("utf-8")
#             # new_version = decoded_line.split("=")[1]
#             if version != self.old_version:
#                 msg = 'Current version: '+ self.old_version+'<br>'+'Latest version '+ str(version)+'<br>'+\
#                       'Update will be available <a href=\"https://osdag.fossee.in/resources/downloads\"> here <a/>'
#             else:
#                 msg = 'Already up to date'
#             return msg
#         except:
#             return "No internet connection"
#
#     def get_current_version(self):
#         version_file = "_version.py"
#         rel_path = str(sys.path[0])
#         rel_path = rel_path.replace("\\", "/")
#         VERSIONFILE = rel_path +'/'+ version_file
#
#         try:
#             verstrline = open(VERSIONFILE, "rt").read()
#         except EnvironmentError:
#             pass  # Okay, there is no version file.
#         else:
#             VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
#             mo = re.search(VSRE, verstrline, re.M)
#             if mo:
#                 verstr = mo.group(1)
#                 return verstr
#             else:
#                 print("unable to find version in %s" % (VERSIONFILE,))
#                 raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))
from tokenize import cookie_re
import requests
import json
import os
from pathlib import Path

######################### UpDateNotifi ################
import urllib.request
import requests
import re
from PyQt5.QtWidgets import QMessageBox, QMainWindow
import sys
import requests
import json
import os
from pathlib import Path
import json


class Update():
    def __init__(self):
        super().__init__()
        self.old_version, self.old_no_of_commits, self.old_commitid = self.get_current_version()  # this fxn gets version and no of commits
        # msg = self.notifi()
        self.latest_commit_sha_id = self.get_latest_commit_sha_id()
        self.url = 'https://api.github.com/repos/spartan289/Osdag/commits'

    def notifi(self):
        try:
            url = "https://raw.githubusercontent.com/addddd123/Osdag/master/version.json"
            file = urllib.request.urlopen(url)
            fileobj = json.loads(file)
            version = 'not found'
            version_and_commits_on_github = []  # will contain no of commits on git and version no on git
            version = fileobj['__version__']
            commits = fileobj["__noOfCommitsOnGithub__"]

            if version== self.old_version:
                print("executed main version found")
                msg = "New update is avialable at <a href=\"https://osdag.fossee.in/resources/downloads\"> here <a/>"
            elif int(commits) > int(self.old_no_of_commits):  # github commit is ahead of local osdag
                print("into mini update check")
                msg = 'Current commits: ' + self.old_no_of_commits + '<br>' + 'Latest commmits ' + \
                      version_and_commits_on_github[1] + '<br>' + \
                      'New mini update is avialable'
            else:
                msg = "no update found!! <br>Osdag already upto date"
            return msg
        except:
            return "No internet connection"

    def get_latest_commit_sha_id(self):
        commits = requests.get(self.url)
        commits_parse = json.loads(commits.text)
        latest_commit = commits_parse[0]["sha"]
        return latest_commit

    def get_current_version(self):
        try:
            version_obj = json.loads(open("version.json").read())
        except EnvironmentError:
            pass  # Okay, there is no version file.
        else:

            VSRE = version_obj['__version__']
            commits = version_obj['__noOfCommitsOnGithub__']
            sha_id = version_obj['_currentSHaid__']

            return VSRE, commits, sha_id


    def update_structure_from(self, current_commit_sha_id):
        commits = requests.get(self.url)
        commits_parse = json.loads(commits.text)
        all_shaid = []

        for commit in commits_parse:
            if commit["sha"] == current_commit_sha_id:
                break
            all_shaid.append(commit["sha"])
        all_shaid.reverse()
        for shaid in all_shaid:
            print("Sha id: " + shaid)
            self.update_structure(shaid)
            print("\n\n")


    def update_file_version(self):
        # version_file = "_version.py"
        # rel_path = str(sys.path[0])
        # rel_path = rel_path.replace("\\", "/")
        # VERSIONFILE = rel_path + '/' + version_file
        # try:
        #     verstrline = open(VERSIONFILE, "rt").read()
        #
        # except EnvironmentError:
        #     pass
        version_obj = json.load(open('version.json'))
        version_obj['_currentShaId__']=self.get_latest_commit_sha_id()
        json.dump(version_obj,open('version.json','w'))

    def update_structure(self, shaid):
        commit_url = "https://api.github.com/repos/spartan289/Osdag/commits" + shaid
        commit_request = requests.get(commit_url)
        if (commit_request.status_code == 200):
            commit_parse = json.loads(commit_request.text)

            total_changed_files = len(commit_parse["files"])
            print(total_changed_files)
            for file in commit_parse["files"]:
                if (file['status'] == 'added'):
                    # self.file_update_dict["added"].append(file["filename"])
                    print("File Added: " + file['filename'])
                    self.add_file(file['filename'], shaid)
                elif (file['status'] == 'modified'):
                    # self.file_update_dict["modified"].append(file["filename"])
                    print("File Modified: " + file['filename'])
                    self.update_file(file['filename'], shaid)

                elif (file['status'] == 'removed'):
                    # self.file_update_dict["removed"].append(file["filename"])
                    print("File Removed: " + file['filename'])
                    self.delete_file(file['filename'])
                else:
                    print("File Status: " + file['status'])
        pass


    def add_file(self, filename, sha_id):
        url = "https://raw.githubusercontent.com/spartan289/Practical/" + sha_id + "/" + filename
        file_request = requests.get(url)
        if (file_request.status_code == 200):
            file_content = file_request.text
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with filepath.open("w+", encoding="utf-8") as f:
                for line in file_content:
                    f.write(line)


    def delete_file(self, filename):
        filepath = Path(filename)
        if (filepath.exists()):
            filepath.unlink()
        else:
            print("File does not exist")

        pass


    def update_file(self, filename, sha_id):
        self.delete_file(filename)
        self.add_file(filename, sha_id)
# obj=Update() #obj here for testing
