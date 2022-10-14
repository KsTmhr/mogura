import asyncio
import json
import logging
import websockets
import csv
import os


logging.basicConfig()

CONNECTIONS = set()
MOGURAS = set()
RANKING = set()

DATA_BASE = "rank.csv" # データファイル
SHOWING_NUM = 5 # 表示するランキング


#-------------------------------関数たち-----------------------------------------
# 送信テンプレート
def make_data(type, data):
    return json.dumps({"type": type, "data": data})


# ファイル取得
def get_ranking_list():
    global DATA_BASE

    # csv取得
    with open(DATA_BASE, "r") as f:
        reader = csv.reader(f)
        a = [row for row in reader][0]

    return a


# 順位を取得
def get_rank(a, i):
    return a.index(i)


# 配列を更新
def update(a, i, d):
    a.insert(i, d)


# ファイル書き換え
def upload(a):
    global DATA_BASE

    os.remove(DATA_BASE) # 削除

    with open(DATA_BASE, 'w') as f: # 新規作成
        writer = csv.writer(f)
        writer.writerow(a)


# top5取得
def get_top():
    global SHOWING_NUM

    a = get_ranking_list()
    return [a[i] for i in range(SHOWING_NUM)]


# ランキング参照 & 更新
def refer_ranking(c, d):
    rankers = get_ranking_list()
    rank = 0

    # 強かったら削除して新規作成
    for point in rankers:
        if d > int(point):
            rank = get_rank(rankers, point)
            update(rankers, rank, d) #ランキング塗り替え
            break


    upload(rankers) # データベース（笑）書き換え
    # websockets.broadcast(c, make_data("info", "updated!"))
    #await websocket.send(make_data("info", "updated!"))
    print(f"Ranking was updated:{rankers}")

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
                    print("ranking")
                    RANKING.add(websocket)

                case "mogura":
                    print("mogura")
                    MOGURAS.add(websocket)


                case "score":
                    print("score")
                    rank = refer_ranking(CONNECTIONS, data["data"])
                    # print(rank)
                    websockets.broadcast(MOGURAS, make_data("rank", rank))
                    # topに入ったら送信
                    if rank < SHOWING_NUM:
                        websockets.broadcast(RANKING, make_data("top", get_top()))

                case "get_top":
                    print("get_top")
                    websockets.broadcast(RANKING, make_data("top", get_top()))



    finally:
        CONNECTIONS.remove(websocket)



#-----------------------------------実行-----------------------------------------
async def main():
    #async with websockets.serve(score, "192.168.1.224", 8765):
    async with websockets.serve(score, "localhost", 8765, ping_interval=None):
        print("runserver")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
