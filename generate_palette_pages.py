import json
from jinja2 import Template

import os
if not os.path.exists('public'):
    os.makedirs('public')


template = Template(open("palette_template.html").read())
rows = json.load(open("data.json"))



with open("public/index.html","w") as f:
  f.write(template.render(row=rows[0]))
  f.close()    

for row in rows:
  filename = "public/{}.html".format(row['id'])
  with open(filename,"w") as f:
    f.write(template.render(row=row))
    if row['id']%500==0:
      print(row['id'])
    f.close()  
 
    
