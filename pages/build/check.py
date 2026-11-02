import html, pathlib, re, sys

failed = False
for page in sorted(pathlib.Path('src/docs').rglob('*.md')):
    built = pathlib.Path('_site') / page.relative_to('src/docs').with_suffix('.html')
    if not built.is_file():
        print(f'::error file={page}::was not built: no {built}.')
        failed = True
        continue
    rendered = html.unescape(re.sub(r'<[^>]*>', '', built.read_text()))
    for token in ('{{', '{%'):
        want, got = page.read_text().count(token), rendered.count(token)
        if got < want:
            print(f'::error file={page}::{want} {token} in the source, {got} on the built page: Liquid rendered some of them.')
            failed = True

sys.exit(1 if failed else 0)
