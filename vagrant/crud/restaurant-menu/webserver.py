from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# Import database methods
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Set up database connection
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = self.get_restaurants()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output = ""
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "<br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "<br>"
                    output += "<br>"
                    output += "<br>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Make a New Restaurant</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='newRestaurantName' type='text' placeholder='New Restaurant Name'><input type='submit' value='Create'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                restaurant = self.get_restaurant(restaurant_id)
                if restaurant:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><input name='newRestaurantName' type='text' placeholder='%s'><input type='submit' value='Rename'> </form>" % (restaurant.id, restaurant.name)
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)
                    return
            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                restaurant = self.get_restaurant(restaurant_id)
                if restaurant:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><input type='submit' value='Delete'></form>" % restaurant.id
                    output += "</body></html>"
                    self.wfile.write(output)
                    print(output)
                    return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    self.new_restaurant(messagecontent[0])

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurant_id = self.path.split("/")[2]

                    # Retrieve and edit restaurant object
                    restaurant = self.get_restaurant(restaurant_id)
                    if restaurant:
                        restaurant.name = messagecontent[0]
                        session.add(restaurant)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurant_id = self.path.split("/")[2]

                    # Retrieve and edit restaurant object
                    restaurant = self.get_restaurant(restaurant_id)
                    if restaurant:
                        session.delete(restaurant)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

    def get_restaurants(self):
        return session.query(Restaurant).all()

    def new_restaurant(self, name):
        restaurant = Restaurant(name=name)
        session.add(restaurant)
        session.commit()

    def get_restaurant(self, id):
        return session.query(Restaurant).filter_by(id=id).one()


def main():
    try:
        port = 8080
        server = HTTPServer(("", port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == "__main__":
    main()
