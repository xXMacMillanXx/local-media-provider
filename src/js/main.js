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
