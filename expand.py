import os

caps = ['cap_01.md', 'cap_02.md', 'cap_03.md', 'cap_06.md', 'cap_07.md']
for cap in caps:
    path = f'output/livros/design-ui-midia-soberana/capitulos/{cap}'
    os.system(f"git restore {path}")
