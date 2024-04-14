from django.shortcuts import render,redirect
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#To fulfill the requirements, we need to implement a view in
# `encyclopedia/views.py` that handles requests for individual
# encyclopedia entries.

def entry(request, title):

    # Get the content of the encyclopedia entry

    content = util.get_entry(title)

    # If the entry doesn't exist, raise a 404 error
    
    if content is None:
        raise Http404("Entry no found")
    
     # Render the entry page with the entry content

    return render(request, "encyclopedia/entry.html", {
                   "title":title,
                   "content": content
                  } )

# create a view to handle the search results in `encyclopedia/views.py

def search_results(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()

    # Find entries that contain the query as a substring
    results = [entry for entry in entries if query.lower() in entry.lower()]

    if len(results) == 1:
        # If there is only one result, redirect directly to that entry's page
        return HttpResponseRedirect(reverse('entry', args=[results[0]]))
    else:
        # Render search results page
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })


# Users can click "Create New Page" in the sidebar to go to the page where they can create a new encyclopedia entry.
# They can enter a title and content for the new page and click "Save Page". 
# If an entry with the provided title already exists, they'll see an error message,
# otherwise, the new entry will be saved, and they'll be redirected to the new entry's page.

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from . import util

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        existing_entries = util.list_entries()

        if not title or not content:
            return render(request, "encyclopedia/new_page.html", {
                "error_message": "Title and content cannot be empty.",
                "title": title,
                "content": content
            })

        if title in existing_entries:
            return render(request, "encyclopedia/new_page.html", {
                "error_message": "An encyclopedia entry with this title already exists.",
                "title": title,
                "content": content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
         return render(request, "encyclopedia/new_page.html")




#  This function retrieves the existing content of the entry with the given 
#  title using the `get_entry` function from `util.py`.
#  If the request method is POST, it saves the changes made to the entry's
#  content using the `save_entry` function and redirects the user back to the entry's page.
#  Otherwise, it renders the `edit_page.html` template with the existing content pre-populated in the textarea.

def edit_page(request, title):
    content = util.get_entry(title)
    
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

#Random list


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect(reverse("entry", args=[random_entry]))





    


    
    

