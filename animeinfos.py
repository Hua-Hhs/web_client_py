import os
import json

anime_root_path = 'E:\\web\\anime\\'

anime_root_path = 'F:\\web\\anime\\'
class anime:
    def __init__(self,title,episode_num,episode_list) -> None:
        self.title = title
        self.episode_num = episode_num
        self.episode_list = episode_list
        
        pass
class animeinfolist:
    def __init__(self):
        self.anime_root_path = anime_root_path
    # 获取动画根路径下所有文件夹，就是所有动画
    def get_all_anime_folder(self):
        anime_folders = [f for f in os.listdir(anime_root_path) if os.path.isdir(os.path.join(anime_root_path, f))]
        return anime_folders
    # 获取所有动画信息
    def get_all_anime_infos(self):
        folders = self.get_all_anime_folder()
        animeinfo = []
        for folder in folders:
            animeinfo.append(list.get_anime_info(folder))
        return animeinfo
    
    # 根据相对路径获取动画信息
    def get_anime_info(self,folder):
        anime_folder = os.path.join(self.anime_root_path,folder)
        info_json = os.path.join(anime_folder,'info.json')
        with open(info_json, 'r') as f:
            json_file = json.load(f)
            return json_file
        
    def get_all_anime_title(self):
        titles =  [info['title'] for info in self.get_all_anime_infos()]
        return titles
    def get_all_anime_cover_name(self):
        covers =  [info['cover'] for info in self.get_all_anime_infos()]
        return covers
    
    def get_anime_episode_titles(title):
        info_json = 'config\\魔圆.json'
        with open(info_json, 'r') as f:
            json_file = json.load(f)
            return json_file
        return['1','2','3','4']
    # def get_anime_info():
       
    
def test():
    li = [{"anime_title": "魔圆", "cover": "F:\\\\web\\anime\\魔圆\\cover.jpg"}]
    data = {"all_info_list": li}
    all_infos_file_path = 'animeinfos\\all_infos.json'
    with open(all_infos_file_path, "w") as json_file:
            # indent=4每行缩进4
            json.dump(data, json_file, indent=4)    
    # json.dump(data, all_infos_file_path, indent=4)  

def get_cover_path_by_anime_title(title):
    
    all_infos_file_path = 'animeinfos\\all_infos.json'
    with open(all_infos_file_path, 'r') as f:
        json_file = json.load(f)
        print(json_file)
        for info in json_file['all_info_list']:
            if(info['anime_title'] == title):
                return info['cover']

def get_anime_titles():
    all_infos_file_path = 'animeinfos\\all_infos.json'
    with open(all_infos_file_path, 'r') as f:
        json_file = json.load(f)
        info_list = json_file['all_info_list']
        anime_titles = []
        for info in info_list:
             anime_titles.append(info['anime_title'])
        return anime_titles
    
        # print(info_list[0:]['anime_title'])
        # for info in info_list:
        #     anime_titles info['anime_title']
        



test()
a = get_cover_path_by_anime_title('魔圆')
a = get_anime_titles()
print(a)
# list = animeinfolist()

# print(list.get_all_anime_infos())
