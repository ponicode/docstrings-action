import os
import sys
import loguru
import copy
import requests
import json
from termcolor import colored
import tqdm 

def convert_py2string(PATH):
    filename = PATH
    with open(filename) as f:
        content = f.readlines()
    for i in range(len(content)):
        content[i] = content[i].replace('"', '\"').replace("'", "\'")
    code = ''.join(content)
    return code

def add_doc2pyfile(doc_dict):
    PATH = doc_dict['path']
    code = doc_dict['code']
    f = open(PATH, "w+")
    f.write(code)
    f.close()

class DocRepo:
    def __init__(self, language, version, auth_token, git_info):
        language = 'python'
        self.language = language
        self.headers = {'Authorization': 'Bearer: ' + auth_token.rstrip(), 'X-version':version}
        self.git_info = git_info

    def get_files_paths(self, repo_path):
            """Get list of testable files"""
            forbidden_words = []
            testable_files = []
            for path, subdirs, files in os.walk(repo_path):
                for name in files:
                    total_path = os.path.join(path, name)
                    if total_path.endswith('.py'):
                        add = True
                        for forbidden_word in forbidden_words:
                            if forbidden_word in total_path:
                                add = False
                        if add:
                            testable_files.append(os.path.abspath(total_path))
            return testable_files
        
    
    def get_docstring_dict(self, code_dict):
        url = 'https://api.ponicode.com/civet/suggest'
        r = requests.post(url, headers=self.headers, json=code_dict, timeout=600)
        r = r.json()
        return r

    def doc_repo(self, repo_path):
        """Add docstrings to all python files in the repo"""
        # Remove file because unused - try/except because if it doesn't exists
        try:
            os.remove('PATHS_TO_CHANGED_FILES.txt')
        except:
            pass
        # Get python files paths
        filespaths = self.get_files_paths(repo_path)
        number_files = len(filespaths)
        loguru.logger.info(colored(f'{number_files} files found', 'green'))
        
        for path in tqdm.tqdm(filespaths):
            print('GA_START',path)
            request = self.run_request(path)
            print('GA_END',path)
            add_doc2pyfile(request)
            loguru.logger.info(colored(f'Add docstrings to a new file', 'green'))

    def doc_repo_from_commit(self, repo_path):
        """Add docstrings to all python files in the repo"""
        # Get python files paths
        with open('PATHS_TO_CHANGED_FILES.txt') as f:
            filespaths = f.readlines()
        f.close()
        os.remove('PATHS_TO_CHANGED_FILES.txt')
        number_files = len(filespaths)
        loguru.logger.info(colored(f'{number_files} files found', 'green'))
        for path in tqdm.tqdm(filespaths):
            path = path[:-1]
            if path.endswith('.py'):
                path = os.path.join(repo_path, path)
                request = self.run_request(path)
                add_doc2pyfile(request)
                loguru.logger.info(colored(f'Add docstrings to a new file', 'green'))

    def run_request(self, path):
        code_string = convert_py2string(path)
        code_dict = {"code": code_string, "path": path, 'gitInfo': self.git_info, 'enable_template': enable_template}
        request = self.get_docstring_dict(code_dict)
        if (request['status'] < 200 or request['status'] >= 300):
            raise RuntimeError(f'{request}')
        elif (request['status'] >= 500):
            raise RuntimeError('internal server error')
        else:
            return request


if __name__ == '__main__':
    _, repo_path, auth_token, all_repo, enable_template = sys.argv
    repo_path = os.path.abspath(repo_path)

    git_info = {
       "userName": os.environ['GITHUB_ACTOR'],
       "repoName": os.environ['GITHUB_REPOSITORY'],
       "workflowName": os.environ['GITHUB_WORKFLOW'],
       "jobId": '',
       "runId": os.environ['GITHUB_RUN_ID']
    }

    version = '0.21.0'
    language = 'python'
    DR = DocRepo(language, version, auth_token, git_info)

    try:
        if (all_repo.lower() == 'true'):
            DR.doc_repo(repo_path)
        else:
            DR.doc_repo_from_commit(repo_path)
    except RuntimeError as err:
        print('Server Error')
        if (err == 'internal server error'): 
            pass

        
