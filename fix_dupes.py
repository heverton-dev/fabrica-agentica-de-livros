import re

for cap in ['cap_01.md', 'cap_02.md', 'cap_03.md', 'cap_06.md', 'cap_07.md']:
    path = f'output/livros/design-ui-midia-soberana/capitulos/{cap}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where "Esta discussão sobre soberania baseia-se..." begins
    idx = content.find("Esta discussão sobre soberania baseia-se")
    if idx != -1:
        # Find where it ends
        end_idx = content.find("conquistadas com tanto esforço [2].", idx)
        if end_idx != -1:
            end_idx += len("conquistadas com tanto esforço [2].")
            content = content[:idx] + content[end_idx:]

    idx2 = content.find("Na fase técnica da implementação, garantir a soberania")
    if idx2 != -1:
        end_idx2 = content.find("produção contínua e segura [4].", idx2)
        if end_idx2 != -1:
            end_idx2 += len("produção contínua e segura [4].")
            content = content[:idx2] + content[end_idx2:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(" \n##", "\n\n##"))
        
