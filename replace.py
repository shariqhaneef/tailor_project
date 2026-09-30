import os
import re

directory = '.'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(('.html', '.py', '.js', '.txt', '.md')):
            if 'migrations' in root:
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace('logo3.gif', 'logo3.gif')
            
            # Replace Case-Insensitive 'TailorCraft' -> 'TailorCraft'
            new_content = re.sub(re.compile(r'TailorCraft', re.IGNORECASE), 'TailorCraft', new_content)
            
            # Replace 'TailorCraft' -> 'TailorCraft' just in case
            new_content = re.sub(re.compile(r'TailorCraft', re.IGNORECASE), 'TailorCraft', new_content)
            
            # Also replace 'tailorcraft_theme' -> 'tailorcraft_theme'
            new_content = new_content.replace('tailorcraft_theme', 'tailorcraft_theme')
            
            if content != new_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {path}')
