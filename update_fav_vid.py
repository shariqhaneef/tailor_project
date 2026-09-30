import os

favicon_html = '    <link rel="icon" type="image/gif" href="{% static \'images/logo3.gif\' %}">\n'

def add_favicon(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "rel=\"icon\"" not in content:
        content = content.replace("<head>", f"<head>\n{favicon_html}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added favicon to {filepath}")

add_favicon(r"core_config\templates\base.html")
add_favicon(r"core_config\templates\tailor_base.html")

# Fix register.html video
reg_file = r"users\templates\users\register.html"
with open(reg_file, 'r', encoding='utf-8') as f:
    reg_content = f.read()

old_vid = "https://videos.pexels.com/video-files/8306458/8306458-uhd_2160_4096_25fps.mp4"
new_vid = "https://videos.pexels.com/video-files/5759060/5759060-uhd_2160_3840_30fps.mp4"

if old_vid in reg_content:
    reg_content = reg_content.replace(old_vid, new_vid)
    with open(reg_file, 'w', encoding='utf-8') as f:
        f.write(reg_content)
    print("Replaced video in register.html")
