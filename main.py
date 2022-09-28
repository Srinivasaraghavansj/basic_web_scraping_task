'''
author: Srinivasa Raghavan
date: 28/09/2022
task: scrape required data from time.com and make a basic web server to return the data in the given json format
phone no: 9884924981
email: jyothishjithan@gmail.com
disclaimer: Please note that this program works specificially only on time.com featured and is not generic

Run this and VISIT: http://localhost:8080/getTimeStories
'''

### NO EXTERNAL LIBRARIES USED
from http.server import BaseHTTPRequestHandler, HTTPServer #For basic server to return data
from urllib.request import urlopen #To get the website time.com

url = "http://time.com" #target url
page = urlopen(url)
html = page.read().decode("utf-8")#getting full html as string
txt = '<ul class="featured-voices__list swipe-h">' #inspected the element in browser and found the tag name
start_index = html.find(txt) + len(txt) #searching for start position of tag
end_index = start_index+html[start_index:].find("</ul>")#searching for end position of tag
my_snippet = html[start_index:end_index]#slicing only the required div from the page
# print(my_snippet)
my_snippet = my_snippet.split('\n') #breaking string into list based on new line for easier processing

json_string = "" #not using JSON lib here to show algorithmic skills
tag = '<h3 class="featured-voices__list-item-headline display-block">'#inspected the element in browser and found the tag name of the featured items

# searches and adds the title and its href link to the json_string variable
for n,i in enumerate(my_snippet):
    if tag in i:
        json_string+=f'''{{
    "title": "{i.replace(tag,"").replace("</h3>","").strip()}",
    "link": "{"https://time.com"+my_snippet[n-1].replace('<a href="',"").replace('">"',"").strip()}"
}},\n'''
json_string = "[\n"+json_string[:-2]+"\n]" #removing last comma
json_string = json_string.replace("\n","<br>") #DO NOT DO THIS IDEALLY FOR API CALLS. Using HTML line break just to make it look better in the webpage display. Comment this line out for API calls.



#Creating a basic server using inbuilt library - common template, nothing special here
hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.path='getTimeStories'
        self.wfile.write(bytes("<html><head><title></title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(f"<p>{json_string}</p>", "utf-8")) #adding our json data to be displayed
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")