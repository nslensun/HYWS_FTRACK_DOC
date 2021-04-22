# -*- coding:utf-8 -*-
"""
Author: weizhen
Time: 2021/3/30 16:55
description:
"""

import os, os.path
import json
import FTShortcut as fts


class Root(object):
    def __init__(self):
        """
        root class of project tree
        """
        pass

    @classmethod
    def createTreeMap(cls, path):
        try:
            os.makedirs(path)
        except OSError:
            if os.path.exists(path):
                pass
            else:
                print("Read/Write Root Path fail, please check windows path")
                raise WindowsError


class ProjectTreeRoot(Root):
    def __init__(self, name='root', process='wip'):
        super(ProjectTreeRoot, self).__init__()
        self.name = name
        self.process = process
        self.parent = None

    def getProcess(self):
        return self.process

    def getProjects(self):
        return fts.getProjects()

    def getProject(self, project_name):
        return fts.getProject(project_name)

    def getProjectConfig(self, project_name):
        pass

    def setProcess(self, process):
        self.process = process

    def getName(self):
        return self.name

    def getChild(self, **kwargs):
        pass

    def getChildren(self, **kwargs):
        pass

    def getParent(self):
        return Root()

    def getParents(self):
        return [Root()]

    def getFullPath(self, **kwargs):
        pass

    def addChild(self, **kwargs):
        pass

    def addChildren(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def setName(self, name):
        self.name = name

    def getProjectName(self):
        pass


class StageMapping(Root):
    mapping = json.load(open(r'./mapping.json', 'r'))

    def __init__(self):
        super(StageMapping, self).__init__()
        # print(self.mapping)
        # print(self.getFTFields())
        # print(self.getLocalFields())

    @classmethod
    def getFTFields(cls):
        return list(cls.mapping.keys())

    @classmethod
    def getLocalFields(cls):
        return list(cls.mapping.keys())

    @classmethod
    def getFieldAbbr(cls, field):
        return cls.mapping.get(field)['abbr']

    @classmethod
    def getFieldFull(cls, field):
        return cls.mapping.get(field)['full']




class ProjectConfig(Root):
    project_config = dict()
    project_config["root_path"] = r'I:\ProjectTree\Root'
    project_config["asset_path"] = r'I:\ProjectTree\Root\lfc'
    project_config["cmp_path"] = r'I:\ProjectTree\Root\lfc'
    project_config["fx_path"] = r'I:\ProjectTree\Root\lfc'
    project_config["ani_path"] = r'I:\ProjectTree\Root\lfc'
    project_config['context_fields'] = ['asset', 'shot', 'rnd', 'mp']

    def __init__(self, root_path=r'I:\ProjectTree\Root\lfc', project_name=r'lfc'):
        super(ProjectConfig, self).__init__()
        self.project_path = self.project_config["project_path"] = os.path.join(root_path, project_name)
        self.project_name = self.project_config["project_name"] = project_name
        project_config_name = r'project_config.json'
        self.project_config_path = os.path.normpath(os.path.join(self.project_path, project_config_name))

        if os.path.exists(self.project_config_path):
            self.readConfigFile()
        else:
            self.writeConfigFile()

    def getConfig(self):
        return self.project_config

    def getConfigFile(self):
        return self.project_config

    def readConfigFile(self):
        config_json = open(self.project_config_path, 'r')
        self.project_config = json.load(config_json)
        config_json.close()

    def writeConfigFile(self, project_config_path=None, project_config=None):
        if not project_config_path:
            project_config_path = self.project_config_path
        if not project_config:
            project_config = self.project_config

        self.createTreeMap(self.project_path)
        with open(project_config_path, 'w') as config_json:
            json.dump(project_config, config_json)
            config_json.close()

    def addValues(self, key, value):
        if not str(key) in self.project_config.keys():
            self.project_config[str(key)] = str(value)
            with open(self.getConfigFile(), 'w') as config_json:
                json.dump(self.project_config, config_json)

    def getConfigPath(self):
        return self.project_config_path

    def getprojectConfig(self):
        return self.project_config

    def getProjectName(self):
        return self.project_config["project_name"]

    def getRootPath(self):
        return self.project_config["root_path"]

    def getProjectPath(self):
        return self.project_config["project_path"]

    def getAniPath(self):
        return self.project_config["ani_path"]

    def getAssetPath(self):
        return self.project_config["asset_path"]

    def getCmpPath(self):
        return self.project_config["cmp_path"]

    def getFxPath(self):
        return self.project_config["fx_path"]


if __name__ == '__main__':
    # rp = r'I:\ProjectTree\Root'
    # rt = Root()
    # pj_config_cls = ProjectConfig(root_path=rp, project_name='lfc')

    smp = StageMapping()
    print(smp.getLocalFields())

