import FTShortcut as fts

# versions = fts.getVersions('lfc', 'shot', 'c10', 'c10010', 'Blocking')

#shot = fts.deleteShot('lfc', 'c10', 'c10010')
# task = fts.deleteTask('lfc', 'shot', 'c10', 'c10020', 'Layout')

# asset_list = {
#     'chr': ['john_west', 'brent', 'dr_strange', 'donald_trump', 'joe_biden', 'son_of_joe_biden'],
#     'prop': ['knife', 'toolbox', 'architectural_micro_devices', 'intel_core_i9', 'nvidia_geforce_rtx3090'],
#     'env': ['united_states', 'central_business_district', 'canton_tower', 'foshan_chancheng_district'],
#     'efx': ['nuclear_explode', 'earthquake', 'armstrong_cyclotron_armstrong_cannon_launch'],
# }

# for asset_type, asset_list in asset_list.items():
#     for asset_name in asset_list:
#         fts.addAssetBuild('lfc', asset_type, asset_name)
#         print(asset_name + ' added')


fts.addVersion('lfc', 'shot', 'b10', 'b10_010', ['D:/Users/Lensun/Downloads/Blocking.mp4'], 'Blocking')

# shot_list = {
#     'c10': ['c10010', 'c10020', 'c10030'],
#     'c15': ['c15010', 'c15020', 'c15030', 'c15040', 'c15050'],
#     'd10': ['d10010', 'd10020', 'd10030', 'd10040'],
#     'd15': ['d15010', 'd15020', 'd15030'],
# }

# for scene_name, shot_list in shot_list.items():
#     fts.addScene('lfc', scene_name)
#     for shot_name in shot_list:
#         fts.addShot('lfc', scene_name, shot_name)
#         print(shot_name + ' added')