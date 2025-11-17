#!/usr/bin/env python3
import os,sys,re
from pathlib import Path

def split_frontmatter(text):
    if text.startswith('+++'):
        parts = text.split('+++',2)
        if len(parts)>=3:
            return parts[1].strip(), parts[2].lstrip('\n')
    return None, text


def main():
    root = Path('/Users/joshstark/0xstark')
    in_path = root / 'content' / 'posts' / 'YIE2020' / 'index.md'
    if not in_path.exists():
        print('index.md not found at', in_path, file=sys.stderr); sys.exit(1)
    text = in_path.read_text(encoding='utf-8')
    fm, html = split_frontmatter(text)
    if fm is None:
        print('No TOML frontmatter detected; aborting', file=sys.stderr); sys.exit(1)

    try:
        from bs4 import BeautifulSoup
        from markdownify import markdownify as md
    except Exception as e:
        print('Missing dependencies:', e, file=sys.stderr)
        print('Please run: pip3 install beautifulsoup4 markdownify')
        sys.exit(1)

    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script','style','noscript','header','footer','nav','form','button']):
        tag.decompose()
    for el in soup.find_all(True):
        attrs = dict(el.attrs)
        for a in list(attrs.keys()):
            if a.startswith('on'):
                del el.attrs[a]
            if a in ('href','src') and isinstance(attrs[a],str) and attrs[a].strip().lower().startswith('javascript:'):
                del el.attrs[a]
    html_body = str(soup)
    md_text = md(html_body, heading_style='ATX')

    out = []
    out.append('+++')
    out.append(fm)
    out.append('+++')
    out.append('\n')
    out.append(md_text)
    out_text = '\n'.join(out)
    in_path.write_text(out_text, encoding='utf-8')
    print('Wrote markdown to', in_path)

    bundle_dir = in_path.parent
    removed = []
    for p in bundle_dir.iterdir():
        if p.is_file() and p.suffix.lower() in ('.js','.mjs'):
            try:
                p.unlink()
                removed.append(p.name)
            except Exception as e:
                print('Failed to remove',p, e, file=sys.stderr)
    if removed:
        print('Removed JS files:', ', '.join(removed))
    else:
        print('No JS files found to remove')

if __name__=='__main__':
    main()
