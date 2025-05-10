import os
import shutil
from markdown_blocks import markdown_to_html_node

def static_to_public(source, destination):
    
    # delete everything in public
    if os.path.exists(destination):
        shutil.rmtree(destination)
    # create new public directory
    os.mkdir(destination)


    # copy all files and sub directories from static to public

    # print(os.listdir(source))
    def recurse(path1, path2):
        # for everything in static
        # if directory, recurse
        # if file, copy
        items = os.listdir(path1)
        
        for item in items:
            newpath = os.path.join(path1, item)
            
            # if file, copy
            if os.path.isfile(newpath):
                shutil.copy(newpath, path2)
            # if directory, recurse
            else:
                newdir = os.path.join(path2, item)
                # print(newdir)
                os.mkdir(newdir)
                recurse(newpath, newdir)

    recurse(source, destination)                  

def extract_title(markdown):
    if len(markdown) == 0:
        raise Exception("Markdown text has a length of 0!")
    split_text = markdown.split('\n')
    if split_text[0].startswith("# "):
        return split_text[0].replace("# ", "", 1).strip()
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as content_file:
        content = content_file.read()

        with open(template_path, 'r') as template_file:
            template = template_file.read()

            html = markdown_to_html_node(content).to_html()
            title = extract_title(content)

            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html)
            template = template.replace('href="/', f'href="{basepath}')
            template = template.replace('src="/', f'src="{basepath}')

            with open(dest_path, "w+") as destination_file:
                destination_file.write(template)
            
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise Exception("Content directory does not exist!")
    
    def recurse(dir_path1, dir_path2):
    # for everything in static
    # if directory, recurse
    # if file, copy
        items = os.listdir(dir_path1)
        
        for item in items:
            newpath_1 = os.path.join(dir_path1, item)
            # if file
            if os.path.isfile(newpath_1):
                item = item.replace(".md", ".html")
                newpath_2 = os.path.join(dir_path2, item)
                generate_page(newpath_1, template_path, newpath_2, basepath)
            else:
                newdir = os.path.join(dir_path2, item)
                os.mkdir(newdir)
                recurse(newpath_1, newdir)

    recurse(dir_path_content, dest_dir_path)
