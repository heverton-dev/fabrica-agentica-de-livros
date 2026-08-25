import glob

for path in glob.glob('output/livros/design-ui-midia-soberana/capitulos/cap_*.md'):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir qualquer espaco antes do ##
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.strip().startswith('## '):
            new_lines.append(line.strip())
        else:
            new_lines.append(line)
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
