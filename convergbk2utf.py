# -*- coding:utf-8 -*-
__author__ = 'tsbc'
 
import os,sys
import chardet

def checkcoding(path):
    with open(path, 'rb') as f:    
        result = chardet.detect(f.read())  
    print(result)
 

def convert( filename, outfilename, out_enc="UTF8" ):
    try:
        print ("convert " + filename)
        with open(filename, 'rb') as f:   
            content = f.read()
            result = chardet.detect(content)  
        coding = result.get('encoding')#获取encoding的值[编码格式]
        if coding != 'utf-8':#文件格式如果不是utf-8的时候，才进行转码
            new_content = content.decode(coding).encode(out_enc)
            open(outfilename, 'w').write(str(new_content))
            print (" done")
        else:
            print (coding)
    except IOError:
    # except:
        print (" error")
 
 
def explore(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            convert(path)
 
def main():
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            convert(path)
        elif os.path.isdir(path):
            explore(path)
 
if __name__ == "__main__":
    # main()
    checkcoding("D:/code/zhimacode/_gitlog/xuliang-zhima-ios.gitlog")
    convert("D:/code/zhimacode/_gitlog/xuliang-zhima-ios.gitlog","D:/code/zhimacode/_gitlog/xuliang-zhima-iosout.gitlog")
    