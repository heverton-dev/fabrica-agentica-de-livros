import re

for cap in ['cap_01.md', 'cap_02.md', 'cap_03.md', 'cap_06.md', 'cap_07.md']:
    path = f'output/livros/design-ui-midia-soberana/capitulos/{cap}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where the second duplicate paragraph starts
    idx = content.find("Explorando as minúcias técnicas da implementação de ecossistemas locais")
    if idx != -1:
        # Find where it ends
        end_idx = content.find("mitigando os riscos associados à gestão de infraestrutura própria.", idx)
        if end_idx != -1:
            end_idx += len("mitigando os riscos associados à gestão de infraestrutura própria.")
            content = content[:idx] + content[end_idx:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.replace(" \n##", "\n\n##"))
        
