import re

with open('/tmp/logo_b64.txt', 'r') as f:
    b64_content = f.read().strip()

with open('templates/invoice.html', 'r') as f:
    html = f.read()

replacement = f'<img src="data:image/png;base64,{b64_content}" style="max-width: 150px; height: auto;" alt="Intimacy Tattoo Logo">'
html = html.replace('<div class="logo-placeholder">LOGO INTEL/PLACEHOLDER</div>', replacement)

with open('templates/invoice.html', 'w') as f:
    f.write(html)
