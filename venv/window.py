import tkinter as tk
import utils as u
import frame as f

class EntryWindow(tk.Tk):
    """
    候補地入力画面
    """
    def __init__(self, dest=None,add_han=None,next_han=None):
        super().__init__()
        self.title("Entry")
        self.geometry('200x350+0+0')
        tk.Button(self,text="次へ",command=next_han).place(x=165,y=0)
        tk.Label(self,text="行きたいところを入力してください！").place(x=10, y=30)
        list_frame = u.ListFrame(master=self,add_han=add_han,del_han=self.__click_delete)
        list_frame.place(x=30, y=70)
        self.candidate_dest=dest
        self.candidate_dest.set_frame(list_frame.get_list_view())
        self.mainloop()

    def __click_delete(self, index):
        """
        削除ボタンが押された
        index : リストのindex
        """
        self.candidate_dest.delete(index=index)

class InitWindow(tk.Toplevel):
    """
    出発地と到着地を入力する画面
    """
    def __init__(self,exe_han=None):
        super().__init__()
        self.exe_han=exe_han
        self.title("Entry")
        self.geometry('310x170+0+0')
        tk.Label(self,text="出発地を到着地を入力してください！").place(x=10,y=5)
        tk.Label(self,text="出発地").place(x=10,y=40)
        self.departure = tk.Entry(self,width=80)
        self.departure.place(width=200,x=70,y=40)
        tk.Label(self,text="到着地").place(x=10,y=80)
        self.arrival = tk.Entry(self,width=80)
        self.arrival.place(width=200,x=70,y=80)
        tk.Button(self,text="OK",command=self.__click_execute_handler).place(x=240,y=110)
        self.mainloop()

    def __click_execute_handler(self):
        self.exe_han(self.departure.get(),self.arrival.get())
        self.destroy()

class PlanWindow(tk.Toplevel):
    """
    日程設定画面    
    """
    def __init__(
            self,
            add_han=None,
            del_han=None,
            next_han=None,
            back_han=None,
            init_exe_han=None,
            schedule=None):
        super().__init__()
        self.title("Entry")
        self.geometry('350x530+0+0')
        self.add_han=add_han
        self.del_han=del_han
        self.back_han=back_han
        self.init_exe_han=init_exe_han
        self.tabs=u.TabManager(self)
        self.tabs.place(x=5,y=60,width=340,height=420)
        tk.Button(self,text="次へ",command=next_han).place(x=315,y=0)
        tk.Button(self,text="前へ",command=self.__click_back).place(x=0,y=0)
        tk.Label(self,text="それぞれの日で行きたい場所を入力してください！").place(x=10, y=30)
        tk.Button(self,text="日程追加",command=self.__click_add_tab).place(x=150,y=490)
        if schedule.has_plan():
            # すでに日程が登録されていたらwindow更新
            self.__update(
                plans=schedule.get_plans(),
                candidates=schedule.get_candidate_names())
        self.mainloop()

    def __click_add_tab(self):
        """
        日程追加ボタンが押された
        """
        InitWindow(self.__click_init_execute)

    def __click_back(self):
        """
        戻るボタンが押された
        """
        self.back_han()
        self.destroy()
        
    def __click_add(self,dest_name=""):
        """
        主要目的地に追加するボタンが押された
        """
        tab_index=self.tabs.get_active_tab_index()
        tab=self.tabs.get_active_tab()
        self.add_han(tab=tab,tab_index=tab_index,dest_name=dest_name)

    def __click_del(self,dest_index=-1):
        """
        主要目的地から削除するボタンが押された
        """
        tab_index=self.tabs.get_active_tab_index()
        tab=self.tabs.get_active_tab()
        self.del_han(tab=tab,tab_index=tab_index,dest_index=dest_index)

    # 出発地と到着地の画面のハンドラー

    def __click_init_execute(self,dep="",arr=""):
        """
        出発地と到着地の画面でOKが押された
        """
        # 委譲する
        self.init_exe_han(dep,arr,self.tabs,self.__click_add,self.__click_del)

    def __update(self, plans=None, candidates=None):
        """
        日程が登録された状態で出発地と到着地を入力する画面のOKが押された
        plans : entity.Planのリスト
        candidates : 候補地のタプル
        """
        for plan in plans:
            tab_frame = f.TabFrame(
                master=self.tabs,
                plan=plan,
                candidates=candidates,
                add_han=self.__click_add,
                del_han=self.__click_del)
            tab_frame.place(width=300,height=300)
            plan.set_frame(tab_frame.get_list_view())
            self.tabs.add_tab(tab_frame)
            plan.update_dests_frame()

class TerminalWindow(tk.Toplevel):
    """
    日程結果画面    
    """
    def __init__(
            self,
            back_han=None,
            opt_plans=None,
            opt_images=None):
        super().__init__()
        self.title("Entry")
        self.geometry('350x530+0+0')
        self.back_han=back_han
        self.tabs=u.TabManager(self)
        self.tabs.place(x=5,y=60,width=340,height=460)
        tk.Button(self,text="前へ",command=self.__click_back).place(x=0,y=0)
        tk.Label(self,text="こんな感じでいいんじゃないですか！").place(x=10, y=30)
        if opt_plans is not None:
            self.__update(plans=opt_plans)
        self.mainloop()

    def __click_back(self):
        """
        戻るボタンが押された
        """
        # self.back_han()
        self.destroy()
    
    def __update(self, plans=None):
        """
        日程が登録された状態で出発地と到着地を入力する画面のOKが押された
        plans : entity.Planのリスト
        candidates : 候補地のタプル
        """
        for plan in plans:
            tab_frame = f.RouteTabFrame(master=self.tabs,plan=plan)
            tab_frame.place(width=300,height=300)
            self.tabs.add_tab(tab_frame)