import os
import json

anime_root_path = 'E:\\web\\anime\\'

anime_root_path = 'F:\\web\\anime\\'

all_infos_file_path = 'animeinfos\\all_infos.json'

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
            animeinfo.append(self.get_anime_info(folder))
        return animeinfo
    
    # 根据相对路径获取动画信息
    def get_anime_info(self,folder):
        anime_folder = os.path.join(self.anime_root_path,folder)
        info_json = os.path.join(anime_folder,'info.json')
        with open(info_json, 'r') as f:
            json_file = json.load(f)
            return json_file
    # ['魔圆', 'bule bird', 'Trick', 'bule bird', 'Trick', '魔圆']返回一个数组，元素是标题字符串
    def get_all_anime_title(self):
        titles =  [info['title'] for info in self.get_all_anime_infos()]
        # print('titles')
        # print(titles)
        # print('------------------==============')
        return titles
    def get_all_anime_cover_name(self):
        covers =  [info['cover'] for info in self.get_all_anime_infos()]
        return covers
    
    def get_anime_episode_titles(title):
        info_json = os.path.join('animeinfos',title + '.json')
        # info_json = 'config\\魔圆.json'
        with open(info_json, 'r') as f:
            data = json.load(f)
            episode_list = data['episode_list']
            episode_title_list = [episode['episode_title'] for episode in episode_list]
            return episode_title_list
        return['1','2','3','4']
    # def get_anime_info():
    def get_anime_titles(self):
        all_infos_file_path = os.path.join('animeinfos','all_infos.json')
        # all_infos_file_path = 'animeinfos\\all_infos.json'
        with open(all_infos_file_path, 'r') as f:
            json_file = json.load(f)
            info_list = json_file['all_info_list']
            anime_titles = []
            for info in info_list:
                anime_titles.append(info['anime_title'])
            return anime_titles
       
    
def test():
    li = [{"anime_title": "魔圆", "cover": "F:\\\\web\\anime\\魔圆\\cover.jpg"}]
    data = {"all_info_list": li}
    all_infos_file_path = 'animeinfos\\all_infos.json'
    with open(all_infos_file_path, "w") as json_file:
            # indent=4每行缩进4
            json.dump(data, json_file, indent=4)    
    # json.dump(data, all_infos_file_path, indent=4)  
            

# return cover的绝对地址
def get_cover_path_by_anime_title(title):
    
    all_infos_file_path = 'animeinfos\\all_infos.json'
    with open(all_infos_file_path, 'r') as f:
        json_file = json.load(f)
        # print(json_file)
        for info in json_file['all_info_list']:
            if(info['anime_title'] == title):
                return info['cover']
# return 一个数组，元素是标题字符串 ['魔圆', 'bule bird', 'Trick', 'bule bird', 'Trick', '魔圆']
def get_anime_titles():
    # all_infos_file_path = 'animeinfos\\all_infos.json'
    all_infos_file_path = os.path.join('animeinfos','all_infos.json')
    with open(all_infos_file_path, 'r') as f:
        json_file = json.load(f)
        info_list = json_file['all_info_list']
        anime_titles = []
        for info in info_list:
             anime_titles.append(info['anime_title'])
        return anime_titles
    
        
def get_animeinfo_by_title(title):
    file_path = os.path.join('animeinfos',title+'.json')
    # # print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # # print(data)
            return data 
        

def delete_animeinfo_by_title(title):
    file_path = os.path.join('animeinfos',title+'.json')
    all_infos_file_path = os.path.join('animeinfos','all_infos.json')
    info_list = []
    with open(all_infos_file_path, 'r') as f:
        json_file = json.load(f)
        info_list = json_file['all_info_list']
        for info in info_list:
            if title == info['anime_title']:
                 
                info_list.remove(info)
                # json.dump({'all_info_list':info_list}, f, indent=4)    
                break
    with open(all_infos_file_path, "w") as json_file:
        # indent=4每行缩进4
        # print(info_list)
        json.dump({'all_info_list':info_list}, json_file, indent=4)    
    os.remove(file_path)
def add_all_infos_item(title,cover):
    all_infos_file_path = os.path.join('animeinfos','all_infos.json')
    info_list = []
    with open(all_infos_file_path, 'r') as f:
        data = json.load(f)
        info_list = data['all_info_list']
        for info in info_list:
            if title == info['anime_title']:
                 
                info_list.remove(info)   
                return False, '该标题已存在'
    info_list.append({'anime_title':title, 'cover': cover})
    with open(all_infos_file_path, "w") as f:
        # indent=4每行缩进4
        # print(info_list)
        json.dump({'all_info_list':info_list}, f, indent=4)   
    return True, 'OK' 

def add_info_item(title,info):
    json_file_path = f"./animeinfos/{title}.json"
    with open(json_file_path, "w") as json_file:
            # indent=4每行缩进4
            json.dump(info, json_file, indent=4)    

# 添加title和cover和anime详细信息（info）到title.json详细文件
def add_animeinfo_by_title_cover(title, cover, info):
    result,msg = add_all_infos_item(title,cover)
    
    if result:
        add_info_item(title, info)
    return msg

def get_all_infos_list():
    with open('animeinfos/all_infos.json', 'r') as file:
        data = json.load(file)
    data = data['all_info_list']
    return data

        
    
def get_episode_by_title_episode_title(title, episode_title):
    print(title)
    print(episode_title)
    file_path = os.path.join('animeinfos',title+'.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        episode_list = data['episode_list']
        for episode in episode_list:
            if episode['episode_title'] == episode_title:
                return episode['episode_path_textbox']




# test()
# titles =  [info['title'] for info in get_all_anime_infos()]
# print(animeinfolist().get_all_anime_title)
a = get_anime_titles()
# a = get_cover_path_by_anime_title('魔圆')
# print('-----')
# print(a)
# list = animeinfolist()

# # print(list.get_all_anime_infos())
