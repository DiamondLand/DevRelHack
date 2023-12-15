from pathlib import Path
import os

def count():
    directory = Path(os.getcwd())
    line_count = 0

    for f in directory.rglob('*.py'):
        if not f.is_file() or not f.exists():
            continue

        local_count = 0
        for line in f.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith(('#', '"', "'")):
                continue
            local_count += 1
        
        print(f'{f} - {local_count} ст')
        line_count += local_count

    return line_count