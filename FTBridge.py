# coding=utf-8
# author:   Lensun
# contact:  lensun@nstation.net
# date:     2021/04/16
# version:  1.2.6

import os
import json
import ftrack_api

class FTBridge():
    '''An universal class for all FTBridge lower classes.'''

    def __init__(self):
        self.session = None
        self.id = None
        self.parent = None
        self.name = None
        self.entity = {}

    def mapping(self, keyword):
        '''Return the mapped object of *keyword*(string).'''
        with open("./mapping.json",'r') as json_file:
            return json.load(json_file)[keyword]

    def getTasks(self):
        '''Return a dict of BrTasks of the current instance.'''
        task_query = self.session.query(
            "select name, id from Task where parent.id is {0}".format(self.id)
        )
        self.task_entities = {}

        for task in task_query:
            self.task_entities[task['name']] = BrTask(self.session, task, self)

        return self.task_entities

    def getStatus(self):
        '''Return a dict of status of the current instance.'''
        status = self.entity['status']

        return {self.entity['status']['name']: status}

    def addTask(self, task_type=None, task_name='Default'):
        '''Add a ftrack task to the current instance. 
        
        *task_type* is in string type. If not specified, 'Generic' type will be used by default.
        *task_name* is in string type. If not specified, the task will be named 'Default'.
        '''
        if task_type:
            task_type = self.getTypes().get(task_type)
        else:
            task_type = self.getTypes().get('Generic')
        
        task = self.session.create(
            "Task", {
                'name': task_name,
                'type': task_type,
                'parent': self.entity,
            }
        )

        return BrTask(self.session, task, self)

    def getTypes(self):
        '''Return a dict of ftrack type instances.'''
        type_query = self.session.query(
            "select name, id from Type"
        )

        self.type_entities = {}

        for _type in type_query:
            self.type_entities[_type['name']] = _type

        return self.type_entities

    def getAssets(self):
        '''Return a dict of BrAssets of the current instance.'''
        asset_query = self.session.query(
            "select name, id from Asset where parent.id is {0}".format(self.parent.id)
        )

        self.asset_entities = {}

        for asset in asset_query:
            self.asset_entities[asset['name']] = BrAsset(self.session, asset, self.parent)

        return self.asset_entities

    def addAsset(self, asset_type="Upload"):
        '''Add a ftrack asset to the current instance. 
        
        *task_type* is in string type. If not specified, 'Generic' type will be used by default.
        *task_name* is in string type. If not specified, the task will be named 'Default'.
        '''
        asset_type = self.session.query('AssetType where name is {0}'.format(asset_type)).one()

        asset = self.session.create(
            "Asset", {
                'name': self.name,
                'type': asset_type,
                'parent': self.entity,
            }
        )

        self.session.commit()
        return BrAsset(self.session, asset, self.parent)

    def addVersion(self, version=None):
        asset_name = self.name
        if asset_name not in self.getAssets().keys():
            self.addAsset()

        asset = self.getAssets()[asset_name].entity

        if version:
            asset_version = self.session.create('AssetVersion', {
                    'asset': asset,
                    'version': version,
                    #'status_id': self.statusList[self.publishStatusBox.currentText()]
                    }
                )

        else:
            asset_version = self.session.create('AssetVersion', {
                    'asset': asset,
                    }
                )

        self.session.commit()
        return BrVersion(self.session, asset_version, self)

    def delete(self):
        self.session.delete(self.entity)
        self.session.commit()

class BrRoot(FTBridge):
    def __init__(self):
        super(BrRoot, self).__init__()
        #self.projects = self.getProjects()
        #self.users = self.getUsers()

        self.session = ftrack_api.Session(
            server_url='https://dovfx.ftrackapp.cn',
            api_key='N2QwNWQ2NTEtOWQxNS00Mjc0LWJmMmMtODA5MWJjNzE1MTZkOjpkMDJmNjRiYy00Y2UxLTQwZDctOGI3ZS0xNmMyNGU5N2Q3ZGM',
            api_user='administrator'
        )

    def getProjects(self):
        project_query = self.session.query("select children.name, children.id, name, id from Project")
        self.project_entities = {}
        for project in project_query:
            self.project_entities[project['name']] = BrProject(self.session, project)

        return self.project_entities

    def getUsers(self):
        user_query = self.session.query(
            "select username from User"
        )
        self.user_entities = {}

        for user in user_query:
            self.user_entities[user['username']] = BrUser(self.session, user, self)

        return self.user_entities

    def delete(self):
        print('[Error] Root can not be deleted')
        raise PermissionError

class BrUser():
    def __init__(self, ftrack_session, ftrack_user_entity, parent):
        self.session = ftrack_session
        self.entity = ftrack_user_entity
        self.name = ftrack_user_entity['username']
        self.id = ftrack_user_entity['id']
        self.parent = parent
        
class BrProject(FTBridge):
    def __init__(self, ftrack_session, ftrack_project_entity):
        super(BrProject, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_project_entity
        self.name = ftrack_project_entity['name']
        self.id = ftrack_project_entity['id']
        #self.scenes = self.getScenes()
        #self.assetTypes = self.getAssetTypes()
        #self.tasks = self.getTasks()
        #self.notes = self.getNotes()
        
    def getConfig(self):
        pass

    def getTaskTemplates(self):
        task_templates = self.entity['project_schema']['task_templates']

        self.task_template_entities = {}

        for task_template in task_templates:
            self.task_template_entities[task_template['name']] = task_template

        return self.task_template_entities

    def getAssetTypes(self):
        # asset_type_query = self.session.query(
        #     "select name, id from Type where color is '#f39c12'"
        #     #"select name, id from Type where color is '#333333'"
        # )
        asset_type_query = self.session.query(
            "select name, id from Folder where parent.name is '01_Asset' and project.id is {0}".format(
                 self.id
            )
        )
        self.asset_type_entities = {}
        for asset_type in asset_type_query:
            self.asset_type_entities[asset_type['name']] = BrAssetType(self.session, asset_type, self)

        return self.asset_type_entities

    def getScenes(self):
        scene_query = self.session.query(
            "select name, id from Scene where project.id is {0}".format(self.id)
        )
        self.scene_entities = {}
        for scene in scene_query:
            self.scene_entities[scene['name']] = BrScene(self.session, scene, self)

        return self.scene_entities

    def getLinks(self):
        pass

    def delete(self):
        print('[Error] Project can not be deleted')
        raise PermissionError

    def addScene(self, scene_name):
        task_template = self.getTaskTemplates()['Scene']
        parent = self.session.query(
            "Folder where name is '02_Shot' and project.id is {0}".format(self.id)
        ).first()

        scene = self.session.create(
            "Scene", {
                'name': scene_name,
                'parent': parent,
            }
        )

        for task_type in [t['task_type'] for t in task_template['items']]:
            self.session.create(
                'Task', {
                    'name': task_type['name'],
                    'type': task_type,
                    'parent': scene
                }
            )

        try:
            self.session.commit()
            return BrScene(self.session, scene, self)

        except:
            return None

class BrAssetType(FTBridge):
    def __init__(self, ftrack_session, ftrack_type_entity, parent):
        super(BrAssetType, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_type_entity
        self.name = ftrack_type_entity['name']
        self.id = ftrack_type_entity['id']
        self.parent = parent
        #self.AssetBuilds = self.getAssetBuilds()

    def getAssetBuilds(self):
        # assetbuild_query = self.session.query(
        #     "select name, id from AssetBuild where type.id is {0} and project.id is {1}".format(
        #         self.id, self.parent.id
        #     )
        # )
        assetbuild_query = self.session.query(
            "select name, id from AssetBuild where parent.id is {0}".format(
                self.id
            )
        )
        self.assetbuild_entities = {}
        for assetbuild in assetbuild_query:
            self.assetbuild_entities[assetbuild['name']] = BrAssetBuild(self.session, assetbuild, self)

        return self.assetbuild_entities

    def addAssetBuild(self, assetbuild_name):
        asset_type = self.mapping(self.name)['full']
        ftrack_type = self.getTypes()[asset_type]
        task_template = self.parent.getTaskTemplates()['Asset']
        assetbuild = self.session.create(
            "AssetBuild", {
                'name': assetbuild_name,
                'parent': self.entity,
                'type': ftrack_type,
            }
        )

        for task_type in [t['task_type'] for t in task_template['items']]:
            self.session.create(
                'Task', {
                    'name': task_type['name'],
                    'type': task_type,
                    'parent': assetbuild
                }
            )

        try:
            self.session.commit()
            return BrAssetBuild(self.session, assetbuild, self)

        except:
            return None

class BrAssetBuild(FTBridge):
    def __init__(self, ftrack_session, ftrack_asset_entity, parent):
        super(BrAssetBuild, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_asset_entity
        self.name = ftrack_asset_entity['name']
        self.id = ftrack_asset_entity['id']
        self.parent = parent
        #self.tasks = self.getTasks()
        #self.links = self.getLinks()

    def getIncomingLinks(self):
        incoming_links = self.entity['incoming_links']

        self.incoming_links = {}

        if len(self.incoming_links.keys) > 0:
            for incoming_link in incoming_links:
                self.incoming_links[incoming_link['from']['name']] = incoming_link

        return incoming_links

    def getOutgoingLinks(self):
        outgoing_links = self.entity['outgoing_links']

        self.outgoing_links = {}

        if len(self.outgoing_links.keys) > 0:
            for outgoing_link in outgoing_links:
                self.outgoing_links[outgoing_link['from']['name']] = outgoing_link

        return outgoing_links

class BrScene(FTBridge):
    def __init__(self, ftrack_session, ftrack_scene_entity, parent):
        super(BrScene, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_scene_entity
        self.name = ftrack_scene_entity['name']
        self.id = ftrack_scene_entity['id']
        self.parent = parent
        #self.shots = self.getShots()
        #self.tasks = self.getTasks()

    def getShots(self):
        shot_query = self.session.query(
            "select name, id from Shot where parent.id is {0}".format(
                self.id
            )
        )
        self.shot_entities = {}

        for shot in shot_query:
            self.shot_entities[shot['name']] = BrShot(self.session, shot, self)

        return self.shot_entities

    def addShot(self, shot_name):
        task_template = self.parent.getTaskTemplates()['Shot']
        shot = self.session.create(
            "Shot", {
                'name': shot_name,
                'parent': self.entity,
            }
        )

        for task_type in [t['task_type'] for t in task_template['items']]:
            self.session.create(
                'Task', {
                    'name': task_type['name'],
                    'type': task_type,
                    'parent': shot
                }
            )

        try:
            self.session.commit()
            return BrShot(self.session, shot, self)

        except:
            return None

class BrShot(FTBridge):
    def __init__(self, ftrack_session, ftrack_shot_entity, parent):
        super(BrShot, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_shot_entity
        self.name = ftrack_shot_entity['name']
        self.id = ftrack_shot_entity['id']
        self.parent = parent
        #self.tasks = self.getTasks()
        #self.links = self.getLinks()

class BrTask(FTBridge):
    def __init__(self, ftrack_session, ftrack_task_entity, parent):
        super(BrTask, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_task_entity
        self.name = ftrack_task_entity['name']
        self.id = ftrack_task_entity['id']
        self.parent = parent

    def addAsset(self, asset_type="Upload"):
        asset_type = self.session.query('AssetType where name is {0}'.format(asset_type)).one()
        asset = self.session.create(
            "Asset", {
                'name': self.name,
                'type': asset_type,
                'parent': self.parent.entity,
            }
        )
        self.session.commit()
        return BrAsset(self.session, asset, self.parent)

    def addVersion(self, version=None):
        asset_name = self.name
        if asset_name not in self.getAssets().keys():
            self.addAsset()

        asset = self.getAssets()[asset_name].entity

        if version:
            asset_version = self.session.create('AssetVersion', {
                    'asset': asset,
                    'task': self.entity,
                    'version': version,
                    }
                )

        else:
            asset_version = self.session.create('AssetVersion', {
                    'asset': asset,
                    'task': self.entity,
                    }
                )

        self.session.commit()
        return BrVersion(self.session, asset_version, self)

class BrAsset(FTBridge):
    def __init__(self, ftrack_session, ftrack_asset_entity, parent):
        super(BrAsset, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_asset_entity
        self.name = ftrack_asset_entity['name']
        self.id = ftrack_asset_entity['id']
        self.parent = parent

    def getVersions(self):
        # version_query = self.session.query(
        #     "select name, id from AssetVersion where parent.id is {0}".format(
        #         self.parent.id
        #     )
        # )

        asset_versions = self.entity['versions']

        self.asset_version_entities = {}

        if len(asset_versions) > 0:
            for asset_version in asset_versions:
                str_version = self.toStrVersion(asset_version['version'])
                self.asset_version_entities[str_version] = BrVersion(self.session, asset_version, self)

        return self.asset_version_entities

    def toStrVersion(self, int_version):
        '''Convert int-formatted version to str-formatted version with provided *intversion*.'''
        if int_version < 10:
            return 'v00' + str(int_version)
        if int_version < 100:
            return 'v0' + str(int_version)
        if int_version < 1000:
            return 'v' + str(int_version)
        else:
            return 'v000'

class BrVersion():
    def __init__(self, ftrack_session, ftrack_version_entity, parent):
        super(BrVersion, self).__init__()
        self.session = ftrack_session
        self.entity = ftrack_version_entity
        self.name = self.toStrVersion(ftrack_version_entity['version'])
        self.id = ftrack_version_entity['id']
        self.parent = parent

    def toStrVersion(self, int_version):
        '''Convert int-formatted version to str-formatted version with provided *intversion*.'''
        if int_version < 10:
            return 'v00' + str(int_version)
        if int_version < 100:
            return 'v0' + str(int_version)
        if int_version < 1000:
            return 'v' + str(int_version)
        else:
            return 'v000'

    def addMediaComponent(self, media_file_path):
        self.entity.encode_media(media_file_path)

    def addMediaComponents(self, media_file_path_list):
        for media_file_path in media_file_path_list:
            self.entity.encode_media(media_file_path)

    def delete(self):
        self.session.delete(self.entity)
        self.session.commit()