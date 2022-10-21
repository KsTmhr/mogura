import asyncio
import json
import logging
import websockets
import csv
import os


logging.basicConfig()

CONNECTIONS = set()
RANKING = set()
MOGURAS = {}
MANAGERS = {}

DATA_BASE = "rank.csv" # データファイル
SHOWING_NUM = 10 # 表示するランキング


#-------------------------------関数たち-----------------------------------------
# 送信テンプレート
def make_data(type, data=None):
    return json.dumps({"type": type, "data": data})


# ファイル取得
def get_list(m):
    global DATA_BASE

    # csv取得
    with open(DATA_BASE, "r") as f:
        reader = csv.reader(f)
        a = [row for row in reader]

    if m == "rank":
        return a[0]

    elif m == "name":
        return a[1]


# 順位を取得
def get_rank(a, i):
    return a.index(i)


# リストを更新
def update_list(a, i, d):
    a.insert(i, d)


# ファイル書き換え
def upload(a, b):
    global DATA_BASE

    os.remove(DATA_BASE) # 削除

    with open(DATA_BASE, 'w', newline="") as f: # 新規作成
        writer = csv.writer(f)
        writer.writerow(a)
        writer.writerow(b)


# toprank取得
def get_top_rank():
    global SHOWING_NUM

    a = get_list("rank")
    return [a[i] for i in range(SHOWING_NUM)]


# topname取得
def get_top_name():
    global SHOWING_NUM

    a = get_list("name")
    return [a[i] for i in range(SHOWING_NUM)]


# ランキング参照 & 更新
def refer_ranking(c, d):
    rankers = get_list("rank")
    name = get_list("name")
    rank = 0

    # 強かったら削除して新規作成
    for point in rankers:
        if d > int(point):
            rank = get_rank(rankers, point)
            update_list(rankers, rank, d) #ランキング塗り替え
            break

    update_list(name, rank, "unknown")

    upload(rankers, name) # データベース（笑）書き換え
    # websockets.broadcast(c, make_data("info", "updated!"))
    #await websocket.send(make_data("info", "updated!"))
    print("Ranking was updated")

    return rank


#---------------------------------通信-------------------------------------------
async def score(websocket):
    global CONNECTIONS, MOGURAS, RANKING

    try:
        # 接続を登録
        CONNECTIONS.add(websocket)

        await websocket.send(make_data("info", "welcome to mogura world"))

        # データ受信
        async for message in websocket:

            # デコード
            print(message)
            data = json.loads(message)

            # もし type が scare ならランキングに反映
            match data["type"]:

                case "ranking":
                    print("register ranking")
                    RANKING.add(websocket)

                case "mogura":
                    print("register mogura")
                    MOGURAS[websocket] = data["data"]

                case "manager":
                    print("register manager")
                    MANAGERS[data["data"]] = websocket


                case "score":
                    print("score")
                    await websocket.send(make_data("info", "got it"))
                    rank = refer_ranking(CONNECTIONS, data["data"])
                    try:
                        await MANAGERS[MOGURAS[websocket]].send(make_data("rank", rank))

                    except KeyError:
                        print("登録されていません")

                    # topに入ったら送信
                    if rank < SHOWING_NUM:
                        websockets.broadcast(RANKING, make_data("top", {"rank":get_top_rank(), "name":get_top_name()}))

                case "get_top":
                    print("get_top")
                    websockets.broadcast(RANKING, make_data("top", {"rank":get_top_rank(), "name":get_top_name()}))

                case "name":
                    rank = data["data"]["rank"]
                    rankers = get_list("rank")
                    name = get_list("name")
                    name[rank] = data["data"]["name"]

                    upload(rankers, name)
                    websockets.broadcast(RANKING, make_data("top", {"rank":get_top_rank(), "name":get_top_name()}))


                case "start":
                    key = [k for k, v in MANAGERS.items() if websocket == v][0]
                    print("start")
                    mogura = [k for k, v in MOGURAS.items() if key == v][0]
                    await mogura.send(make_data("start"))

    finally:
        CONNECTIONS.remove(websocket)



#-----------------------------------実行-----------------------------------------
async def main():
    #async with websockets.serve(score, "192.168.1.224", 8765):
    #async with websockets.serve(score, "localhost", 8765, ping_interval=None):
    async with websockets.serve(score, "10.0.1.3", 8765, ping_interval=None):

        print("runserver")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
