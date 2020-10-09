# 🦄 Automatically write docstrings for your code!🦄
This github action generates docstrings for your **Python** functions with the Ponicode AI engine (this action is currently in beta version)
```yaml
- uses: ponicode/docstrings-action@master
  with:
    repo_path: ./
    all_repo: False
```
Once the docstrings are written, use the [create pull request action](https://github.com/peter-evans/create-pull-request) to see the results in the branch of your choice
```yaml
- name: Create Pull Request
  uses: peter-evans/create-pull-request@v2
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    commit-message: '[ponicode-pull-request] Ponicode found docstrings to write!'
    branch: ponicode-docstrings
    title: '[Ponicode] Docstrings created'
    body: |
        Ponicode report
        - Ponicode found docstrings to write
        - Auto-generated by Ponicode
```
## Terms of use
By using this action, Ponicode will send the content of all the Python files of your project to the Ponicode API in order to provide you with relevant information.
# How to setup
## Create a yaml workflow file in your project
Go to the root of your project, and create the path to your workflow file. For example
```
mkdir -p .github/workflows
```
Here is an example of what to put in your ```.github/workflows/ponicode.yml``` file to trigger the action.
```yaml
name: Ponicode docstrings generation

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ master ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with: 
        fetch-depth: 0
    - name: Get paths
      run: |
        git show --pretty="" --name-only ${{ github.sha }} > PATHS_TO_CHANGED_FILES.txt
    - uses: ponicode/docstrings-action@master
      with:
        repo_path: ./
        all_repo: True
      # Creates pull request with all changes in file
    - name: Create Pull Request 
      uses: peter-evans/create-pull-request@v2 
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: '[ponicode-pull-request] Ponicode wrote new docstrings!'
        branch: ponicode-docstring
        title: '[Ponicode] Docstrings created'
        body: |
            Ponicode report
            - Ponicode found undocumented functions
            - Auto-generated by Ponicode
```
**This yaml file writes docstrings on your undocumented Python functions everytime you push on master and makes a pull request on a ponicode-docstrings branch with the docstrings created**

# Ponicode Action inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| ``repo_path`` | The relative path in your repo to the files you want Ponicode to test. By default, Ponicode tests your whole repo. | true | ``./`` |
| ``all_repo`` | Boolean. By default, the value is False. Choose if you want to write docstrings only on the files you just commited (False) or on all your repository (True)| true |`` False`` |

# Use cases:
### Trigger Ponicode action on push on ``custom`` branch.
```yaml
name: Ponicode docstrings generation

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ custom ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with: 
        fetch-depth: 0
    - name: Get paths
      run: |
        git show --pretty="" --name-only ${{ github.sha }} > PATHS_TO_CHANGED_FILES.txt
    - uses: ponicode/docstrings-action@master
      with:
        repo_path: ./
        all_repo: True
      # Creates pull request with all changes in file
    - name: Create Pull Request 
      uses: peter-evans/create-pull-request@v2 
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: '[ponicode-pull-request] Ponicode wrote new docstrings!'
        branch: ponicode-docstring
        title: '[Ponicode] Docstrings created'
        body: |
            Ponicode report
            - Ponicode found undocumented functions
            - Auto-generated by Ponicode
```
### Trigger Ponicode action when you push on ``master`` or when you make a pull request on ``custom`` branch
```yaml
name: Ponicode docstrings generation

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ custom ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with: 
        fetch-depth: 0
    - name: Get paths
      run: |
        git show --pretty="" --name-only ${{ github.sha }} > PATHS_TO_CHANGED_FILES.txt
    - uses: ponicode/docstrings-action@master
      with:
        repo_path: ./
        all_repo: True
      # Creates pull request with all changes in file
    - name: Create Pull Request 
      uses: peter-evans/create-pull-request@v2 
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: '[ponicode-pull-request] Ponicode wrote new docstrings!'
        branch: ponicode-docstring
        title: '[Ponicode] Docstrings created'
        body: |
            Ponicode report
            - Ponicode found undocumented functions
            - Auto-generated by Ponicode
```
### Trigger Ponicode action only on your last committed files (all_repo = False) when you push on ``master``
```yaml
name: Ponicode docstrings generation

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ master ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with: 
        fetch-depth: 0
    - name: Get paths
      run: |
        git show --pretty="" --name-only ${{ github.sha }} > PATHS_TO_CHANGED_FILES.txt
    - uses: ponicode/docstrings-action@master
      with:
        repo_path: ./
        all_repo: False
      # Creates pull request with all changes in file
    - name: Create Pull Request 
      uses: peter-evans/create-pull-request@v2 
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: '[ponicode-pull-request] Ponicode wrote new docstrings!'
        branch: ponicode-docstring
        title: '[Ponicode] Docstrings created'
        body: |
            Ponicode report
            - Ponicode found undocumented functions
            - Auto-generated by Ponicode
```
