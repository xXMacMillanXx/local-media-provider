# Local Media Center

This is a simple and minimalistic project, creating a convenient media center for your local files. Currently the project is looking for a *media* folder inside the same folder as the *main.py* file.

## Installation / Usage

Requirements
```bash
pip install python-fasthtml
pip install baize
```

Run project
```bash
python main.py
```
Starting the project, it should tell you the address. By default this should be 0.0.0.0:5001 or 127.0.0.1:5001. Open it in your web browser of choice.

Like I mentioned, currently the project is looking for a *media* folder in the same directory. You can copy some files there to test, or create a symlink to a folder called media.
```bash
ln -s /path/to/media/you/want/to/see media
```

If you want to add online media (e.g., youtube videos) you can create a *.link* file which contains the link to the video.
Copy the embed link from the video. (YouTube: Share -> Embed -> copy link from *src* attribute)

For example, a link file for the Youtube rewind 2014, would look like this:  
Filename: *Youtube Rewind 2024.link*
```link
https://www.youtube.com/embed/zKx2B8WCQuw
```

## What currently works

 - videos can be played (only HTML video tag / browser supported formats)
 - audio can be played (only HTML audio tag / browser supported formats)
 - images can be viewed (only HTML img tag / browser supported formats)
 - pdfs can be viewed (uses embed, should be the browser pdf viewer)
 - links to websites and embed media can be viewed with *link* files (uses iframe, some websites might block this)
 - files and folders are listed in the sidebar (only web supported formats)
 - sidebar can be filtered / searched with the topbar

## Which additions are planned?

### Want to add

 - *currently empty*

### Might add

 - save media as favorite?
 - add subfolder search for searchbar?

## What is not planned?

Everything not listed in the section above.  
I want the project to stay simple with a clear focus.

