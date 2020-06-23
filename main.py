import requests
import json
from messenger import Messenger

def main():

    # トークンの取得
    with open('token.txt') as f:
        taken = f.read()
    param = {'token': taken.replace('\n','')}

    # 過去の情報を読み込む
    data_get_only = False
    try:
        fr = open("past_data.json", 'r')
        past_data = json.load(fr)
    except FileNotFoundError:
        # 過去データが存在しないとき
        # APIを叩いて、データだけ保存
        data_get_only = True

    # APIを叩く
    url = 'https://slack.com/api/users.list'
    r = requests.get(url, param)
    row_data = r.json()

    # 必要な情報だけ整理
    shaped_data = {}
    for member in row_data['members']:
        if member['name'] == 'slackbot' or member['is_bot']:
            continue
        shaped_data[member['real_name']] = member['profile']['image_512']

    if data_get_only:
        fw = open('past_data.json', 'w')
        json.dump(shaped_data, fw, indent=4)

        return

    ms = Messenger()

    # 過去のデータと比較
    for usr, img_url in shaped_data.items():
        try:
            if past_data[usr] == img_url:
                # print("{}'s image is same.".format(usr))
                pass
            else:
                # print("{}'s image was changed.".format(usr))
                ms.send_post(usr, img_url)
        except KeyError:
            # 新規ユーザー追加 or ユーザー名変更で過去のデータのキーにないとき
            # 特に何もしない
            pass

    fw = open('past_data.json', 'w')
    json.dump(shaped_data, fw, indent=4)

    return

if __name__ == '__main__':
    main()
