# -*- coding:utf-8 -*-
"""
Author: weizhen
Time: 2021/3/26 17:15
description: it just a test
"""

import os, os.path, shutil
import json
import PTBase as cgc
import FTShortcut as fts
import re


class Project(cgc.ProjectTreeRoot):
    def __init__(self, project_config_class, parent, process='wip'):
        """
        :param project_config_class: is a instance of the cgc.ProjectConfig
        :param process: wip or publish or something else
        """
        # initial values
        self.process = process

        # project config
        self.configuration_class = project_config_class
        self.project_config = self.configuration_class.getprojectConfig()

        # read project config dict to set the initial values
        self.name = self.project_name = self.project_config["project_name"]
        self.project_path = self.configuration_class.getProjectPath()
        self.ani_path = self.configuration_class.getAniPath()
        self.asset_path = self.configuration_class.getAssetPath()
        self.cmp_path = self.configuration_class.getCmpPath()
        self.fx_path = self.configuration_class.getFxPath()

        super(Project, self).__init__(name=self.name, process=self.process)
        self.parent = parent

        # create local network folders
        self.createTreeMap(self.getFullPath())

    def getConfigPath(self):
        return self.configuration_class.getConfigPath()

    def getRootPath(self):
        return os.path.dirname(self.project_path)

    def getChild(self, context_name):
        if 'asset' in context_name or 'shot' in context_name:
            return Context(project_config_class=self.configuration_class, context_name=context_name,
                           parent=self, process=self.process)
        else:
            return None

    def getChildren(self, process='wip'):
        return [x for x in os.listdir(os.path.join(self.getFullPath(), process)) if os.path.isdir(os.path.join(self.getFullPath(), process, x))]

    def getParent(self):
        return self.parent

    def getParents(self):
        return [self.getParent()]

    def getFullPath(self):
        return self.project_path

    def getScene(self):
        return fts.getScenes(self.project_name)

    def getName(self):
        return self.project_name

    def delete(self):
        print("You should not delete file in this layer")
        raise PermissionError

    def getProjectName(self):
        return self.project_name
    """
    def addChild(self):
        pass

    def addChildren(self):
        pass

    def setName(self, name):
        self.project_name = name

    def createLocalFolders(self):
        pass
    """


class Context(cgc.ProjectTreeRoot):
    def __init__(self, project_config_class, context_name, parent, process='wip'):
        self.project_config_class = project_config_class
        self.project_name = self.project_config_class.getProjectName()
        self.name = self.context_name = context_name
        self.process = process

        super(Context, self).__init__(name=self.name, process=self.process)
        self.parent = parent

        # create local network folders
        self.createTreeMap(self.getFullPath())

    def getChild(self, context_name, asset_type_name):
        if 'asset' in context_name:
            result = self.getAssetType(asset_type_name)
        elif 'shot' in context_name:
            result = self.getScene(asset_type_name)
        else:
            result = None

        return result

    def getChildren(self, context_name):
        if 'asset' in context_name:
            result = fts.getAssetTypes(project_name=self.project_name)
        elif 'shot' in context_name:
            result = fts.getScenes(project_name=self.project_name)
        else:
            result = None

        return result

    def getParent(self):
        return self.parent

    def getParents(self):
        elders = self.parent.getParents()
        elders.append(self.parent)
        return elders

    def getFullPath(self):
        return os.path.join(self.parent.getFullPath(), self.process, self.context_name)

    def getAssetType(self, asset_type_name):
        return fts.getAssetType(project_name=self.project_name, asset_type_name=asset_type_name)

    def getScene(self, scene_name):
        return fts.getScene(project_name=self.project_name, scene_name=scene_name)

    def getName(self):
        return self.context_name

    def setName(self, name):
        self.name = self.context_name = name

    def getProjectName(self):
        return self.project_name

    def addChild(self):
        pass

    def addChildren(self):
        pass

    def delete(self):
        return self.parent.delete


class Category(cgc.ProjectTreeRoot):
    """
    context type is asset、shot、rnd/cpt
    scene name = asset type name = category name
    """
    def __init__(self, project_config_class, category_name, parent, process='wip'):
        self.project_config_class = project_config_class
        self.project_name = self.project_config_class.getProjectName()
        self.name = self.category_name = category_name
        self.process = process

        super(Category, self).__init__(name=self.name, process=self.process)
        self.parent = parent

        # create local network folders
        self.createTreeMap(self.getFullPath())

    def getParent(self):
        return self.parent

    def getParents(self):
        elders = self.parent.getParents()
        elders.append(self.parent)
        return elders

    def getName(self):
        return self.category_name

    def getFullPath(self):
        return os.path.join(self.getParent().getFullPath(), self.name)

    def getChild(self, context_name, name):
        if 'asset' in context_name:
            result = self.getAsset(asset_name=name)
        elif 'shot' in context_name:
            result = self.getShot(shot_name=name)
        else:
            result = None

        return result

    def getChildren(self, context_name):
        if 'asset' in context_name:
            result = fts.getAssetBuilds(project_name=self.project_name, asset_type=self.category_name)
        elif 'shot' in context_name:
            result = fts.getShots(project_name=self.project_name, scene_name=self.category_name)
        else:
            result = None

        return result

    def getShot(self, shot_name):
        return fts.getShot(project_name=self.project_name, scene_name=self.category_name, shot_name=shot_name)

    def getAsset(self, asset_name):
        return fts.getAssetBuild(project_name=self.project_name, asset_type=self.category_name, asset_name=asset_name)

    def getScene(self):
        return fts.getScene(project_name=self.project_name, scene_name=self.category_name)

    def setName(self, name):
        self.name = self.category_name = name

    def getProjectName(self):
        return self.project_name

    def addChild(self):
        pass

    def addChildren(self):
        pass

    def delete(self):
        return self.parent.delete


class Object(cgc.ProjectTreeRoot):
    """
    context type is asset、shot、rnd/cpt
    scene name = asset type name = category name
    stage name = task name
    """
    def __init__(self, project_config_class, object_name, parent, process='wip'):
        self.project_config_class = project_config_class
        self.project_name = self.project_config_class.getProjectName()
        self.category_name = parent.name
        self.name = self.object_name = object_name
        self.process = process
        super(Object, self).__init__(name=self.name, process=self.process)
        self.parent = parent

        # create local network folders
        self.createTreeMap(self.getFullPath())

    def getParent(self):
        return self.parent

    def getParents(self):
        elders = self.parent.getParents()
        elders.append(self.parent)
        return elders

    def getName(self):
        return self.name

    def getFullPath(self):
        return os.path.join(self.getParent().getFullPath(), self.name)

    def getChild(self, context_name, task_name):
        tasks = self.getChildren(context_name=context_name)
        if tasks:
            child = tasks[task_name]
            return child
        else:
            return None

    def getChildren(self, context_name):
        tasks = fts.getTasks(project_name=self.project_name, context_name=context_name, category_name=self.category_name,
                     object_name=self.name)

        return tasks

    def getTask(self, context_name, task_name):
        self.getChild(context_name=context_name, task_name=task_name)

    def getTasks(self, context_name):
        self.getChildren(context_name=context_name)

    def setName(self, name):
        self.name = self.object_name = name

    def getProjectName(self):
        return self.project_name

    def addChild(self, context_name, task_name):
        result = fts.addTask(project_name=self.project_name, context_name=context_name, category_name=self.category_name,
                    object_name=self.name, task_name=task_name)

        if result:
            return True
        else:
            return False

    def addChildren(self, task_dict):
        if isinstance(task_dict, dict):
            for key in task_dict:
                try:
                    self.addChild(context_name=key, task_name=task_dict[key])
                except KeyError:
                    continue

    def delete(self, context_type):
        if 'asset' in context_type:
            result = fts.deleteAssetBuild(project_name=self.project_name, asset_type=context_type, asset_name=self.object_name)
        elif 'shot' in context_type:
            result = fts.deleteShot(project_name=self.project_name, scene_name=context_type, shot_name=self.object_name)
        else:
            result = False

        return result


class Stage(cgc.ProjectTreeRoot, cgc.StageMapping):
    def __init__(self, project_config_class, stage_name, parent, process='wip'):
        self.project_config_class = project_config_class
        self.project_name = self.project_config_class.getProjectName()
        self.object_name = parent.name
        self.name = self.stage_name = stage_name
        self.process = process
        super(Stage, self).__init__(name=self.name, process=self.process)
        self.parent = parent

        # create local network folders
        self.createTreeMap(self.getFullPath())

    # def getCurrentCache(self):
    #     return os.path.join(self.getFullPath(), self.getCurrentVersion(), "cache")

    def getCurrentVersion(self, context_name, category_name):
        result = self.getVersions(context_name=context_name, category_name=category_name)
        # if result:
        #     result
        return result

    def getVersions(self, context_name, category_name):
        # print(self.project_name, context_name, category_name, self.object_name, self.name)
        return fts.getVersions(project_name=self.project_name, context_name=context_name, category_name=category_name,
                               object_name=self.object_name, task_name=self.name)

    def getFullPath(self):
        return os.path.join(self.getParent().getFullPath(), self.name)

    def getParent(self):
        return self.parent

    def getParents(self):
        elders = self.parent.getParents()
        elders.append(self.parent)
        return elders

    def createTreeMap(self, path):
        if self.name not in cgc.StageMapping.getLocalFields():
            print("%s is not included in the Mapping Dictionary" % self.name)
            raise KeyError

        cgc.Root.createTreeMap(path)

    # def getPreview(self):
    #     return os.path.join(self.getFullPath(), self.getCurrentVersion(), "preview")
    #
    # def getProjectFiles(self):
    #     return [(os.path.join(self.getFullPath(), x)).replace('\\', '/') for x in os.listdir(self.getFullPath())
    #             if os.path.isfile(os.path.join(self.getFullPath(), x))]


class Version(cgc.ProjectTreeRoot, cgc.StageMapping):
    def __init__(self, project_config_class, version_num, parent, process='wip'):
        self.project_config_class = project_config_class
        self.project_name = self.project_config_class.getProjectName()
        self.stage_name = parent.name
        self.object_name = parent.object_name
        self.name = self.version_name = self.initialVersionName(version_num)
        self.process = process

        super(Version, self).__init__(name=self.name, process=self.process)
        self.parent = parent

        # create local network folders
        self.cache_path = os.path.join(self.getFullPath(), 'cache')
        self.preview_path = os.path.join(self.getFullPath(), 'preview')

        self.createTreeMap(self.getFullPath())
        self.createTreeMap(self.cache_path)
        self.createTreeMap(self.preview_path)

    def initialVersionName(self, version_num):
        if 'v' in version_num:
            version_num = version_num.split('v')[-1]

        version_num = 'v' + "%03d" % int(version_num)
        version_name = "%s_%s_%s_%s" % (self.object_name, self.getFieldAbbr(self.stage_name), self.stage_name,
                                        version_num)

        return version_name

    def getFullPath(self):
        return os.path.join(self.getParent().getFullPath(), self.name)

    def getCache(self):
        return [(os.path.join(self.cache_path, x)).replace('\\', '/') for x in os.listdir(self.cache_path)]

    def getParent(self):
        return self.parent

    def getPreview(self):
        return [(os.path.join(self.preview_path, x)).replace('\\', '/') for x in os.listdir(self.preview_path)]

    def getProjectFiles(self):
        return [(os.path.join(self.getFullPath(), x)).replace('\\', '/') for x in os.listdir(self.getFullPath())
                if os.path.isfile(os.path.join(self.getFullPath(), x))]

    def getVersionNum(self):
        result = re.search(r'[0-9]{3,3}$', self.version_name)

        if result:
            return result.group()

    def setName(self, name):
        self.name = self.version_name = name

    # def addVersion(self):
    #     pass
    #
    # def changeVersion(self, version_num):
    #     self.name = self.version_name = self.initialVersionName(version_num)
    #
    # def deleteCurrentVersion(self):
    #     # local delete
    #     shutil.rmtree(self.getFullPath())
    #
    #     # ftrack delete

    def deletePreviews(self):
        shutil.rmtree(self.preview_path)
        self.createTreeMap(self.preview_path)

    def deleteCaches(self):
        shutil.rmtree(self.cache_path)
        self.createTreeMap(self.cache_path)

    def deleteProjectFiles(self):
        files = self.getProjectFiles()
        if files:
            for f in files:
                os.remove(f)


if __name__ == '__main__':
    # initial values
    root_path = r'I:\ProjectTree\Root'
    pj_config_cls = cgc.ProjectConfig(root_path=root_path, project_name='lfc')
    ptr = cgc.ProjectTreeRoot()

    pj_lfc = Project(pj_config_cls, parent=ptr, process=r'wip')
    # print(pj_lfc.getConfigPath())
    # print(pj_lfc.getRootPath())
    # print(pj_lfc.getChild('asset'))
    # print(pj_lfc.getChild('shot'))
    # print(pj_lfc.getChildren())
    # print(pj_lfc.getParent())
    # print(pj_lfc.getParents())
    # print(pj_lfc.getFullPath())
    # print(pj_lfc.getScene())
    # print(pj_lfc.delete())
    # print(pj_lfc.getName())
    # print(pj_lfc.getProjectName())

    ctx_lfc = Context(project_config_class=pj_config_cls, context_name='shot', parent=pj_lfc)
    # print(ctx_lfc.name)
    # print(ctx_lfc.getParent())
    # print(ctx_lfc.getParents())
    # print(ctx_lfc.getChildren(context_name='asset'))
    # print(ctx_lfc.getChildren(context_name='shot'))
    # print(ctx_lfc.getFullPath())
    # ctx_lfc.setName('asset')
    # ctx_lfc.setProcess('publish')
    # print(ctx_lfc.process)

    cate = Category(project_config_class=pj_config_cls, category_name='c10', parent=ctx_lfc)
    # print(cate.name)
    # print(cate.getParent())
    # print(cate.getParents())
    # print(cate.getFullPath())
    # print(cate.getChild(context_name='shot', name='b10010'))
    # print(cate.getChildren(context_name='shot'))
    # print(cate.getChildren(context_name='shot'))

    # cate.setName('chr')
    # print(cate.getChild(context_name='asset', name='example_a'))
    # print(cate.getChildren(context_name='asset'))

    obj = Object(project_config_class=pj_config_cls, object_name='c10050', parent=cate)
    # print(obj.getChild(context_name, task_name))
    # # print(obj.project_name, obj.category_name, obj.name, obj.process)
    print(obj.getFullPath())
    # print(obj.getParent())
    # print(obj.getParents())
    # obj.setName('example_a')
    # print(obj.getFullPath())
    # print(obj.getChildren(context_name='shot'))
    # print(obj.getChild(context_name='shot', task_name='Blocking'))

    print('-'*50)
    sta = Stage(project_config_class=pj_config_cls, stage_name='Blocking', parent=obj)
    # print(sta.name, sta.parent.name)
    # print(sta.getFullPath())
    # print(sta.getParent())
    # print(sta.getParents())
    # print(sta.getProjectFiles())
    # print(sta.getVersions(context_name='shot', category_name='c10'))
    # print(sta.mapping)
    # print(sta.getLocalFields())
    # print(sta.getFTFields())
    # print(fts.getTasks('lfc','shot','c10','c10010'))
    # print(fts.getVersions("lfc", "shot", "c10", "c10010", "Blocking"))
    # print(sta.getProjectFiles())

    # vsn = Version(project_config_class=pj_config_cls, version_num="v001", parent=sta, process='wip')
    # print(vsn.getFullPath())
    # print(vsn.name)
    # print(vsn.getCache())
    # print(vsn.getPreview())
    # print(vsn.getProjectFiles())
    # print(vsn.getVersionNum())
    #
    # vsn.deletePreviews()
    # vsn.deleteCaches()
    # vsn.deleteProjectFiles()
