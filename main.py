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
    <table>
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input type="text" name="username" value="%(uservalue)s" value required>
                <span style="color: red">%(user-error)s</span>
                </td>
        </tr>
        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input type="password" name="password" value="" value required>
                <span style="color: red">%(password-error)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input type="password" name="verify" value="" value required>
                <span style="color: red">%(verify-error)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label form="email">Email (Optional)</label>
            </td>
            <td>
                <input type="text" name="email" value="%(emailvalue)s">
                <span style="color: red">%(email-error)s</span>
            </td>
        </tr>
    </table>
    <input type="submit">
</form>
"""

welcome_page = """
<h2>Welcome,
<span>%(username)s</span>!

</h2>
"""


content = page_header + username_form + page_footer
welcome = page_header + welcome_page + page_footer



class MainHandler(webapp2.RequestHandler):



    def write_form(self, usererror, passworderror, verifyerror, emailerror, username, email):
        self.response.out.write(content % {'user-error': usererror,
                                           'password-error': passworderror,
                                           'verify-error': verifyerror,
                                           'email-error': emailerror,
                                           'uservalue': username,
                                           'emailvalue': email })

    def get(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        usererror = ''
        passworderror = ''
        verifyerror = ''
        emailerror = ''

        self.write_form(usererror, passworderror, verifyerror, emailerror, username, email)

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
            verifyerror= 'Your passwords do not match'
            have_error = True
        if password == verify:
            verifyerror=''

        if not valid_email(email):
            emailerror='That is not a valid email.'
            have_error = True
        else:
            emailerror=''

        if have_error == True:
            self.write_form(usererror, passworderror, verifyerror, emailerror, username, email)

        if have_error == False:
            self.redirect('/welcome?username=' + username)


class Welcome(MainHandler):
    def welcome_writer(self, username):
        self.response.out.write(welcome_page % {'username': username})


    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.welcome_writer(username)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
