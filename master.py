import dummy
import SocketServer
import time
import BaseHTTPServer

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        output=[]
        a,searchTerm=s.path.split('/')
        #print searchTerm
        searchString=s.path.split('=')
        #print searchString
        if len(searchString)>1:
            searchTerm=''.join(searchString[1])
            #print searchTerm
        searchTerm=searchTerm.lower()
        dummy.listFiles(searchTerm,output)
        #print output
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>QMUL Search Engine</title>")
        s.wfile.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"mystyle.css\">")
        s.wfile.write("</head>")
        s.wfile.write("<body><p></p>")
        sout=','.join(output)
        html=''
        #print sout
        html=s.html_table(sout,searchTerm)
        #print html
        s.wfile.write("%s" % html)
        s.wfile.write("</body></html>")

    def html_table(s,output,searchTerm):
        markup='<form class="form-wrapper cf"><input type="text" name="search" placeholder="Search here..." required><button type="submit">Search</button></form>'
        markup+='<div class="container">    <hgroup class="mb20">        <h1>Search Results</h1>        <h2 class="lead"><strong class="text-danger">'
        splitlist=output.split(",")
        markup+=str(len(splitlist))
        markup+='</strong> results were found for the search for <strong class="text-danger">'
        markup+=searchTerm
        markup+='</strong></h2></hgroup>'
        #splitlist=output.split(",")
        #print splitlist
        for sublist in splitlist:
            #print sublist
            #print 'data/'+ ''.join(sublist) +'.json'
            fh=open('data/'+ ''.join(sublist) +'.json',"r")
            for line in fh:
                #print line
                if (line.lower().startswith("url".lower())):
                    url=''.join(line.split()[1])
                if (line.lower().startswith("category".lower())):
                    category=line
                if (line.lower().startswith("description".lower())):
                    description=''.join(line.split(':')[1])
            #print url
            #print category
            #print description
            fh.close()
            markup+='<section class="col-xs-12 col-sm-6 col-md-12"> <article class="search-result row">'
            markup+='<div class="col-xs-12 col-sm-12 col-md-7 excerpet"><h3><a href="'
            markup+=url
            markup+='" title="">'
            markup+=searchTerm
            markup+='</a></h3><p>'
            markup+=description
            markup+='</p>'                     
            markup+='</h3><p><strong>'
            markup+=category
            markup+='</strong></p>'                     
        markup+='</section></div>'
        return markup

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

