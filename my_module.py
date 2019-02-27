def file_as_string(file_path):
    buff=""
    file_to_read = open(file_path,'r')
    
    while True:
        line = file_to_read.readline()
        if line == "":
            break
        buff+=line
    
    file_to_read.close()
    return buff

def save_to_file(file_path, content):
    
    file_to_save = open(file_path,'w')
    file_to_save.write(content)
    file_to_save.close()

def buildwebpage(content,title="My page"):
    base_html = file_as_string("base.html")
    
    return base_html.format(title,content)
    
