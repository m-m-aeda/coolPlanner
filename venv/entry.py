import sys
import tkinter as tk
import tkinter.ttk as ttk
import utils as u
import window as w
import frame as f
import entity
import control

class Entry:
    def __init__(self):
        candidate_dest=entity.DestinationList()
        self.schedule=control.Schedule(candidate_dest)

        self.entry_frame = w.EntryWindow(
            candidate_dest,
            add_han=self.__click_candidate_add,
            next_han=self.__click_candidate_next)

    # 候補地入力画面のハンドラー

    def __click_candidate_add(self, text=""):
        """
        候補地入力画面で追加が押された
        text : entryの文字列
        """
        self.schedule.add_candidate(text)        

    def __click_candidate_next(self):
        """
        候補地入力画面で次へが押された
        """
        w.PlanWindow(
            add_han=self.click_primary_add,
            del_han=self.click_primary_del,
            next_han=self.click_next_to_terminal,
            back_han=self.click_back_to_entry,
            init_exe_han=self.click_init_execute,
            schedule=self.schedule)        

    # 出発地と到着地の画面のハンドラー

    def click_init_execute(self,dep="",arr="",tabs=None,add_han=None,del_han=None):
        """
        出発地と到着地の画面でOKが押された
        dep : 出発地の文字列
        arr : 到着地の文字列
        tabs : util.TabManager
        """
        plan=self.schedule.init_plan(dep=dep,arr=arr)
        if plan is None:
            # TODO ダイアログを表示する。
            pass
        candidates = self.schedule.get_candidate_names()
        tab_frame = f.TabFrame(master=tabs,plan=plan,candidates=candidates,add_han=add_han,del_han=del_han)
        tab_frame.place(width=300,height=300)
        plan.set_frame(tab_frame.get_list_view())
        tabs.add_tab(tab_frame)
        
    # 日程設定画面のハンドラー
    
    def click_primary_add(self,tab=None,tab_index=-1,dest_name=""):
        """
        日程設定画面で追加ボタンが押された
        tab_index : タブのindex
        dest_name : 選択された目的地の名前の文字列
        """
        self.schedule.add_primary(tab_index=tab_index,dest_name=dest_name)
        candidates=self.schedule.get_candidate_names()
        # Comboboxの更新
        tab.update_values(candidates)
    
    def click_primary_del(self,tab=None,tab_index=-1,dest_index=-1):
        """
        日程設定画面で削除ボタンが押された
        tab : TabFrame
        tab_index : タブのindex
        dest_index : 選択された目的地のindex
        """
        self.schedule.del_primary(tab_index=tab_index,dest_index=dest_index)
        candidates=self.schedule.get_candidate_names()
        # Comboboxの更新
        tab.update_values(candidates)

    def click_back_to_entry(self):
        """
        日程選択画面で戻るボタンが押された
        """
        self.schedule.update_candidates()

    def click_next_to_terminal(self):
        """
        日程選択画面で次へボタンが押された
        """
        # GoogleApi用
        w.TerminalWindow(opt_plans=self.schedule.get_optimized_plans())
        # yahoo.api用
        # w.TerminalWindow(opt_images=self.schedule.get_optimized_images())
        # self.schedule.update_candidates()
        
Entry()