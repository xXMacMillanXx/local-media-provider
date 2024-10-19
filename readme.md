# Local Media Center

This is a simple and minimalistic project, creating a convenient media center for your local files. Currently the project is looking for a *media* folder inside the same folder as the *main.py* file.

## Installation / Usage

Requirements
```bash
pip install python-fasthtml
```

Run project
```bash
python main.py
```
Starting the project, it should tell you the address. By default this should be 0.0.0.0:5001 or 127.0.0.1:5001. Open it in your web browser of choice.

Like I mentioned, currently the project is looking for a *media* folder in the same directory. You can copy some files there to test, or create symlink to a folder called media.
```bash
ln -s /path/to/media/you/want/to/see media
```

## What currently works

 - videos can be played (only HTML video tag / browser supported formats)
 - files and folders are listed in the sidebar
 - sidebar can be filtered / searched with the topbar

## Which additions are planned?

### Want to add

 - setting filters for files listed in the sidebar (e.g. mp4, webm - filetypes)

### Might add

 - playing audio files
 - view images
 - open pdf files

## What is not planned?

Everything not listed in the section above.  
I want the project to stay simple with a clear focus.

