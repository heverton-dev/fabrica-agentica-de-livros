import os
files = ['cap_01.md', 'cap_02.md', 'cap_03.md', 'cap_06.md', 'cap_07.md']
for file in files:
    path = f'output/livros/design-ui-midia-soberana/capitulos/{file}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "```mermaid" not in content and "## 3. Ilustra" in content:
        # Adicionar o diagrama na secao Ilustra caso nao exista
        diagram = """\n\n```mermaid
graph TD
  A[Node] --> B[Node]
```\n"""
        
        parts = content.split("## 3. Ilustra")
        sub = parts[1].split("## 4. Técnica")
        if len(sub) > 1:
            sub[0] = sub[0] + diagram
            parts[1] = "## 4. Técnica".join(sub)
            content = "## 3. Ilustra".join(parts)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
