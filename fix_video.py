import os
import glob

search_str = "{% static 'videos/tail.mp4' %}"
replace_str = "https://videos.pexels.com/video-files/8306458/8306458-uhd_2160_4096_25fps.mp4"

for filepath in glob.glob("**/*.html", recursive=True):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if search_str in content:
        content = content.replace(search_str, replace_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
