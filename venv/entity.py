import control

class DestinationList:
    def __init__(self):
        self.dests=[]

    def set_frame(self, dests_frame=None):
        """
        DestinationListを表示するframe
        dests_frame : util.ListView
        """
        self.dests_frame=dests_frame

    def add(self,dest=None):
        """
        Destinationを追加します。
        dest : Destination
        """
        self.dests.append(dest)
        self.dests_frame.add(dest.get_name())

    # TODO メソッド名をpopに直す
    def delete(self,index=-1):
        """
        Destinationのリストから削除します。
        index : リストのindex
        """
        self.dests_frame.delete(index)
        return self.dests.pop(index)

    def get_names(self):
        """
        Destinationの名前のタプルを返します。
        return : 文字列のタプル
        """
        names = []
        for dest in self.dests:
            names.append(dest.get_name())
        return tuple(names)

    # def get_geos(self):
    #     """
    #     Destinationの位置をタプルで返します。
    #     return : 位置のタプル
    #     """
    #     geos = []
    #     for dest in self.dests:
    #         (lat,lng)=dest.get_geo()
    #         geos.append((lat,lng))
    #     return list(geos)

    def get_dest_by_name(self, dest_name=""):
        """
        目的地の名前の文字列を受け取ってDestinationをpopします。
        dest_name : 目的地の名前の文字列
        """
        index=-1
        for dest in self.dests:
            if dest.get_name() == dest_name:
                index=self.dests.index(dest)
                break
        return self.dests.pop(index)
    
    def update_frame(self):
        """
        dest_frameを現在のdestにupdateします。
        """
        dest_names=list(self.get_names())
        self.dests_frame.update(dest_names)

class Plan:
    def __init__(self,departure=None,arrival=None):
        """
        departure : Destination
        arrival : Destination
        """
        self.departure=departure
        self.arrival=arrival
        self.dests=DestinationList()

    def set_frame(self,dest_frame=None):
        """
        DestinationListを表示するframe
        dests_frame : util.ListView
        """
        self.dests.set_frame(dest_frame)

    def add_dest(self, dest=None):
        """
        Destinationを追加する
        dest : Destination
        """
        self.dests.add(dest=dest)

    def pop_dest(self, index=-1):
        """
        Destinationを取り出す
        index : index
        """
        return self.dests.delete(index=index)

    def get_dep_and_arr_name(self):
        """
        出発地と到着地の名前を返します
        return 出発地と到着地の名前のタプル
        """
        dep = self.departure.get_name()
        arr = self.arrival.get_name()
        return (dep,arr)

    # def get_dep_and_arr_geo(self):
    #     """
    #     出発地と到着地の位置を返します。
    #     return 出発地と到着地の位置
    #     """
    #     (dep_lat,dep_lng)=self.departure.get_geo()
    #     (arr_lat,arr_lng)=self.arrival.get_geo()
    #     return ((dep_lat,dep_lng), (arr_lat,arr_lng))
    
    def update_dests_frame(self):
        """
        destsのframeを更新します。
        """
        self.dests.update_frame()

    def get_dest_names(self):
        """
        destsの目的地の文字列のタプルを取得します
        """
        return self.dests.get_names()

    # def get_dest_geos(self):
    #     """
    #     destsの目的地の位置のタプルを取得します
    #     """
    #     return self.dests.get_geos()

    def sort_by(self, names=None):
        """
        namesの順番にdestを並び替えます。
        names : 目的地の文字列のリスト
        """
        new_dests=DestinationList()
        for name in names:
            dest=self.dests.get_dest_by_name(name)
            new_dests.add(dest)
        self.dests=new_dests

class Destination:
    def __init__(self,text="",lat=0.0,lng=0.0):
        self.name=text
        self.lat=lat
        self.lng=lng

    def get_geo(self):
        return (self.lat,self.lng)

    def get_name(self):
        return self.name
