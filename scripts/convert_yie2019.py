#!/usr/bin/env python3
import io,os,re,sys
root='/Users/joshstark/0xstark'
html_path=os.path.join(root,'originals','yie2019.html')
if not os.path.exists(html_path):
    print('originals/yie2019.html not found',file=sys.stderr); sys.exit(1)
with open(html_path,'r',encoding='utf-8') as f:
    s=f.read()
start_token='<div class="css-72ne1l">'
start=s.find(start_token)
if start==-1:
    print('start token not found',file=sys.stderr); sys.exit(1)
# find balanced divs starting from start
idx=start
count=0
pattern=re.compile(r'<(/?)div\b',re.IGNORECASE)
for m in pattern.finditer(s,start):
    if m.group(1)=='':
        count+=1
    else:
        count-=1
    if count==0:
        end_pos = m.end()
        break
else:
    print('could not find matching closing div',file=sys.stderr); sys.exit(1)
article_html=s[start:end_pos]
# fix local asset paths
article_html=article_html.replace('./yie2019_files/','./')
# pick a cover image filename if present
m=re.search(r'<img[^>]+src=["\']?([^"\' >]+)',article_html)
cover=''
if m:
    cover=os.path.basename(m.group(1))
# prepare front matter
fm = []
fm.append('+++')
fm.append('title = "The Year in Ethereum 2019"')
fm.append('date = 2020-01-20T00:00:00')
fm.append('description = "The Year in Ethereum 2019"')
fm.append('tags = ["year-in-ethereum", "ethereum"]')
fm.append('draft = false')
if cover:
    fm.append('\n[params.cover]')
    fm.append(f'image = "{cover}"')
    fm.append('alt = "The Year in Ethereum 2019"')
    fm.append('caption = "The Year in Ethereum 2019"')
fm.append('+++\n')
content='\n'.join(fm)+article_html+"\n"
out_dir=os.path.join(root,'content','posts','YIE2019')
os.makedirs(out_dir,exist_ok=True)
out_path=os.path.join(out_dir,'index.md')
with open(out_path,'w',encoding='utf-8') as f:
    f.write(content)
print('Wrote',out_path)
# move assets directory if present
assets_src=os.path.join(root,'originals','yie2019_files')
if os.path.exists(assets_src):
    for name in os.listdir(assets_src):
        src=os.path.join(assets_src,name)
        dst=os.path.join(out_dir,name)
        try:
            os.replace(src,dst)
            print('moved',name)
        except Exception as e:
            print('failed moving',name, e,file=sys.stderr)
    try:
        os.rmdir(assets_src)
        print('removed',assets_src)
    except Exception:
        pass
else:
    print('assets folder not found; remember to copy originals/yie2019_files into',out_dir)
print('Done')
