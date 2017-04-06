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

class MainHandler(webapp2.RequestHandler):
    def get(self):

        username_form = """
        <form action="/" method="post">
            <label>Username</label>
            <input type="text" name="user-name"><br>

            <label>Password</label>
            <input type="text" name="password"><br>

            <label>Verify Password</label>
            <input type="text" name="verify-password"><br>

            <label>Email (Optional)</label>
            <input type="text" name="email"><br>

            <input type="submit">
        </form>
        """
        content = page_header + username_form + page_footer

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
