import io
import datetime
from pathlib import Path

# Define this variable with your hostname / Hostname of github pages (username.github.io/projectname)
hostname_site = "https://3n3a.github.io/makeIndex"

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('.github/workflows/templates/'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.ninja')

def getUpdateTime():
    """Returns the current time, with Timezone of System, in human readable format"""
    time_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.now().strftime(time_format)

def checkPathRoot(path):
    if path in ['.', './']:
        return "Root"
    else:
        return path.name


def whatIcon(extension):
    """returns correct icons for extension"""
    icon_types = {
        ".py": "py.svg",
        ".pdf": "pdf.svg",
        "folder": "folder.svg",
        "folder-home": "folder-home.svg"
    }

    return hostname_site + "/public/icons/" + str(icon_types.get(extension, "unknown.svg"))


def index(path):
    """Recursive Indexing of all Subdirectories of given `path`"""
    p = Path(path)  # declares path
    fs_ = []
    for item in p.iterdir():  # like os.listdir()
        if item.name not in ['index.html', 'CNAME', '.gitignore']:
            if item.stem not in ['.git', '.github', 'public']:
                if item.is_dir():
                    additive_folders = "/"
                    extension = "folder"
                elif item.is_file():
                    additive_folders = ""
                    extension = item.suffix

                fs_.append(
                    {
                        'name': item.name + additive_folders,
                        # TODO: convert modification time from seconds to time format --> UNIX standard time to human time
                        'mod': item.stat().st_mtime,
                        'ext': extension,
                        'icon': whatIcon(extension),  # determine correct icon by usage of the library on todo file
                        'path': item.name + additive_folders,
                        'size': item.stat().st_size,  # TODO: convert size from bytes to KB??
                    })  # adds the files & folders to fs_ array

                if item.is_dir():  # checks if item is a directory
                    print(item)  # prints the folders name
                    index(item)  # indexes the folders, subfolders

    # render template w fs_ array
    rendered_index = template.render(
        {
            'items': fs_,
            'folderPath': checkPathRoot(path),
            'parent': '../',
            'updateTime': getUpdateTime()
        })

    # save rendered index.html
    index_path = p.joinpath('index.html')
    with io.open(index_path, mode='w', encoding='UTF-8') as f_index:
        f_index.write(rendered_index)
        f_index.close()


index('.')
