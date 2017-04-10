#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re



def valid_username(username):
    return username and re.compile(r"^[a-zA-Z0-9_-]{3,20}$").match(username)

def valid_password(password):
    return password and re.compile(r"^.{3,20}$").match(password)

def valid_email(email):
    return not email or re.compile(r"^[\S]+@[\S]+.[\S]+$").match(email)




page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
<body>
    <h1>User Signup</h1>
"""

page_footer = """
</body>
</html>
"""

username_form = """
<form action="/" method="post">
    <label>Username</label>
    <input type="text" name="username" value="" value required>
    <span style="color: red">%(user-error)s</span>
    <br>

    <label>Password</label>
    <input type="text" name="password" value="" value required>
    <span style="color: red">%(password-error)s</span><br>

    <label>Verify Password</label>
    <input type="text" name="verify" value="" value required>
    <span style="color: red">%(verify-error)s</span><br>

    <label>Email (Optional)</label>
    <input type="text" name="email" value="">
    <span style="color: red">%(email-error)s</span><br>

    <input type="submit">
</form>
"""

welcome_page = """
<h2>Welcome, user!<h2>

"""

content = page_header + username_form + page_footer
welcome = page_header + welcome_page + page_footer



class MainHandler(webapp2.RequestHandler):
    def write_form(self, usererror, passworderror, verifyerror, emailerror):
        self.response.out.write(content % {'user-error': usererror,
                                            'password-error': passworderror,
                                           'verify-error': verifyerror,
                                           'email-error': emailerror })

    def get(self):

        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')




        if not valid_username(username):
            usererror=('That is not a valid user name.')
            have_error = True
        if valid_username(username):
            usererror=''

        if not valid_password(password):
            passworderror='That is not a valid password.'
            have_error = True
        if valid_password(password):
            passworderror=''

        if password != verify:
            if not valid_username(username):
                verifyerror='Your passwords do not match.'
                have_error = True
        else:
            verifyerror=''

        if not valid_email(email):
            emailerror='That is not a valid email.'
            have_error = True

        else:
            emailerror=''

        #lst = [usererror, passworderror, verifyerror, emailerror]

        self.write_form(usererror, passworderror, verifyerror, emailerror)

class Welcome(MainHandler):

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(welcome)
        else:
            self.redirect('/')




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
