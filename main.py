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
import os
import jinja2
from google.appengine.ext import db
# set up jinja

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(BlogHandler):
    def get(self):
        self.render("mainpage.html")

class viewPostHandler(BlogHandler):
    def get(self,id):
        import pdb
        #pdb.set_trace()
        blog= writeblogtext.get_by_id(int(id))

        if not blog:
            self.response.write("There is no blog")

        self.render("permalink.html", blog=blog)

class writeblogtext(db.Model):
    title=db.StringProperty(required=True)
    blogtext=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    last_modified=db.DateTimeProperty(auto_now=True)

# Defined a class that displays the all the post listings on a separate page
class MainBlog(BlogHandler):
    def get(self):
        blogs=db.GqlQuery("select*from writeblogtext order by created desc limit 5")
    #    blogID=blogs.key().id()
        self.render("mainblog.html", blogs=blogs)#, blogID=blogID)



# Defines the new posts
class NewPost(BlogHandler):
    def writeform(self,title="",blogtext="",error=""):

        self.render("NewPost.html",title=title,
                                    blogtext=blogtext,
                                    error=error
                                    )

    def get(self):
        self.writeform()
    def post(self):
        title=self.request.get("title")
        blogtext=self.request.get("blogtext")

        if title and blogtext:

            a=writeblogtext(title=title,blogtext=blogtext)
            a.put()

            self.redirect("/blog" +"/" +str(a.key().id()))
        else:
            error="The text in the title or blog_text is not entered"
            self.writeform(title, blogtext,error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/blog", MainBlog),
    ("/blog/newpost",NewPost),
    webapp2.Route('/blog/<id:\d+>', viewPostHandler)
], debug=True)
