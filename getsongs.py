import requests, json
import webbrowser, time, glob

songlist = glob.glob("C:\\Users\\David\\Downloads\*.osz") + glob.glob("F:\\osu!\\Songs\\*\\")

for i in range(150):
    print("OFFSET", i)
    r = requests.get("https://osusearch.com/query/?statuses=Ranked&modes=Standard&star=(5.50,10.00)&offset={}".format(i))
    data = json.loads(r.text)
    for i, song in enumerate(data['beatmaps']):
        beatmapset_id = song['beatmapset_id']
        print(beatmapset_id)
        if not any([str(beatmapset_id) in x for x in songlist]):
            url = "https://osu.ppy.sh/beatmapsets/{}/download?noVideo=1".format(song['beatmapset_id'])
            webbrowser.open(url, autoraise=False)
            time.sleep(3)
            if i == len(data['beatmaps']) - 1:
                time.sleep(1500)