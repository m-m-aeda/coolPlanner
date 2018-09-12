import tkinter as tk
import utils as u
import os

class TabFrame(tk.Frame):
    """
    それぞれの日程の画面
    """
    def __init__(self,master=None,plan=None,candidates=None,add_han=None,del_han=None):
        """
        candidates : 候補地の名前の文字列のタプル
        """
        super().__init__(master=master)
        # widgetの配置
        (dep,arr) = plan.get_dep_and_arr_name()
        tk.Label(self,text="出発地").place(x=10,y=10)
        tk.Label(self,text=dep).place(width=200,x=70,y=10)
        tk.Label(self,text="到着地").place(x=10,y=50)
        tk.Label(self,text=arr).place(width=200,x=70,y=50)
        tk.Label(self,text="主要行先").place(x=10,y=90)
        self.list = u.ComboListFrame(self,height=10,add_han=add_han,del_han=del_han)
        self.list.set_values(candidates)
        self.list.place(x=30,y=120,width=300)
    
    def update_values(self,candidates=None):
        self.list.set_values(candidates)

    def get_list_view(self):
        return self.list.get_list_view()

class RouteTabFrame(tk.Frame):
    """
    それぞれの日程の結果を表示するタブ
    """
    def __init__(self,master=None,plan=None,image=None):
        super().__init__(master=master)
        tabs=u.TabManager(self)
        tabs.place(x=0,y=0,width=340,height=450)
        if plan is not None:
            road_frame = RoadTabFrame(master=tabs,plan=plan)
            road_frame.place(x=0,y=0)
            tabs.add(road_frame,text=" 道 ")
        img_frame = ImageTabFrame(master=tabs,plan=plan)
        img_frame.place(width=30,height=440)
        tabs.add(img_frame,text=" 図 ")

class RoadTabFrame(tk.Frame):
    """
    それぞれの日程の道順を表示するタブ
    """
    def __init__(self,master=None,plan=None):
        super().__init__(master=master)
        (dep,arr) = plan.get_dep_and_arr_name()
        #img_path = os.path.dirname(os.path.abspath(__file__)) + "\\under_arrow.GIF"
        #arrow = tk.PhotoImage(file = img_path)
        # 出発地
        tk.Label(self,text=dep).place(x=10,y=10)
        tk.Label(self,text="↓").place(x=40,y=35)
        count=0
        shifted_height=0
        for dest_name in plan.get_dest_names():
            # 目的地
            tk.Label(self,text=dest_name).place(x=10,y=(60+shifted_height))
            tk.Label(self,text="↓").place(x=40,y=(85+shifted_height))
            count=count+1
            shifted_height=50*count
        # 到着地
        tk.Label(self,text=arr).place(x=10,y=(60+shifted_height))

class ImageTabFrame(tk.Frame):
    """
    それぞれの日程の図を表示するタブ
    """
    def __init__(self,master=None,plan=None):
        super().__init__(master=master)
        # 図
        tk.Label(self,text="図").place(x=10,y=10,width=310,height=410)