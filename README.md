# md2html

A small tool to render Markdown documents into styled HTML.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Use

```bash
python3 render_md.py /path/to/doc.md
```

Output defaults to the same name with `.html`.

### Options

```bash
python3 render_md.py /path/to/doc.md \
  --title "AIR宠物用户服务协议" \
  --template template.html \
  --output /path/to/output.html
```

## Template

`template.html` contains a clean, print-friendly layout. You can edit the styles to match your brand.
