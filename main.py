import os
from fasthtml.common import *
from baize.asgi.staticfiles import Files


# database could include favorites?


media_folder = "media"
routes = [
    Mount(f'/{media_folder}', app=Files(directory='.'), name=f"{media_folder}")
]
hdrs = [
    Title("Media Center"),  # leave title as first element in the list
    Link(rel="stylesheet", href="src/css/main.css"),
    Script(src="src/js/main.js")
]


app, rt = fast_app(hdrs=hdrs, routes=routes)
# write file endings in lower case
supported_video = [".mp4", ".webm", ".ogg"]
supported_audio = [".mp3", ".wav", ".ogg"]
supported_image = [".apng", ".gif", ".ico", ".cur", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png", ".svg", ".webp"]
supported_document = [".pdf"]
supported_web = [".link"]


def index_page(sess):
    path = sess['path']
    media = get_media_list(path)
    first_media = ""
    if len(media) > 0:
        first_media = media[0][1]
    media_display = get_suitable_display(first_media)
    return hdrs[0], sidebar(sess), searchbar(sess), Div(media_display, cls="main")


def file_filter(x: str, file_formats: list[str]):
    # could do [f.lower() for f in file_formats] but formats should be lower case anyways
    if x.lower().endswith(tuple(file_formats)):
        return True
    return False


def filter_list(input: list[str]) -> list[str]:
    """Uses supported_* lists to filter files in list"""
    supported_files = supported_video + supported_audio + supported_image + supported_document + supported_web
    ret = list(filter(lambda x: file_filter(x, supported_files), input))
    return ret


def explore(starting_path: str, level: int = -1):
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


def get_dir_list(path: str) -> list[str]:
    ret = explore(path, 1)["directories"]
    return ret


def get_media_list(path: str) -> list[(str, str)]:
    media = explore(path, 1)
    ret = [(x, os.path.join(path, x)) for x in media["files"]]
    return ret


def get_tree(path: str, level: int = -1) -> dict[str]:
    return explore(path, level)


def get_suitable_display(media_path: str):
    ext = which_media_type(media_path)
    if ext == "video":
        return video_player(media_path)
    if ext == "audio":
        return audio_player(media_path)
    if ext == "image":
        return image_viewer(media_path)
    if ext == "document":
        return pdf_viewer(media_path)
    if ext == "web":
        return web_viewer(media_path)
    return ""


def which_media_type(file: str) -> str:
    if "." not in file:
        return "unsupported"

    ext = "." + file.rsplit('.', 1)[1].lower()
    if ext in supported_video:
        return "video"
    if ext in supported_audio:
        return "audio"
    if ext in supported_image:
        return "image"
    if ext in supported_document:
        return "document"
    if ext in supported_web:
        return "web"
    return "unsupported"


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
    ext = which_media_type(path)
    if ext in ["video", "audio", "image", "document", "web"]:  # or != unsupported
        return A(f"{name}", hx_post="update_display", hx_target=".main", hx_vals="{\"media_path\":\"" + path + "\"}")
    return A(f"{name}")


def create_dir_link(x: str):
    return A(f"{x}", hx_post="change_tree", hx_target="#video-list", hx_vals="{\"value\":\"" + x + "\"}", onclick="clear_searchbar()")


def searchbar(sess):
    return Div(Input(type="search", name="search", list="searchwords", hx_post="/search", hx_trigger="input changed delay:500ms, search", hx_target="#video-list"), cls="topnav")


def sidebar(sess):
    c_list = create_sidebar_links(sess)
    return Div(*c_list, create_datalist(sess), cls="sidenav", id="video-list")


def video_player(video_path: str):
    return Video(Source(src=video_path, type="video/mp4"), style="width:100%;max-height:92vh;", onloadstart="this.volume=get_vol()", onvolumechange="set_vol(this.volume)", controls="controls", autoplay="autoplay", loop="loop", preload="auto")


def audio_player(audio_path: str):
    return Audio(Source(src=audio_path, type="audio/mpeg"), onloadstart="this.volume=get_vol()", onvolumechange="set_vol(this.volume)", controls="controls", autoplay="autoplay", preload="auto")


def image_viewer(image_path: str):
    return Div(Img(src=image_path, id="image_box"), id="scale_box")


def pdf_viewer(pdf_path: str):
    return Embed(src=pdf_path, type="application/pdf", width="100%", style="height:92vh;")


def web_viewer(web_path: str):
    web_link = ""
    with open(web_path, "r") as f:
        web_link = f.read()
    return Iframe(src=web_link, title="Web Viewer", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share", referrerpolicy="strict-origin-when-cross-origin", allowfullscreen="allowfullscreen", width="100%", style="height:92vh;border:none;")


@rt('/')
def get(sess):
    if 'path' not in sess:
        sess['path'] = media_folder
    return index_page(sess)


@rt("/{fname:path}.{ext:static}")
def get(fname: str, ext: str, sess):
    return FileResponse(f'{fname}.{ext}', headers={"accept-ranges": "bytes"})


@rt('/search')
def post(search: str, sess):
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


@rt('/update_display')
def post(media_path: str, sess):
    return get_suitable_display(media_path)


serve()
