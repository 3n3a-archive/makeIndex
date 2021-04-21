import io
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.ninja')

def checkPathRoot(path):
    if ['.', './'] in path.name:
        return "Root"
    else:
        return path.name

def index(path):
    """Recursive Indexing of all Subdirectories of given `path`"""
    p = Path(path) # declares path
    fs_ = []
    for item in p.iterdir(): # like os.listdir()
        if item.name != 'index.html':
        
            if item.is_dir():
                additive_folders = "/"
                extension = "folder"
            elif item.is_file():
                additive_folders = ""
                extension = item.suffix
                
            fs_.append(
            {
                'name': item.name + additive_folders,
                'mod': item.stat().st_mtime, # TODO: convert modification time from seconds to time format --> UNIX standard time to human time
                'ext': extension,
                'icon': '', # determine correct icon by usage of the library on todo file
                'path': item.name,
                'size': item.stat().st_size, # TODO: convert size from bytes to KB??
            }) # adds the files & folders to fs_ array
            
        if item.is_dir(): # checks if item is a directory
            print(item) # prints the folders name
            index(item) # indexes the folders, subfolders
            
    # render template w fs_ array
    rendered_index = template.render(
    {
        'items': fs_,
        'folderPath': checkPathRoot(path),
        'parent': p.parent
    })
     
    # save rendered index.html
    index_path = p.joinpath('index.html')
    with io.open(index_path, mode='w', encoding='UTF-8') as f_index:
        f_index.write(rendered_index)
        f_index.close()

index('.')