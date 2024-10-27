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

function set_sidebar_width(size) {
    let r = document.querySelector(':root');
    r.style.setProperty("--sidebar-size", size + "px");
    r.style.setProperty("--topbar-pad-left", size + 15 + "px");
}

/*
var m_pos;
function resize(e) {
    let dx = m_pos - e.x;
    m_pos = e.x;
    set_sidebar_width(m_pos + dx);
}

window.onload = function() {
    let sidebar = document.getElementById('video-list');
    sidebar.addEventListener("mousedown", function(e) {
        if (e.offsetX < 10) {
            m_pos = e.x;
            document.addEventListener("mousemove", resize, false);
        }
    }, false);
};

document.addEventListener("mouseup", function() {
    document.removeListener("mousemove", resize, false);
}, false);
*/
/*
function changeVideo(path) {
    var player = document.getElementsByTagName('video')[0];
    player.children[0].src = path;
    player.load();
}

function changeAudio(path) {
    var player = document.getElementsByTagName('audio')[0];
    player.children[0].src = path;
    player.load();
}

function changeImage(path) {
    var viewer = document.getElementsByTagName('img')[0];
    viewer.src = path;
}
*/
