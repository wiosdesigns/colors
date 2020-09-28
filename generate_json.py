from colour import Color
import json

from mongoengine import *
connect("igcolors",host="localhost",port=27017,username="",password="")


standard_colors = {
  "#EF9A9A":"Light Red",
  "#F44336":"Red",
  "#B71C1C":"Dark Red",
  
  "#F48FB1":"Light Pink",
  "#E91E63":"Pink",
  "#880E4F":"Dark Pink",
  
  "#CE93D8":"Light Purple",
  "#9C27B0":"Purple",
  "#4A148C":"Dark Purple",
  
  "#B39DDB":"Light Deep Purple",
  "#673AB7":"Deep Purple",
  "#311B92":"Dark Deep Purple",
  
  "#9FA8DA":"Light Indigo",
  "#3F51B5":"Indigo",
  "#1A237E":"Dark Indigo",
  
  "#90CAF9":"Light Blue",
  "#2196F3":"Blue",
  "#0D47A1":"Dark Blue",
  
  "#81D4FA":"Light Sky Blue",
  "#03A9F4":"Sky Blue",
  "#01579B":"Dark Sky Blue",
  
  "#80DEEA":"Light Cyan",
  "#00BCD4":"Cyan",
  "#006064":"Dark Cyan",
  
  "#80CBC4":"Light Teal",
  "#009688":"Teal",
  "#004D40":"Dark Teal",
  
  "#A5D6A7":"Light Green",
  "#4CAF50":"Green",
  "#1B5E20":"Dark Green",
  
  "#E6EE9C":"Light Lime",
  "#CDDC39":"Lime",
  "#827717":"Dark Lime",
  
  "#FFF59D":"Light Yellow",
  "#FFEB3B":"Yellow",
  "#F57F17":"Dark Yellow",
  
  "#FFE082":"Light Amber",
  "#FFC107":"Amber",
  "#FF6F00":"Dark Amber",
  
  "#FFCC80":"Light Orange",
  "#FF9800":"Orange",
  "#E65100":"Dark Orange",
  
  "#FFAB91":"Light Deep Orange",
  "#FF5722":"Deep Orange",
  "#BF360C":"Dark Deep Orange",
  
  "#BCAAA4":"Light Brown",
  "#795548":"Brown",
  "#3E2723":"Dark Brown",
  
  "#EEEEEE":"Light Gray",
  "#9E9E9E":"Gray",
  "#424242":"Dark Gray",
  
  "#000000":"Black",
  "#ffffff":"White" 
}

def closest_color_name(color):
  color = Color("#"+color)
  min_colors = {}
  for key in standard_colors:
    s_color = Color(key)
    r_c, g_c, b_c = s_color.red,s_color.green,s_color.blue
    rd = (r_c - color.red) ** 2
    gd = (g_c - color.green) ** 2
    bd = (b_c - color.blue) ** 2
    min_colors[(rd + gd + bd)] = standard_colors[key]
  
  c = min(min_colors.keys())
  return min_colors[c]



class Post(Document):
  shortcode = StringField(unique=True)
  thumbnail = StringField()
  caption = StringField()
  colors = ListField(StringField())
  status = StringField(default="discovered")
  hashtag = StringField()
  meta = {
    'indexes': [
      'shortcode',
      'status',
      'hashtag'
    ]  
  }

i = 0 
rows = []
count = Post.objects(status="processed").count()
 
for post in Post.objects(status="processed"):
  i += 1
  if i%100==0:
    print(i)
  
  post.colors.sort(key=lambda color: Color("#"+color).luminance)
  rows.append({
    "id":i,
    "shortcode": post.shortcode,
    "caption": post.caption,
    "colors": post.colors,
    "colornames": [closest_color_name(c) for c in post.colors],
    "similars0": [],
    "similars1": [],
    "similars2": [],
    "similars3": [],
    "next":(i+1)%count,
    "prev":(i-1)%count
  })


for i in range(len(rows)):
  if i%100==0:
    print(i)
  sc = [0,0,0,0]
  for j in range(i+1,len(rows)):
    for k in range(0,4):
      if len(rows[i]['similars'+str(k)])<4 and rows[i]['colornames'][k] in rows[j]['colornames']:        
        rows[i]['similars'+str(k)].append({
          "id": rows[j]['id'],
          "colors": rows[j]['colors']
        })
        sc[k] += 1
    if sc[0]>3 and sc[1]>3 and sc[2]>3 and sc[3]>3:
      break    


open("data.json","w").write(json.dumps(rows,indent=2))    


