import settings
import os

txt_path = os.path.join(os.path.dirname(__file__), 'tor_path.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(settings.TOR_EXE_PATH)
print('tor_path.txt создан/обновлён')