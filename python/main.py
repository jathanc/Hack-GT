import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.api import images
from models import User
from models import Interest
from models import Image
import os.path

jinja_current_directory = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

# gets current logged-in user
# so it is easy to access their data on each new page
# request_handler is key for self, but since this method isn't in a class
# that makes it very hard to call self xD
def get_logged_in_user(request_handler):
    # gets current user via a method defined in google app engine
    user = users.get_current_user()

    # if this user doesn't exist (aka no one is signed into Google)
    if not user:
        # send them to Google log-in url
        dict = {
            'log_in_url' : users.create_login_url('/')
        }
        # put that Google log-in link on the page and get them in!
        log_in_template = jinja_current_directory.get_template('templates/login-page.html')
        request_handler.response.write(log_in_template.render(dict))
        print 'transaction halted because user is not logged in'
        return None

    # at this point, the user is logged into google
    # now let's make sure that user has been logged into our site
    # aka do we have their Google ID in OUR model (which is called User)?
    # user (appengine) vs User (our own Model). Definitely not confusing
    existing_user = User.get_by_id(user.user_id())

    # if this person is not a user in our database, throw an error
    if not existing_user:
        print 'transaction halted because user not in database'
        request_handler.error(500)
        return None

    # otherwise if they exist in both Google and our site, let's return them
    # now we can easily access their information
    return existing_user
