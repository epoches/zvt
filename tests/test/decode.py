import sys
import chardet
print(sys.maxunicode)
dic=b"\xe5\xb7\xb2\xe8\xb6\x85\xe8\xbf\x87\xe6\xaf\x8f\xe6\x97\xa5\xe6\x9c\x80\xe5\xa4\xa7\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x95\xb0\xe9\x87\x8f\n\xe6\xb7\xbb\xe5\x8a\xa0\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98\xe5\xbe\xae\xe4\xbf\xa1\xe5\x85\x8d\xe8\xb4\xb9\xe9\xa2\x86\xe5\x8f\x96\xe6\x9b\xb4\xe5\xa4\x9a\xe9\xa2\x9d\xe5\xba\xa6\xef\xbc\x9b\xe6\x88\x96\xe4\xbb\x98\xe8\xb4\xb9\xe5\x8d\x87\xe7\xba\xa7\xe5\x88\xb02\xe4\xba\xbf\xe6\x9d\xa1/\xe5\xa4\xa9\xef\xbc\x8c\xe8\xaf\xa6\xe6\x83\x85\xe8\xaf\xb7\xe5\x92\xa8\xe8\xaf\xa2\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98\xef\xbc\x8c\xe5\xbe\xae\xe4\xbf\xa1\xe5\x8f\xb7\xef\xbc\x9a'"
#print(decode(str,str1))
chardet.detect(dic)
ss = dic.decode("utf-8")
print(ss)