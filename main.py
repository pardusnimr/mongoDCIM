import webapp2
import os
import jinja2
from pymongo import MongoClient

template_path = os.path.join(os.path.dirname(__file__))

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))


def get_connection():
    c = MongoClient()
    dbh = c["dcim"]
    return dbh
    

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        conn = get_connection()
        
        rows = conn.devices.find()
        conn.connection.close()
        template_values = {"rows":rows}
        template = jinja2_env.get_template('index.html')
        self.response.out.write(template.render(template_values))
        

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()