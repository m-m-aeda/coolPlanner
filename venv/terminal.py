import tkinter as tk
import tkinter.ttk as ttk

class RouteFrame(tk.Frame):
    def __init__(self,master=None,point=None):
        tk.Frame.__init__(self)
        self.point=point
        tk.Label(self,text=point.get_name()).place(x=0,y=0)
        tk.Label(self,bmp="under_arrow.bmp").place(x=30,y=30,width=22,height=22)
        tk.Button(self,text="経路案内",command=self.click_route_guide).place(x=60,y=30)

    def click_route_guide(self):
        pass

class TerminalFrame:
    def __init__(self,schedule=None,entry=None):
        self.schecule=schedule
        self.execute_handler=entry.click_close_handler

    def show(self):
        # Window生成
        self.root = tk.Tk()
        self.root.title("Terminal")
        self.root.geometry('700x450+0+0')
        # タブ
        self.note_book = ttk.Notebook(self.root,width=680,height=380)
        self.note_book.place(x=10,y=0)
        # 閉じるボタン
        tk.Button(self.root,text="閉じる",command=self.close).place(x=650,y=400)
        self.root.mainloop()

    def close(self):
        self.root.destroy()
        self.execute_handler()

    def click_execute_handler(self):
        plans=self.schecule.get_plans()
        for plan in plans:
            self.add_tab(plan)
        self.show()
        
    def add_tab(self,plan):
        y=0
        # TODO ここで新たにタブを作成する。
        for point in plan.get_points():
            RouteFrame(self,point).place(x=0,y=y,width=200,height=60)
            y=y+10
        # TODO planから地図のImageを取得し貼る
        tk.Label(self,bmp="").place(x=10,y=10)