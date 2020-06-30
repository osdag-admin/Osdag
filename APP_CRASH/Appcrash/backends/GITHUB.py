"""
This module contains the github backend.
"""
import logging
import webbrowser
#import requests
#import keyring
#import json
from .base import BaseBackend
from ..formatters.markdown import MardownFormatter
from PyQt5 import QtGui, QtCore, QtWidgets
from .._dialogs.gh_login import DlgGitHubLogin
import github

GH_MARK_NORMAL = ':/rc/GitHub-Mark.png'
GH_MARK_LIGHT = ':/rc/GitHub-Mark-Light.png'


def _logger():
    return logging.getLogger(__name__)


class GithubBackend(BaseBackend):

    def __init__(self, gh_owner, gh_repo, formatter=MardownFormatter()):
        """
        :param gh_owner: Name of the owner of the github repository.
        :param gh_repo: Name of the repository on github.
        """
        super(GithubBackend, self).__init__(
            formatter, "Submit on github",
            "Submit the issue on our issue tracker on github", None)
        icon = GH_MARK_NORMAL
        if QtWidgets.qApp.palette().base().color().lightness() < 128:
            icon = GH_MARK_LIGHT
        self.button_icon = QtGui.QIcon(icon)
        self.gh_owner = gh_owner
        self.gh_repo = gh_repo
        self._show_msgbox = True  # False when running the test suite

    def send_report(self, title, body, application_log=None):
        _logger().debug('sending bug report on github\ntitle=%s\nbody=%s',
                        title, body)
        username, password, remember, is_basic, remember_token, token = self.get_user_credentials()
        _logger().debug('got user credentials')

        try:
            '''
            print('username is',username)
            print('pass is',password)
            print('is basic',is_basic)
            print('remember token',remember_token)
            print('token is',token)'''

            if not is_basic:
                gh = github.Github(username)
            else:
                gh = github.Github(username,password)
            # upload log file as a gist
            if application_log:
                url = self.upload_log_file(application_log,gh,username, is_basic)
                body += '\nApplication log: %s' % url
            if url is None:
                return False
            repo = gh.get_repo(str(self.gh_owner)+'/'+str(self.gh_repo))
            ret = repo.create_issue(title=title, body=body)
            '''labels = repo.get_labels()
            for x in labels:
                print(x)
            print(repo.get_topics(),'got this')'''
        except Exception as e:
            QtWidgets.qApp.restoreOverrideCursor()
            _logger().warn('failed to send bug report on github. %s' % type(e).__name__)
            # invalid credentials
            if e.status == 401:
                if is_basic:
                    self.qsettings().setValue('github/remember_credentials', 0)
                else:
                    self.qsettings().setValue('github/remember_token', 0)
                if self._show_msgbox:
                    QtWidgets.QMessageBox.warning(
                        self.parent_widget, 'Invalid credentials',
                        'Failed to create github issue, invalid credentials...')
            else:
                # other issue
                if self._show_msgbox:
                    QtWidgets.QMessageBox.warning(
                        self.parent_widget,
                        'Failed to create issue',
                        'Failed to create github issue. Error %s' %
                        type(e).__name__+"\n \n"+"NOTE: If you are using Two Factor Authentication. Please Sign in using Access Token.")
            return False
        else:
            #issue_nbr = ret['number']
            issue_nbr = ret.number
            if self._show_msgbox:
                ret = QtWidgets.QMessageBox.question(
                    self.parent_widget, 'Issue created on github',
                    'Issue successfully created. Would you like to open the '
                    'ticket in your web browser?')
            if ret in [QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Ok]:
                webbrowser.open(
                    'https://github.com/%s/%s/issues/%d' % (
                        self.gh_owner, self.gh_repo, issue_nbr))
            return True

    def _get_credentials_from_qsettings(self):
        remember = self.qsettings().value('github/remember_credentials', "0")
        username = self.qsettings().value('github/username', "")
        password = self.qsettings().value('github/password', "")
        remember_token = self.qsettings().value('github/remember_token', "0")
        token = self.qsettings().value('github/token', "")
        try:
            # PyQt5 or PyQt4 api v2
            remember = bool(int(remember))
            remember_token = bool(int(remember_token))

        except TypeError:  # pragma: no cover
            # pyside returns QVariants
            remember, _ok = remember.toInt()
            remember_token, _ok = remember_token.toInt()
            username = username.toString()
            password = password.toString()
            token = token.toString()

        if not remember:
            username = ''
            password = ''
        if not remember_token:
            token = ''
        return username, bool(remember), password, remember_token, token

    def _store_credentials(self, username, password, remember, is_basic, remember_token, token):
        if is_basic:
            self.qsettings().setValue('github/username', username)
            self.qsettings().setValue('github/password', password)
            self.qsettings().setValue('github/remember_credentials', int(remember))
        else:
            self.qsettings().setValue('github/remember_token', int(remember_token))
            self.qsettings().setValue('github/token', token)



    def get_user_credentials(self):  # pragma: no cover
        # reason: hard to test methods that shows modal dialogs
        username, remember, password, remember_token, token = self._get_credentials_from_qsettings()
        '''print('username is',username)
        print('pass is',password)
        print('remember token',remember_token)
        print('token is',token)
        print('llllllllllllllllllllllll')'''
        # ask for credentials
        username, password, remember, is_basic, remember_token, token = DlgGitHubLogin.login(
            self.parent_widget, username, remember, password, remember_token, token)
        '''print('username is',username)
        print('pass is',password)
        print('remember token',remember_token)
        print('remember is',remember)
        print('token is',token)
        print('is_basic',is_basic)
        print('llllllllllllllllllllllll  jjjjjjjjjjjjjjjjjjjjjjj' )'''
        self._store_credentials(username, password, remember, is_basic, remember_token, token)

        return username, password, remember, is_basic, remember_token, token

    def upload_log_file(self, log_content, gh, username, is_basic):
        try:
            QtWidgets.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
            '''data = {
                "public": True,
                "files": {
                    "Osdag_crash_log.log": {
                        "content": log_content
                    },
                }
            }
            if is_basic:
                auth = gh.get_user()
                ret = auth.create_gist(True, {"Osdag_crash_log.log": github.InputFileContent(log_content)},"Osdag crash report.")
                ret = str(ret.id)
                ret = 'https://gist.github.com/' + ret
            else:
                query_url = "https://api.github.com/gists"
                headers = {'Authorization': f'token {username}'}
                r = requests.post(query_url, headers=headers, data=json.dumps(data))
                ret = r.json()
                ret = ret['html_url']'''
            auth = gh.get_user()
            ret = auth.create_gist(True, {"Osdag_crash_log.log": github.InputFileContent(log_content)},"Osdag crash report.")
            ret = str(ret.id)
            ret = 'https://gist.github.com/' + ret
            QtWidgets.qApp.restoreOverrideCursor()
        except Exception as e:

            QtWidgets.qApp.restoreOverrideCursor()
            QtWidgets.QMessageBox.warning(
                self.parent_widget, 'Error',
                'Unable to create gist. {}'.format(type(e).__name__)+"\n \n"+"NOTE:  If you are using Two Factor Authentication. Please Sign in using Access Token.")
            if is_basic:
                self.qsettings().setValue('github/remember_credentials', 0)
            else:
                self.qsettings().setValue('github/remember_token', 0)
            return None
        else:
            return ret
