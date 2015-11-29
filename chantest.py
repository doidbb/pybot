url = "http://boards.4chan.org/sci/thread/7583059#p7583168"
newsplit = url.split("boards.4chan.org")
#print(newsplit)
if len(newsplit) > 1:
	maybesplit = url.split("#")
	if len(maybesplit) > 1:
		url = maybesplit[0]
	print(url.split("#"))
	newsplit   = url.split("/")
	print(newsplit)
    #print(newsplit[5])
	chanURL    = "https://a.4cdn.org/"+newsplit[3]+"/thread/"+newsplit[5]+".json"
print(chanURL)
