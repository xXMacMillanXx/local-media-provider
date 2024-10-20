import os
from fasthtml.common import *


def page_style():
    return Style("""
        :root {
            --sidebar-size: 320px;
            --topbar-size: 60px;
        }

        .topnav {
            width: 100%;
            height: var(--topbar-size);
            padding: 5px 15px;
        }

        .sidenav {
            height: 100%;
            width: var(--sidebar-size);
            position: fixed;
            z-index: 1;
            top: var(--topbar-size);
            left: 0;
            overflow-x: hidden;
            padding-top: 5px;
        }

        .sidenav a {
            padding: 6px 8px 6px 16px;
            text-decorator: none;
            display: block;
        }

        .main {
            margin-left: var(--sidebar-size);
            padding: 0px 10px;
        }

        @media screen and (max-height: 450px) {
            .sidenav {padding-top: 15px;}
            .sidenav a {}
        }
    """, type="text/css")


def page_script():
    return Script("""
        var volume = 0.1;

        function get_vol() {
            return volume;
        }

        function set_vol(num) {
            volume = num;
        }

        function clear_searchbar() {
            document.getElementsByName("search")[0].value = "";
        }

        function changeVideo(path) {
            var player = document.getElementsByTagName('video')[0];
            player.src = path;
        }
    """, type="text/javascript")


app, rt = fast_app()
supported_video = [".mp4", ".webm", ".ogg"]
supported_audio = [".mp3", ".wav", ".ogg"]
supported_image = [".apng", ".gif", ".ico", ".cur", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png", ".svg", ".webp"]
supported_document = [".pdf"]


def index_page(sess):
    path = sess['path']
    media = get_media_list(path)
    first_vid = ""
    if len(media) > 0:
        first_vid = media[0][1]
    return page_style(), page_script(), sidebar(sess), Div(video_player(first_vid), cls="main")


def filter_list(input: list[str]) -> list[str]:
    """Uses supported_* lists to filter files in list"""
    supported_files = supported_video + supported_audio + supported_image + supported_document
    ret = [file for file in input for ext in supported_files if ext.lower() in file.lower()]
    return ret


def explore(starting_path, level=-1):
    alld = {'': {}}
    count = 0
    if starting_path[-1] == os.sep:
        starting_path = starting_path[0:-1]

    for dirpath, dirnames, filenames in os.walk(starting_path, followlinks=True):
        d = alld
        dirpath = dirpath[len(starting_path):]
        for subd in dirpath.split(os.sep):
            d = d[subd]
        d['directories'] = []
        if dirnames:
            d['directories'] = sorted(dirnames)
            for dn in dirnames:
                d[dn] = {}
        d['directories'].insert(0, "..")
        d['files'] = []
        if filenames:
            d['files'] = sorted(filter_list(filenames))
        count += 1
        if level != -1 and count >= level:
            break
    return alld['']


def get_dir_list(path) -> list[str]:
    ret = explore(path, 1)["directories"]
    return ret


def get_media_list(path) -> list[(str, str)]:
    # worked, but is linux specific
    # ret = [(x.rsplit('/', 1)[1], x) for x in os.popen(f"find -L {path} -maxdepth 1 -type f").read().split('\n') if len(x) > 1]
    # ret.sort()
    media = explore(path, 1)
    ret = [(x, os.path.join(path, x)) for x in media["files"]]
    return ret


def get_tree(path, level=-1) -> dict[str]:
    return explore(path, level)


def sidebar(sess):
    c_list = create_sidebar_links(sess)
    return Div(Input(type="search", name="search", list="searchwords", hx_post="/search", hx_trigger="input changed delay:500ms, search", hx_target="#video-list"), cls="topnav"), Div(*c_list, create_datalist(sess), cls="sidenav", id="video-list")


def create_sidebar_links(sess) -> list[A]:
    path = sess['path']
    dirs = get_dir_list(path)
    media = get_media_list(path)
    d_list = [create_dir_link(x) for x in dirs]
    a_list = [create_file_link(x[0], x[1]) for x in media]
    return d_list + a_list


def create_datalist(sess) -> list[Option]:
    path = sess['path']
    dirs = get_dir_list(path)
    media = get_media_list(path)
    opts = [Option(value=x) for x in dirs]
    opts += [Option(value=x[0]) for x in media]
    return Datalist(*opts, id="searchwords")


def create_file_link(name: str, path: str):
    return A(f"{name}", onclick=f"changeVideo(\"{path}\")")


def create_dir_link(x: str):
    return A(f"{x}", hx_post="change_tree", hx_target="#video-list", hx_vals="{\"value\":\"" + x + "\"}", onclick="clear_searchbar()")


def video_player(video_path):
    return Video(Source(src=video_path, type="video/mp4"), style="width:100%;height:95vh;", onloadstart="this.volume=get_vol()", onvolumechange="set_vol(this.volume)", controls="controls", autoplay="autoplay", loop="loop", preload="auto")


@rt('/')
def get(sess):
    if 'path' not in sess:
        sess['path'] = "media"  # set start directory
    return index_page(sess)


@rt("/{fname:path}.{ext:static}")
def get(fname:str, ext:str, sess):
    return FileResponse(f'{fname}.{ext}', headers={"accept-ranges": "bytes"})


@rt('/search')
def post(search: str , sess):
    ret = []
    tree = get_tree(sess['path'], 1)
    for x in tree['directories']:
        if search.lower() in x.lower():
            ret.append(create_dir_link(x))
    for x in tree['files']:
        if search.lower() in x.lower():
            ret.append(create_file_link(x, os.path.join(sess['path'], x)))
    return ret, create_datalist(sess)


@rt('/change_tree')
def post(value: str, sess):
    path = os.path.join(sess['path'], value)
    if value == "..":
        path = sess['path'].rsplit(os.sep, 1)[0]
    sess['path'] = path

    return create_sidebar_links(sess), create_datalist(sess)


serve()
