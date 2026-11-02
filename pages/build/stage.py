import json, os, pathlib, re, shutil, sys

src = pathlib.Path('src/docs')
out = pathlib.Path('site-src')
blob = f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/blob/{os.environ['SHA']}"
composer = json.loads(pathlib.Path('composer.json').read_text())

shutil.copytree(src, out)

failed = False
for page in sorted(out.rglob('*.md')):
    text = page.read_text()
    if re.search(r'\{%-?\s*(end)?raw\b', text):
        print(f"::error file=src/docs/{page.relative_to(out)}::holds a raw or endraw tag, which the page's own raw block cannot contain.")
        failed = True
        continue

    text = re.sub(r'\]\(\s*\.\./\.\./', f'](' + blob + '/', text)
    text = re.sub(r'\]\(\s*\.\./', f'](' + blob + '/src/', text)

    heading = re.search(r'^#\s+(.+?)\s*#*\s*$', text, re.M)
    title = heading.group(1) if heading else page.stem
    page.write_text(
        '---\n'
        f'title: {json.dumps(title)}\n'
        '---\n'
        '{% raw %}\n'
        f'{text.rstrip()}\n'
        '{% endraw %}\n'
    )

if failed:
    sys.exit(1)

name = composer['name'].split('/')[-1]
(out / '_config.yml').write_text(
    f'title: {json.dumps(name)}\n'
    f"description: {json.dumps(composer.get('description', ''))}\n"
    f"baseurl: {json.dumps(os.environ['BASE_PATH'])}\n"
)
