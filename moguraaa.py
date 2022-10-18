import asyncio
import random
import time

# モグラ起動時間
mogura_time = 3
# フレーム
frame = 0.3
# モグラが起動しているか
mogura_is_standing = [False, False, False, False, False]


# led出力（想定）
def led(n, m):
    if m == 1:
        print(f"{n}led on")

    elif m == 0:
        print(f"{n}led off")


# モグラ関数
async def mogura(num):
    # 起動する
    led(num, 1)
    mogura_is_standing[num] = True

    # ３秒待つ -> mainのループは邪魔されない
    await asyncio.sleep(mogura_time)

    # 終わったら戻ってきてモグラ終了
    led(num, 0)
    mogura_is_standing[num] = False


# メインループ
async def main():

    while True:
        # ランダムでモグラ選択
        mogura_num = random.randrange(5)

        # 起動してない子だったら起動
        if not mogura_is_standing[mogura_num]:
            task = asyncio.create_task(mogura(mogura_num))

        await asyncio.sleep(frame)



asyncio.run(main())
