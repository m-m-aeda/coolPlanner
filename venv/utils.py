import tkinter as tk
import tkinter.ttk as ttk

class ListFrame(tk.Frame):
    def __init__(self,master=None,height=10,add_han=None,del_han=None):
        super().__init__(master)
        self.list = ListView(self,height=height)
        self.dest_entry = self.create_entry()
        self.add_han=add_han
        self.del_han=del_han
        # widgetの配置
        tk.Button(self,text="追加",command=self.click_add_handler).grid(column=0,row=2,padx=10)
        tk.Button(self,text="削除",command=self.click_delete_handler).grid(column=1,row=2,padx=10)
        self.list.grid(column=0,row=0,columnspan=4,pady=10)
        self.dest_entry.grid(column=0,row=1,columnspan=4,pady=10)
    
    def create_entry(self):
        return tk.Entry(self)

    def get_list_view(self):
        return self.list

    def click_add_handler(self):    
        if self.dest_entry.get() is "":
            return
        self.add_han(self.dest_entry.get())
        self.dest_entry.delete(0,tk.END)

    def click_delete_handler(self):
        if self.list.curselection() is None:
            return
        ## TODO 削除はいまのところひとつづつ
        self.del_han(self.list.curselection()[0])

# 下のCombListFrameは以下のエラーが出るのでいまはこのクラスを使う。
# TODO リファクタリング
#     self.add_han(self.dest_entry.get())
# TypeError: 'NoneType' object is not callable
class ComboListFrame(tk.Frame):
    def __init__(self,master=None,height=10,add_han=None,del_han=None):
        super().__init__(master)
        self.list = ListView(self,height=height)
        v1=tk.StringVar()
        self.dest_entry = ttk.Combobox(self, state='readonly',textvariable=v1)
        self.add_han=add_han
        self.del_han=del_han
        # widgetの配置
        tk.Button(self,text="追加",command=self.click_add_handler).grid(column=0,row=2,padx=10)
        tk.Button(self,text="削除",command=self.click_delete_handler).grid(column=1,row=2,padx=10)
        self.list.grid(column=0,row=0,columnspan=4,pady=10)
        self.dest_entry.grid(column=0,row=1,columnspan=4,pady=10)
    
    def set_values(self, candidates=()):
        self.dest_entry["values"]=candidates
        self.dest_entry.set("")

    def get_list_view(self):
        return self.list

    def click_add_handler(self):    
        if self.dest_entry.get() is "":
            return
        self.add_han(self.dest_entry.get())
        self.dest_entry.delete(0,tk.END)

    def click_delete_handler(self):
        if self.list.curselection() is None:
            return
        ## TODO 削除はいまのところひとつづつ
        self.del_han(self.list.curselection()[0])

# このCombListFrameは以下のエラーが出るのでいまは上のクラスを使う。
# TODO リファクタリング
#     self.add_han(self.dest_entry.get())
# TypeError: 'NoneType' object is not callable
# class ComboListFrame(ListFrame):
#     def __init__(self,master=None,height=10,add_han=None,del_han=None):
#         super().__init__(master=master,height=height,add_han=add_han,del_han=del_han)

#     def create_entry(self):
#         v1=tk.StringVar()
#         return ttk.Combobox(self, state='readonly',textvariable=v1)
    
#     def set_values(self, candidates=()):
#         self.dest_entry["values"]=candidates

#     def click_add_handler(self):    
#         if self.dest_entry.get() is "":
#             return
#         self.add_han(self.dest_entry.get())
#         self.dest_entry.delete(0,tk.END)

class ListView(tk.Listbox):
    def __init__(self,master=None,height=0):
        super().__init__(master=master,height=height)

    def add(self, text=""):
        self.insert(tk.END,text)

    def update(self,items=None):
        self.delete(0,tk.END)
        for item in items:
            self.insert(tk.END,str(item))


class TabManager(ttk.Notebook):
    def __init__(self,master=None):
        super().__init__(master)
        self.tab_count=0
        self.tab_list=[]

    def add_tab(self,tab=None):
        """
        タブを追加する. 上限は8
        tab : TabFarme
        """
        if self.tab_count >= 8:
            return
        self.tab_count = self.tab_count + 1
        tab.place(x=0,y=0)
        self.add(tab,text=str("%d日目" % self.tab_count))
        self.tab_list.append(tab)
        self.select(self.tabs()[-1])

    def get_active_tab_index(self):
        """
        現在表示中のタブのindexを返す
        return : index
        """
        return self.index(tk.CURRENT)

    def get_active_tab(self):
        """
        現在表示中のTabFrameを返す。
        return : TabFrame
        """
        return self.tab_list[self.get_active_tab_index()]