
# Formatchecklist as HTML
def format_email_checklist(checklist_title: str, items: str):
    title = f'{checklist_title}:'
    
    html_message = f"""
    <html>
    <body>
        <h1>{ title }</h1>
        <ul>\n"""
    
    for item in items.all():
        if item.done:
            html_message += f'<li><s>{item.text}</s></li>\n'
        else:
            html_message += f'<li>{item.text}</li>\n'
    
    html_message += """\
        </ul>\n
        </body>\n
        </html>"""
        
    return html_message