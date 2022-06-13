
from tokenize import cookie_re
import requests
import json
import os
from pathlib import Path

######################### UpDateNotifi@Updater ################
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
        self.url = "https://api.github.com/repos/spartan289/Osdag/commits"

        self.old_version, self.old_no_of_commits, self.old_commitid = self.get_current_version()  # this fxn gets version and no of commits
        # msg = self.notifi()
        self.latest_commit_sha_id = self.get_latest_commit_sha_id()
        print(self.url)

    def notifi(self):
        try:
            url = "https://raw.githubusercontent.com/spartan289/Osdag/master/version.json"
            file = requests.get(url)
            fileobj = json.loads(file.text)
            version = 'not found'
            version_and_commits_on_github = []  # will contain no of commits on git and version no on git
            version = fileobj['__version__']
            commits = fileobj["__noOfCommitsOnGithub__"]
            shaId = self.latest_commit_sha_id
            print(shaId)
            print(self.old_commitid)
            if version != self.old_version:
                print("executed main version found")
                msg = "New update is avialable at <a href=\"https://osdag.fossee.in/resources/downloads\"> here <a/>"
            elif shaId != self.old_commitid:  # github commit is ahead of local osdag
                print("into mini update check")
                msg = 'New mini update is available'
            else:
                msg = "no update found!! <br>Osdag already upto date"
            return msg
        except Exception as e:
            print(e)
            return "No internet connection"

    def get_latest_commit_sha_id(self):
        print(self.url)
        commits = requests.get(self.url)
        commits_parse = json.loads(commits.text)
        latest_commit = commits_parse[0]["sha"]
        print('Latest Commit Sha id', latest_commit)
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

    def update_structure_from(self):
        current_commit_sha_id = self.old_commitid
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
        self.update_file_version()

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
        version_obj['_currentSHaid__'] = self.get_latest_commit_sha_id()
        json.dump(version_obj, open('version.json', 'w'))

    def update_structure(self, shaid):
        commit_url = "https://api.github.com/repos/spartan289/Osdag/commits/" + shaid
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
        url = "https://raw.githubusercontent.com/spartan289/Osdag/" + sha_id + "/" + filename
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
# obj.notifi()
