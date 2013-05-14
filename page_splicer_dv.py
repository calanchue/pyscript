# -*- coding:utf-8 -*-
'''
Created on 2013. 4. 30.

@author: Hwang-JinHwan

parsing the txt file which are generated by coping the pdf nova praxis rpg rule book 
to create bootstrap document
'''
import re
import codecs

template = """
<head>
    <style type="text/css">
        body {{
          padding-top: 60px;
          padding-bottom: 40px;
        }}
      </style>

    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">
</head>
<body>
<div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
      <div class="container">
        
          <ul class="nav">
            {nav_content}
          </ul>
        
      </div>
    </div>
 </div> 
<div class='container'>
<div class="row">
    {body_content}
</div>
</div>
<script src="//code.jquery.com/jquery-1.4.2.min.js"></script> 
<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>
</body>
"""

"""
<li class="dropdown">
  <a data-toggle="dropdown" class="dropdown-toggle" href="#">Dropdown <b class="caret"></b></a>
  <ul class="dropdown-menu">
    <li>
        <a href="#">2-level Dropdown <i class="icon-arrow-right"></i></a>
        <ul class="dropdown-menu sub-menu">
            <li><a href="#">Action</a></li>
            <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li class="divider"></li>
            <li class="nav-header">Nav header</li>
            <li><a href="#">Separated link</a></li>
            <li><a href="#">One more separated link</a></li>
        </ul>
    </li>
    <li><a href="#">Another action</a></li>
    <li><a href="#">Something else here</a></li>
    <li class="divider"></li>
    <li class="nav-header">Nav header</li>
    <li><a href="#">Separated link</a></li>
    <li><a href="#">One more separated link</a></li>
  </ul>
</li>

"""


nav_template ="""
<li class="dropdown">
  <a data-toggle="dropdown" class="dropdown-toggle" href="#">Dropdown <b class="caret"></b></a>
  <ul class="dropdown-menu">
    {drop_down_content}
    <li>
        <a href="#">Link</a>
    </li>
    <li class="active">
        <a href="#">Link</a>
    </li>
    <li class="divider"></li>
    <li>
        <a href="#">Link</a>
    </li>
    </ul>
</li>
"""
indexed_title = []
 

def resolve_index_line(line):
    def resolve(matchObj):
        title = matchObj.group(1)
        indexed_title.append(title.lower())
        dot = matchObj.group(2)
        page_num = matchObj.group(3)
        return ur'<a href="#%s">%s</a>%s<a href="#p%s">%s</a><br>'%(title.lower(), title, dot, page_num.lower(), page_num)
        
    return re.sub(ur'(\w.*?)\s*(\.{2,})\s*(\d+)', resolve, line, re.M | re.I)
     

curr_searching_title = 0
def resovle_title_line(line):
    global curr_searching_title
    if curr_searching_title < indexed_title.__len__() and line.rstrip().lower() == indexed_title[curr_searching_title]:
        curr_searching_title+=1
        level = 3
        if line.startswith("CHAPTER") :
            level = 1
        return '<h{level}><a name="{anchor}"></a>{text}</h{level}>\n'.format(anchor=line.rstrip().lower(), text=line.rstrip(), level=level)
    else:
        return line
        
    """if line.isupper() : 
        if re.match("^[A-Z]([A-Z0-9]|\s){3,}$", line, re.M):
            titles.append(line.rstrip())
            return '<h3><a name="%s"></a>%s</h3>\n' % (line.rstrip(), line.rstrip())"""

def resolve_normal_line(line):
    sub_line = re.sub(ur'(pg. |page )(\d+)', ur'<a href="#p\2">\g<0></a>', line, re.M | re.I)
    if line != sub_line:
        print line,
        print sub_line,
    sub_line = "<p>%s</p>\n" % sub_line.rstrip()
    return sub_line
        
def get_nav_content():    
    drop_down_content = []
    for title in indexed_title:
        drop_down_content.append('<li><a href="#%s">%s</a></li>\n' % (title, title))
    return nav_template.format(drop_down_content="".join(drop_down_content))

if __name__ == '__main__':
    # fr = open("resource/bar_test.txt", 'r')
    fr = open("resource/dogs in vineyard.txt", 'r')
    
    lines = fr.readlines()
    
    toc_page_num = 5
    
    prev_page_num = 5
    
    body_content = []
    buffered = []
    for line in lines:
        if(prev_page_num+1 <= toc_page_num):
            ret = resolve_index_line(line)
            if ret != line:
                buffered.append(ret)
                continue
        elif(prev_page_num+1 >toc_page_num):
            ret = resovle_title_line(line)
            if ret != line:
                buffered.append(ret)
                continue
            
        # data = fr.read()
        matchObj = re.search(ur'(^\d+|\d+$)', line, re.M | re.I)
        if matchObj:
            page_num = int(matchObj.group(1))
            if page_num < prev_page_num or page_num > prev_page_num + 2:
                line = resolve_normal_line(line)
                buffered.append(line)
                continue
            matched_tail = matchObj.group()
            print "#MATCH:", matched_tail
            buffered.append(matched_tail + "<br>\n")
            buffered.insert(0, '<div class="well">')
            buffered.append(r'</div>')
            buffered.insert(0, '<a name="p%s"></a>' % page_num)
            
            body_content.append("".join(buffered))
            
            buffered = []
            buffered.append(line[len(matched_tail):])
            prev_page_num = page_num
        else:
            line = resolve_normal_line(line)
            buffered.append(line)
            
    fw = codecs.open("resource/dogs in the vineyard.html", 'w', encoding='utf-8')
    body_content.append("".join(buffered))
    fw.write(template.format(body_content="".join(body_content), nav_content=get_nav_content()))
    
    
    fr.close() 
    fw.close()
