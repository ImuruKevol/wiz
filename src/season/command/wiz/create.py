import os
import shutil
from argh import arg, expects_obj
from git import Repo
import socket
import json

def portchecker(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port = int(port)
        s.connect(("127.0.0.1", port))
        return True
    except:
        pass
    return False

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

@arg('projectname', default='sample-project', help='project name')
@arg('--uri', help='https://github.com/season-framework/wiz-demo')
def create(projectname, uri="https://github.com/season-framework/wiz-demo"):
    PATH_FRAMEWORK = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    PATH_PROJECT = os.path.join(os.getcwd(), projectname)

    if os.path.isdir(PATH_PROJECT):
        return print("Already exists project path '{}'".format(PATH_PROJECT))

    # install default structures
    print("create project...")
    PATH_PUBLIC_SRC = os.path.join(PATH_FRAMEWORK, 'data', 'wizbase')
    shutil.copytree(PATH_PUBLIC_SRC, PATH_PROJECT)

    # port finder
    startport = 3000
    while portchecker(startport):
        startport = startport + 1
    
    CONFIG_PATH = os.path.join(PATH_PROJECT, 'config', 'config.py')
    f = open(CONFIG_PATH, 'r')
    data = f.read()
    f.close()
    data = data.replace("__PORT__", str(startport))
    f = open(CONFIG_PATH, 'w')
    f.write(data)
    f.close()

    
    print("install base branch...")
    branch_path = os.path.join(PATH_PROJECT, 'branch', 'master')
    Repo.clone_from(uri, branch_path)


    plugins = {
        "core.setting": "wiz-plugin-setting",
        "core.branch": "wiz-plugin-branch",
        "core.workspace": "wiz-plugin-workspace",
        "theme": "wiz-plugin-theme",
    }
    plugin_config = os.path.join(branch_path, "config", "plugin.json")
    if os.path.isfile(plugin_config):
        with open(plugin_config, "r") as f:
            config = f.read()
            try:
                config = json.loads(config)
            except:
                print(f"Is not valid {}", plugin_config)
                return
            for key in config:
                val = config[key]
                plugins[key] = val
        
    for plugin_name in plugins:
        info = {}
        if type(config[plugin_name]) == str:
            info["repo"] = config[plugin_name]
        else:
            info = config[plugin_name]
        if type(info) != dict:
            print(f"Is not valid {}", plugin_config)
            return
        if "base" not in info:
            info["base"] = "https://github.com"
        if "owner" not in info:
            info["owner"] = "season-framework"
        if "repo" not in info:
            info["repo"] = plugin_name
        if "version" not in info:
            info["version"] = None
        if info["version"] in ["", "lts", "last"]:
            info["version"] = None
        
        print(f"install plugin... ({})", plugin_name)
        repo_path = os.path.join(info["base"], info["owner"], info["repo"])
        kwargs = {}
        if info["version"] is not None:
            kwargs["branch"] = info["version"]
        plugin_path = os.path.join(PATH_PROJECT, 'plugin', plugin_name)
        Repo.clone_from(repo_path, plugin_path, **kwargs)

            


    # install plugins
    #print("install plugin... (setting)")
    #Repo.clone_from('https://github.com/season-framework/wiz-plugin-setting', os.path.join(PATH_PROJECT, 'plugin', 'core.setting'))
    #print("install plugin... (branch)")
    #Repo.clone_from('https://github.com/season-framework/wiz-plugin-branch', os.path.join(PATH_PROJECT, 'plugin', 'core.branch'))
    #print("install plugin... (workspace)")
    #Repo.clone_from('https://github.com/season-framework/wiz-plugin-workspace', os.path.join(PATH_PROJECT, 'plugin', 'core.workspace'))
    #print("install plugin... (theme)")
    #Repo.clone_from('https://github.com/season-framework/wiz-plugin-theme', os.path.join(PATH_PROJECT, 'plugin', 'theme'))

    # print("install base branch...")
    # Repo.clone_from(uri, os.path.join(PATH_PROJECT, 'branch', 'master'))

    gitpath = os.path.join(PATH_PROJECT, 'branch', 'master', '.git')
    try:
        shutil.rmtree(gitpath)
    except:
        try:
            os.remove(gitpath)
        except:
            pass
