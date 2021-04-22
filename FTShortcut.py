# coding=utf-8
# author:   Lensun
# contact:  lensun@nstation.net
# date:     2021/04/19
# version:  1.1.1

import json
import FTBridge

def getRoot():
    '''Return a BrRoot instance.'''
    root = FTBridge.BrRoot()
    
    return root

def getMapping():
    '''Return a dict of unpacked mapping json.'''
    with open("./mapping.json",'r') as json_file:
        return json.load(json_file)

def getProjects():
    '''Return a dict of BrProject.'''
    root = FTBridge.BrRoot()
    projects = root.getProjects()

    return projects

def getProject(project_name):
    '''Return *project_name* if *project_name* exists, otherwise return None.
    
    *project_name* is in string type.
    
    '''
    project = getProjects().get(project_name)

    if project:
        return project_name
    else:
        return None

def getCategories(project_name, context_name):
    '''Return a dict of BrCategory(BrAssetType or BrScene) of given *context_name* under project named *project_name*.
    
    *project_name* and *context_name* are in string type. 
    *context_name* should be either 'asset' or 'shot'.
    
    '''
    context_selection = {
        'asset': getAssetTypes,
        'shot': getScenes,
    }

    context_func = context_selection.get(context_name)

    if context_func:
        return context_func(project_name)
    else:
        print('[Error] ' + context_name + ' not found')

def getCategory(project_name, context_name, category_name):
    '''Return *category_name* if *category_name* exists, otherwise return None.
    
    *project_name*, *context_name* and *category_name* are in string type.
    *context_name* should be either 'asset' or 'shot'.
    
    '''
    context_selection = {
        'asset': getAssetType,
        'shot': getScene,
    }

    context_func = context_selection.get(context_name)

    if context_func:
        return context_func(project_name, category_name)
    else:
        print('[Error] ' + context_name + ' not found')

def getObjects(project_name, context_name, category_name):
    '''Return a dict of BrObject(BrAssetBuild of BrShot) under the category named *category_name*.
    
    *project_name*, *context_name* and *category_name* are in string type. 
    *context_name* should be either 'asset' or 'shot'.
    
    '''
    context_selection = {
        'asset': getAssetBuilds,
        'shot': getShots,
    }

    context_func = context_selection.get(context_name)

    if context_func:
        return context_func(project_name, category_name)
    else:
        print('[Error] ' + context_name + ' not found')

def getObject(project_name, context_name, category_name, object_name):
    '''Return *object_name* if *object_name* under the category named *category_name* exists, otherwise return None.
    
    *project_name*, *context_name*, *category_name* and *object_name* are in string type.
    *context_name* should be either 'asset' or 'shot'.
    
    '''
    context_selection = {
        'asset': getAssetBuild,
        'shot': getShot,
    }

    context_func = context_selection.get(context_name)

    if context_func:
        return context_func(project_name, category_name, object_name)
    else:
        print('[Error] ' + context_name + ' not found')

def addVersion(project_name, context_name, category_name, object_name, media_file_path_list, task_name=None, version=None):
    '''Create a new version under the task named *task_name*.
    
    *project_name*, *context_name*, *category_name*, *object_name* and *task_name* are in string type.
    *media_file_path_list* is in list type.
    *version* is optional, in int type. By default, new version is added by 1.
    
    Return True if operation was successful, otherwise return False.

    '''
    if task_name:
        task = getTasks(project_name, context_name, category_name, object_name).get(task_name)
        if task:
            asset_version = task.addVersion(version)
            if media_file_path_list:
                asset_version.addMediaComponents(media_file_path_list)
                return True
            else:
                print('[Error] kwarg *media_file_path_list*' + 'is empty')
        else:
            print('[Error] ' + task_name + ' not found')
            return False

def deleteVersion(project_name, context_name, category_name, object_name, version, task_name=None):
    '''Delete a specified *version* under the task named *task_name*.
    
    *project_name*, *context_name*, *category_name*, *object_name* and *task_name* are in string type.
    *version* is in int type.

    Return True if operation was successful, otherwise return False.
    
    '''
    asset_versions = getVersions(project_name, context_name, category_name, object_name, task_name)
    asset_version = asset_versions.get(toStrVersion(version))
    try:
        asset_version.delete()
        return True
    except:
        print('[Error] Failed to delete version')
        return False

def getVersions(project_name, context_name, category_name, object_name, task_name=None):
    '''Return a dict of BrVersion under the task named *task_name*.
    
    *project_name*, *context_name*, *category_name*, *object_name* and *task_name* are in string type. 
    
    '''
    if task_name:
        task = getTasks(project_name, context_name, category_name, object_name)[task_name]
        asset = task.getAssets().get(task_name)
        if asset:
            versions = asset.getVersions()
        else:
            # print('[Error] No versions found in task ' + task_name)
            return {}

    elif object_name:
        pass

    else:
        pass

    return versions

def toStrVersion(int_version):
    '''Convert int-formatted version to str-formatted version with provided *intversion*.'''
    if int_version < 10:
        return 'v00' + str(int_version)
    if int_version < 100:
        return 'v0' + str(int_version)
    if int_version < 1000:
        return 'v' + str(int_version)
    else:
        return 'v000'

def getTasks(project_name, context_name, category_name, object_name=None):
    '''Return a dict of BrTask under the category named *category_name*. 
    
    *object_name* is optional. When provided, return a dict of BrTask under *object_name* instead.
    *project_name*, *context_name*, *category_name* and *object_name* are in string type. 
    
    '''
    if object_name:
        tasks = getObjects(project_name, context_name, category_name)[object_name].getTasks()
        
    else:
        tasks = getCategories(project_name, context_name)[category_name].getTasks()

    return tasks

def addTask(project_name, context_name, category_name, object_name=None, task_name="default"):
    '''Create a new task named *task_name* under the category named *category_name*.

    *object_name* is optional. When provided, create the task under the object named *object_name* instead.
    *project_name*, *context_name*, *category_name*, *object_name* and *task_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    if object_name:
        _object = getObjects(project_name, context_name, category_name)[object_name]
        
    else:
        _object = getCategories(project_name, context_name)[category_name]

    _object.addTask(task_name)

    try:
        _object.session.commit()
        return True

    except:
        return False

def deleteTask(project_name, context_name, category_name, task_name, object_name=None):
    '''Delete a task under the category named *category_name*.

    *object_name* is optional. When provided, Delete the task under the category named *object_name* instead.
    *project_name*, *context_name*, *category_name*, *object_name* and *task_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    task = getTasks(project_name, context_name, category_name, object_name).get(task_name)

    if task:
        try:
            task.delete()
            return True
        except:
            return False

    else:
        print('[Error] ' + task_name + ' not found')
        return False

def getScenes(project_name):
    '''Return a dict of BrScene under the project named *project_name*.
    
    *project_name* is in string type. 
    
    '''
    project = getProjects().get(project_name)

    if project:
        scenes = project.getScenes()
        return scenes
    else:
        print('[Error] ' + project_name + ' not found')

def getScene(project_name, scene_name):
    '''Return *scene_name* if the scene named *scene_name* under the project named *project_name* exists, 
    otherwise return None.
    
    *project_name* and *scene_name* are in string type.
    
    '''
    scene = getScenes(project_name).get(scene_name)

    if scene:
        return scene_name
    else:
        print('[Error] ' + scene_name + ' not found')
        return None

def addScene(project_name, scene_name):
    '''Create a new scene named *scene_name* under the project named *project_name*.

    *project_name* and *scene_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    project = getProjects().get(project_name)

    if project:
        scene = project.addScene(scene_name)
        if scene:
            return True
        else:
            print('[Error] Failed to add ' + scene_name + '. Please check if scene already exists.')
    else:
        print('[Error] ' + project_name + ' not found')
        return False

def deleteScene(project_name, scene_name):
    '''Delete a scene named *scene_name* under the project named *project_name*.

    *project_name* and *scene_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    scene = getScenes(project_name).get(scene_name)

    if scene:
        try:
            scene.delete()
            return True
        except:
            return False
    else:
        print('[Error] ' + scene_name + ' not found')
        return False

def getShots(project_name, scene_name):
    '''Return a dict of BrShot under the scene named *scene_name*.
    
    *project_name* is in string type. 
    
    '''
    scene = getScenes(project_name).get(scene_name)

    if scene:
        shots = scene.getShots()
        return shots
    else:
        print('[Error] ' + scene_name + ' not found')

def getShot(project_name, scene_name, shot_name):
    '''Return *shot_name* if the scene named *shot_name* under the scene named *scene_name* exists, 
    otherwise return None.
    
    *project_name*, *scene_name* and *shot_name* are in string type.
    
    '''
    shot = getShots(project_name, scene_name).get(shot_name)

    if shot:
        return shot_name
    else:
        return None

def addShot(project_name, scene_name, shot_name):
    '''Create a new shot named *shot_name* under the scene named *scene_name*.

    *project_name*, *scene_name* and *shot_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    scene = getScenes(project_name).get(scene_name)

    if scene:
        shot = scene.addShot(shot_name)
        if shot:
            return True
        else:
            print('[Error] Failed to add ' + shot_name + '. Please check if shot already exists.')
    else:
        print('[Error] ' + scene_name + ' not found')
        return False

def deleteShot(project_name, scene_name, shot_name):
    '''Delete a shot named *shot_name* under the scene named *scene_name*.

    *project_name*, *scene_name* and *shot_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    shot = getShots(project_name, scene_name).get(shot_name)

    if shot:
        try:
            shot.delete()
            return True
        except:
            return False

    else:
        print('[Error] ' + shot_name + ' not found')
        return False

def getAssetTypes(project_name):
    '''Return a dict of BrAssetType under the project named *project_name*.
    
    *project_name* is in string type. 
    
    '''
    project = getProjects().get(project_name)
    if project:
        asset_types = project.getAssetTypes()
        return asset_types
    else:
        print('[Error] ' + project_name + ' not found')

def getAssetType(project_name, asset_type_name):
    '''Return *asset_type_name* if *asset_type_name* under the project named *project_name* exists, otherwise return None.
    
    *project_name* is in string type.
    
    '''
    asset_type = getAssetTypes(project_name).get(asset_type_name)

    if asset_type:
        return asset_type
    else:
        print('[Error] ' + asset_type_name + ' not found')
        return None

def getAssetBuilds(project_name, asset_type_name):
    '''Return a dict of BrAssetBuild under the asset_type named *asset_type_name*.
    
    *project_name* and *asset_type_name* are in string type. 
    
    '''
    asset_type = getAssetTypes(project_name).get(asset_type_name)

    if asset_type:
        assets = asset_type.getAssetBuilds()
        return assets
    else:
        print('[Error] ' + asset_type_name + ' not found')

def getAssetBuild(project_name, asset_type_name, assetbuild_name):
    '''Return *assetbuild_name* if *assetbuild_name* under the asset type named *asset_type_name* exists, otherwise return None.
    
    *project_name* and *asset_type_name* and *assetbuild_name* are in string type. 
    
    '''
    asset = getAssetBuilds(project_name, asset_type_name).get(assetbuild_name)

    if asset:
        return assetbuild_name
    else:
        print('[Error] ' + assetbuild_name + ' not found')
        return None

def addAssetBuild(project_name, asset_type_name, assetbuild_name):
    '''Create a new assetbuild named *assetbuild_name* under the asset type named *asset_type_name*.

    *project_name*, *asset_type_name* and *assetbuild_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    asset_type = getAssetTypes(project_name).get(asset_type_name)

    if asset_type:
        try:
            asset_type.addAssetBuild(assetbuild_name)
            return True
        except:
            print('[Error] Failed to add ' + assetbuild_name + '. Please check if asset already exists.')
            return False

    else:
        print('[Error] ' + asset_type_name + ' not found')
        return False

def deleteAssetBuild(project_name, asset_type_name, assetbuild_name):
    '''Delete a assetbuild named *assetbuild_name* under the asset type named *asset_type_name*.

    *project_name*, *asset_type_name* and *assetbuild_name* are in string type.
    
    Return True if operation was successful, otherwise return False.

    '''
    asset = getAssetBuilds(project_name, asset_type_name).get(assetbuild_name)

    if asset:
        try:
            asset.delete()
            return True
        except:
            return False

    else:
        print('[Error] ' + assetbuild_name + ' not found')
        return False

def getUsers():
    '''Return a dict of BrUser.'''
    root = getRoot()
    users = root.getUsers()

    return users

def getUser(user_name):
    '''Return user name if *user_name* exists, otherwise return None.
    
    *user_name* is in string type. 
    
    '''
    user = getUsers().get(user_name)

    if user:
        return user_name
    else:
        return None



if __name__ == '__main__':

    # print(getProjects())
    # print(getScenes('WS'))
    # print(getShots('WS', 'b10'))
    # print(getAssetTypes('WS'))
    # print(getAssetBuilds('WS', 'Prop'))

    #asset = getAssetBuilds('WS', 'Prop')['wst']
    #print(asset.getTasks())
    #print(asset.parent)
    #print(asset.id)

    #print(getUsers())
    # print(getAssetTypes('lfc'))
    # print(getObjects('lfc', 'asset', 'chr'))
    # print(getObjects('lfc', 'shot', 'b10'))
    # print(getObject('lfc', 'shot', 'b10', 'b10010'))
    # print(getObjects('lfc', 'shot', 'b10')['b10010'].getTasks())
    # print(getTasks('lfc', 'shot', 'b10', 'b10010'))
    # print(getTasks('lfc', 'shot', 'b10'))

    # print(getTasks('lfc', 'asset', 'chr', 'example_a'))
    # print(getTasks('lfc', 'asset', 'chr'))
    # print(list(getAssetTypes('lfc')['chr'].getAssetBuilds()['example_a'].entity.keys()))

    # print(getAssetTypes('lfc')['chr'].getAssetBuilds()['example_a'].getIncomingLinks())

    root = FTBridge.BrRoot()

    project = root.getProjects()['lfc']

    # scene = project.addScene('c10')

    # for i in range(10, 100, 10):
    #     shot = 'c100'
    #     shot_name = shot + str(i)
    #     print(shot_name)

    #     shot = scene.addShot(shot_name)

    # types = project.getTypes()

    #print(types)

    # task_templates = project.getTaskTemplates()['Asset']['items']

    # print(task_templates)

    # asset_type = project.getAssetTypes()['chr']

    # asset_type.addAssetBuild('ccd')

    # scene = project.getScenes()['b10']

    # scene.addShot('b10020')

    # assetbuild = asset_type.getAssetBuilds()['example_a']

    # task = assetbuild.getTasks()['Design']

    # asset = task.getAssets()

    # print(asset)

    #task = getTasks('lfc', 'shot', 'c10', 'c10010')['Blocking']

    versions = getVersions('lfc', 'shot', 'c10', 'c10010', 'Blocking')

    print(versions)

    # asset = task.getAssets()['example_a']

    # versions = asset.getVersions()

    # print(versions['v001'].name)

    # print(list(versions['v001'].keys()))