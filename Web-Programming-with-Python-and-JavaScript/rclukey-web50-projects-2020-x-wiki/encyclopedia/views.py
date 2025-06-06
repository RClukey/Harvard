from django.shortcuts import render
from django import forms
from markdown import Markdown
import random

from . import util

class NewTitleForm(forms.Form):
    title = forms.CharField(label="Title: ")
class NewContentForm(forms.Form):
    content = forms.CharField(label="Markdown Content: ")

def md_to_html(title):
    md = util.get_entry(title)
    markdowner = Markdown()
    if md == None:
        return None
    else:
        return markdowner.convert(md)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = md_to_html(title.lower())
    if html == None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })

def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        html = md_to_html(search_entry)

        if html is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": search_entry,
            "content": html
        })

        else:
            entries = util.list_entries()
            possible_entries = []
            for entry in entries:
                if  search_entry.lower() in entry.lower():
                    possible_entries.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "possible_entries": possible_entries
            })

def rand(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    html = md_to_html(entry)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": html
    })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        title = title.lower()

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new_error.html", {
                "title": title
            })
        else:
            util.save_entry(title, content)
            html = md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html
            })
            

def edit(request):
    if request.method == "POST":
        title = request.POST["entry_name"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        util.save_entry(title, content)
        html = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })