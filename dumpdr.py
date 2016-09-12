import os, sys, re
import requests, json

ASSET_API_ENDPOINT = "http://www.dr.dk/mu-online/api/1.3/page/tv/player/%s"

def get_json(url):
    return requests.get(url).json()

def parse_extm3u(playlist):
    while not playlist[0].startswith("#EXT-X-STREAM-INF"):
        playlist.pop(0)

    records = []
    for i in range(len(playlist) // 2):
        header = playlist[i * 2]
        url = playlist[i * 2 + 1]
        bandwidth = int(re.search(r'BANDWIDTH=(\d+)', header[18:]).group(1))
        records.append((bandwidth, url))

    # TODO: let the user figure out which quality they want.
    records.sort(reverse=True)
    bandwidth, url = records[0]

    return url, bandwidth

def get_asset_link(slug):
    primary_asset_uri = get_json(ASSET_API_ENDPOINT % slug)["ProgramCard"]["PrimaryAsset"]["Uri"]
    primary_asset = get_json(primary_asset_uri)

    for link in primary_asset["Links"]:
        if link["Target"] == "HDS":
            stream_uri = link["Uri"]
            break

    # this is where the magic happens!
    playlist_uri = stream_uri.replace('/z/', '/i/').replace('manifest.f4m', 'master.m3u8')
    playlist = requests.get(playlist_uri).text.splitlines()

    asset_url, bandwidth = parse_extm3u(playlist)

    return asset_url


if __name__=='__main__':
    slug = sys.argv[1].split('/')[-1]
    url = get_asset_link(slug)
    cmdline = "ffmpeg -i '%s' -acodec copy -vcodec copy -absf aac_adtstoasc '%s.mp4' " % (url, slug)

    print(cmdline)
