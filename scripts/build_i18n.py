from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'i18n-source.json').read_text(encoding='utf-8'))
assert len(data)==12
for code,values in data.items():
 assert values.keys()==data['en-US'].keys(),code
 assert all(isinstance(v,str) and v for v in values.values()),code
(root/'i18n.js').write_text('const MaterialTranslations = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
print(len(data),'languages;',len(data['en-US']),'keys each')
