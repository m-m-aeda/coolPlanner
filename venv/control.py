import requests as rq
import urllib.request as ureq
import tkinter as tk
import entity as en
import json

class Schedule:
    def __init__(self,candidate_dests=None):
        """
        candidate_dests : DestinationList
        """
        self.candidate_dests=candidate_dests
        self.plans=[]
        self.map_api=GoogleMapAPI()
        # self.yolp_api=YahooAPI()
        pass

    def init_plan(self,dep="",arr=""):
        """
        Planの初期化を行う
        depとarrが問題なければそのPlanを返す
        """
        (dep_name,dep_lat,dep_lng)=self.map_api.get_location_info(dep)
        dep_dest=en.Destination(dep_name,dep_lat,dep_lng)
        (arr_name,arr_lat,arr_lng)=self.map_api.get_location_info(arr)
        arr_dest=en.Destination(arr_name,arr_lat,arr_lng)
        plan=en.Plan(dep_dest,arr_dest)
        self.plans.append(plan)
        return plan

    def add_candidate(self, dest_name=""):
        """
        候補地に追加する
        dest_name : 候補地の名前の文字列
        """
        (name,lat,lng)=self.map_api.get_location_info(dest_name)
        self.candidate_dests.add(en.Destination(name,lat,lng))

    def get_candidate_names(self):
        """
        candidate_destsの文字列のタプルを返す
        return : 文字列のタプル
        """
        return self.candidate_dests.get_names()
    
    def add_primary(self,tab_index=-1,dest_name=""):
        """
        主要目的地に追加して、候補地から消す
        tab_index : タブのindex
        dest_name : 選択された目的地の名前の文字列
        """
        plan=self.plans[tab_index]
        dest=self.candidate_dests.get_dest_by_name(dest_name=dest_name)
        print("dest = ")
        plan.add_dest(dest)

    def del_primary(self,tab_index=-1,dest_index=-1):
        """
        主要目的地から削除して、候補地に追加する
        tab_index : タブのindex
        dest_index : 選択された目的地のindex
        """
        plan=self.plans[tab_index]
        dest=plan.pop_dest(dest_index)
        dest=self.candidate_dests.add(dest)

    def update_candidates(self):
        """
        候補地のリストフレームを更新します。
        """
        self.candidate_dests.update_frame()

    def has_plan(self):
        """
        日程が1つでも作られているかを返します。
        return : planが1つでもあればtrue
        """
        return len(self.plans) != 0

    def get_optimized_plans(self):
        """
        最適化したPlanのリストを返します。
        return : entity.Planのリスト
        """
        for plan in self.plans:
            names=list(plan.get_dest_names())
            (dep,arr)=plan.get_dep_and_arr_name()
            optimized_names=self.map_api.get_optimized_route(origin=dep,destination=arr,names=names)
            plan.sort_by(optimized_names)
        return self.plans

    # def get_optimized_images(self):
    #     """
    #     最適化したPlanの画像のリストを返します。
    #     return : entity.Planの画像リスト
    #     """
    #     images=[]
    #     for plan in self.plans:
    #         geos=list(plan.get_dest_geos())
    #         (dep,arr)=plan.get_dep_and_arr_geo()
    #         optimized_image=self.yolp_api.get_optimized_route_image(*dep,*arr,geos)
    #         images.append(optimized_image)
    #     return images


class GoogleMapAPI:
    def __init__(self):
        pass

    def get_location_info(self,target_name=""):
        """
        target_nameの名前、位置情報を取得します。
        target_name : 地名の文字列
        return (正式名称の文字列, 緯度, 経度)
        """
        if target_name is "":
            raise ValueError(target_name +" is empty.")

        goo_api_key=self.get_google_api_key()
        
        url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='+target_name+'&inputtype=textquery&fields=name,geometry&key=' + goo_api_key
        res = rq.get(url)

        if res.status_code != 200:
            raise ValueError("response code = " + res.status_code + ", name = " + target_name)

        # json例(candidates[0]) :
        #           {'geometry':
        #               {'location':
        #                   {'lat': 35.675888,
        #                   'lng': 139.744858}, 
        #               'viewport': 
        #                   {'northeast':
        #                       {'lat': 35.67723782989273,
        #                       'lng': 139.7462078298927},
        #                   'southwest': 
        #                       {'lat': 35.67453817010728,
        #                       'lng': 139.7435081701073}}},
        #           'name': 'National Diet Building'}
        jdic = res.json()
        # candidatesはリストを返す
        candidate=jdic["candidates"][0]
        location=candidate["geometry"]["location"]
        lat=location["lat"]
        lng=location["lng"]
        return (str(candidate["name"]),float(lat),float(lng))

    def get_optimized_route(self,origin="",destination="",names=None):
        """
        正式名称の名前のリストから最適な道順のlistを返します。
        names : 正式名称のリスト
        return : 最適化した正式名称のリスト
        """
        if names is None:
            raise ValueError("names is None.")

        goo_api_key=self.get_google_api_key()

        url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + origin + '&destination=' + destination + "&waypoints=optimize:true"
        for name in names:
            url = url + "|" + name
        url = url + '&mode=transit&key=' + goo_api_key
        response = rq.get(url)
        # print(response)
        # print("status code = " + str(response.status_code))
        # print("headers = " + str(response.headers))
        # print("encoding = " + response.encoding)
        # print("body = " + response.text)
        return []

    def get_google_api_key(self):
        goo_api_key=""
        with open("venv/app_settings.json") as f:
            settings=json.load(f)
            goo_api_key=settings["goo_api_key"]
        return goo_api_key


# class YahooAPI:
#     def __init__(self):
#         pass

#     def get_optimized_route_image(self,ori_lat=0.0,ori_lng=0.0,dest_lat=0.0,dest_lng=0.0,geos=None):
#         """
#         正式名称の名前のリストから最適な道順の画像を返します。
#         geos : 位置のタプルのリスト
#         return : 最適化した画像
#         """
#         if geos is None:
#             raise ValueError("names is None.")
#         url = "https://map.yahooapis.jp/course/V1/routeMap?appid=&route="
#         # 出発地
#         url = url + str(ori_lat) + "," + str(ori_lng) + ","
#         for (lat,lng) in geos:
#             # 経由地
#             url = url + str(lat) + "," + str(lng) + ","
#         # 到着地
#         url = url + str(dest_lat) + "," + str(dest_lng)
#         for (lat,lng) in geos:
#             # 経由地のpin
#             url = url + "&pin=" + str(lat) + "," + str(lng)
#         ureq.urlretrieve(url, "test.jpg")
#         return []