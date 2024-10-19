import os
from fasthtml.common import *


# Works, but if session cookie is full, can produce issues.
# cookie gets full if too many files are found in the folder.
# maybe other storage is available, or perhaps a database could help.

# Make it possible to filter files, so only specific file types show up.
# for example, mp4 and webm


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

        function changeVideo(path) {
            var player = document.getElementsByTagName('video')[0];
            player.src = path;
        }
    """, type="text/javascript")


app, rt = fast_app()


def index_page(sess):
    path = sess['path']
    media = get_media_list(path)
    sess['tree'] = get_tree(path, True)
    first_vid = ""
    if len(media) > 0:
        first_vid = media[0][1]
    return page_style(), page_script(), sidebar(sess), Div(video_player(first_vid), cls="main")


def explore(starting_path, space_saver=False):
    alld = {'': {}}
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
            d['files'] = sorted(filenames)
    if space_saver:
        return {"directories": alld['']['directories'], "files": alld['']['files']}
    else:
        return alld['']


def get_dir_list(path) -> list[str]:
    ret = explore(path)["directories"]
    return ret


def get_media_list(path) -> list[(str, str)]:
    # worked, but is linux specific
    # ret = [(x.rsplit('/', 1)[1], x) for x in os.popen(f"find -L {path} -maxdepth 1 -type f").read().split('\n') if len(x) > 1]
    # ret.sort()
    media = explore(path)
    ret = [(x, os.path.join(path, x)) for x in media["files"]]
    return ret


def get_tree(path, space_saver=False) -> dict[str]:
    return explore(path, space_saver)


def sidebar(sess):
    c_list = create_sidebar_links(sess)
    return Div(Input(type="search", name="search", list="searchwords", hx_post="/search", hx_trigger="input changed delay:500ms, search", hx_target="#video-list"), cls="topnav"), Div(*c_list, create_datalist(sess), cls="sidenav", id="video-list")


def create_sidebar_links(sess) -> list[A]:
    path = sess['path']
    dirs = sess['tree']['directories']
    media = get_media_list(path)
    d_list = [create_dir_link(x) for x in dirs]
    a_list = [create_file_link(x[0], x[1]) for x in media]
    return d_list + a_list


def create_datalist(sess) -> list[Option]:
    path = sess['path']
    dirs = sess['tree']['directories']
    media = get_media_list(path)
    opts = [Option(value=x) for x in dirs]
    opts += [Option(value=x[0]) for x in media]
    return Datalist(*opts, id="searchwords")


def create_file_link(name: str, path: str):
    return A(f"{name}", onclick=f"changeVideo(\"{path}\")")


def create_dir_link(x: str):
    return A(f"{x}", hx_post="change_tree", hx_target="#video-list", hx_vals="{\"value\":\"" + x + "\"}")


def video_player(video_path):
    return Video(Source(src=video_path, type="video/mp4"), style="width:100%;height:95vh;", onloadstart="this.volume=get_vol()", onvolumechange="set_vol(this.volume)", controls="controls", autoplay="autoplay", loop="loop", preload="auto")


@rt('/')
def get(sess):
    sess['tree'] = {}
    if 'path' not in sess:
        sess['path'] = "media"  # set start directory
    return index_page(sess)


@rt("/{fname:path}.{ext:static}")
def get(fname:str, ext:str, sess):
    return FileResponse(f'{fname}.{ext}', headers={"accept-ranges": "bytes"})


@rt('/search')
def post(search: str , sess):
    ret = []
    for x in sess['tree']['directories']:
        if search.lower() in x.lower():
            ret.append(create_dir_link(x))
    for x in sess['tree']['files']:
        if search.lower() in x.lower():
            ret.append(create_file_link(x, os.path.join(sess['path'], x)))
    return ret, create_datalist(sess)


@rt('/change_tree')
def post(value: str, sess):
    path = os.path.join(sess['path'], value)
    if value == "..":
        path = sess['path'].rsplit(os.sep, 1)[0]
    sess['tree'] = get_tree(path, True)
    sess['path'] = path

    return create_sidebar_links(sess), create_datalist(sess)


serve()