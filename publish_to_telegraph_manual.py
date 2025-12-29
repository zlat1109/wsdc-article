import re
import sys

try:
    from telegraph import Telegraph
except ImportError:
    print("Error: 'telegraph' library not found.")
    print("Please install it: pip install telegraph")
    sys.exit(1)

def parse_markdown_to_html(md_text):
    """
    Converts the specific Markdown format of the article to HTML suitable for Telegraph.
    """
    html = []
    lines = md_text.split('\n')
    
    in_table = False
    
    for line in lines:
        line = line.strip()
        
        # Headers
        if line.startswith('# '):
            html.append(f"<h3>{line[2:]}</h3>") # Telegraph H3 is big enough
        elif line.startswith('## '):
            html.append(f"<h4>{line[3:]}</h4>")
        elif line.startswith('### '):
            html.append(f"<h5>{line[4:]}</h5>")
            
        # Lists (numbered)
        elif re.match(r'^\d+\.\s+', line):
            content = re.sub(r'^\d+\.\s+', '', line)
            content = content.replace('**', '<b>').replace('**', '</b>')
            html.append(f"<p>{line.split('.')[0]}. {content}</p>") 
            
        # Tables
        elif line.startswith('|'):
            if not in_table:
                html.append("<table>")
                in_table = True
            
            if '---' in line: continue
            
            row = "<tr>"
            cells = [c.strip() for c in line.strip('|').split('|')]
            for cell in cells:
                cell_html = cell.replace('**', '<b>').replace('**', '</b>')
                row += f"<td>{cell_html}</td>"
            row += "</tr>"
            html.append(row)
            
        # Horizontal Rule
        elif line == '---':
            if in_table:
                html.append("</table>")
                in_table = False
            html.append("<hr>")
            
        # Normal Text
        elif line:
            if in_table:
                html.append("</table>")
                in_table = False
                
            content = line
            content = content.replace('**', '<b>').replace('**', '</b>')
            content = content.replace('*', '<i>').replace('*', '</i>')
            html.append(f"<p>{content}</p>")
            
        else:
            # Empty line
             if in_table:
                html.append("</table>")
                in_table = False
    
    if in_table:
        html.append("</table>")
        
    return "".join(html)

def main():
    print("Reading publication_draft.txt...")
    try:
        with open('publication_draft.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: publication_draft.txt not found. Run this in the same folder.")
        return

    # Extract Telegram Post and Article
    try:
        tg_draft = content.split('=== TELEGRAM POST DRAFT ===')[1].split('=== TELEGRA.PH ARTICLE CONTENT (Markdown) ===')[0].strip()
        article_draft = content.split('=== TELEGRA.PH ARTICLE CONTENT (Markdown) ===')[1].strip()
        
        # Parse Title and Body
        article_lines = article_draft.split('\n')
        title = "WSDC 2025 Events Analysis" # Default
        author = "WSDC Analytics"
        
        body_start_idx = 0
        for i, line in enumerate(article_lines):
            if line.startswith('Title: '):
                title = line.replace('Title: ', '').strip()
            elif line.startswith('Author: '):
                author = line.replace('Author: ', '').strip()
            elif line.strip() == '':
                continue
            else:
                body_start_idx = i
                break
        
        body_md = "\n".join(article_lines[body_start_idx:])
        html_content = parse_markdown_to_html(body_md)
        
    except IndexError:
        print("Error: Could not parse draft file structure.")
        return

    print(f"Publishing article: '{title}'...")
    
    # Initialize Telegraph
    telegraph = Telegraph()
    telegraph.create_account(short_name='WSDC_Stats')
    
    response = telegraph.create_page(
        title=title,
        html_content=html_content,
        author_name=author
    )
    
    url = response['url']
    print(f"\n✅ SUCCESS! Article Published: {url}")
    
    print("\n" + "="*50)
    print("FINAL TELEGRAM POST (Copy this):")
    print("="*50)
    
    final_post = tg_draft.replace('[Ссылка]', url)
    print(final_post)
    print("="*50)

if __name__ == "__main__":
    main()

