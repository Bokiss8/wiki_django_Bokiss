from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import random


new_list = []
spisok = util.list_entries()
#----------------------------------------------------------------------------------------
def index(request):
    #print("spisok otrabotal")
    return render(request, "encyclopedia/index.html", {
        "entries": spisok
    })
#----------------------------------------------------------------------------------------
def wpages(request, title):
    print(f"request={request.path}")
    print(f"title={title}")
    return render(request, "encyclopedia/pages.html", {
        #"title": title.capitalize(),
        "title": title,
        "vmist": markdown2.markdown(util.get_entry(title)),
        "kysok_search_rezult": new_list
    })
#----------------------------------------------------------------------------------------
def poisk(request):
    #print(f"request={request}")
    search_query = request.GET.get('q','')
    #print(f"poisk = {search_query}")
    #print(f"utillistentries={util.list_entries()}")
    #chek = (search_query in util.list_entries())
    #print(f"trueorFalse={chek}")
    #print(f"utillistentries={util.list_entries()[1]}")
    #print(f"utilgetentry={util.get_entry(search_query)}")
    if util.get_entry(search_query) is not None:
   # це також працює але враховує регістр букв if (search_query in util.list_entries()) == True:
        return HttpResponseRedirect(reverse("wiki:wpages", args=(search_query,)))
        #context = { 
         #   "title": search_query.capitalize(),
          #  "rezsearch": markdown2.markdown(util.get_entry(search_query))    }
        #return render(request, "encyclopedia/search.html", context = context)
    else:
        # шукаємо співпадіння нашого запиту по буквах чи словосполученнях 
        # які є в елементах нашого списку 
        kysok = search_query
        spisok = util.list_entries()
        #new_list = []
        new_list.clear()
        for text in spisok:
            if kysok != '' and kysok in text:
                    new_list.append(text)
        print(f"kysok={kysok}")
        print(f"spisok={spisok}")
        print(f"newl_ist={new_list}")
        if not new_list:
            print("pysto")
            context = {
                       "title": str("Sorry"),
                       "Sorry": str("Sorry такої статті не існує!")
                       }
            return render(request, "encyclopedia/search.html", context = context)
        else:
             context = {
                       "title": str("Search rezult"),
                       "kysok_search_rezult": new_list
                       }
    #print(dir(request))
    #print(request.GET)
        return render(request, "encyclopedia/search.html", context = context)
#----------------------------------------------------------------------------------------
def createpage(request):
        if request.method == "POST":
            zak = request.POST
            #print(f"form={zak}")
            article = zak.get('article')
            zmist = zak.get('mark')
            #print(f"article={article}")
            #print(f"zmist={zmist}")
            if util.get_entry(article) is not None:
                return render(request, "encyclopedia/createpage.html", {
                "error": str("Заголовок такої статті вже існує!")
                })
            else:
                 spisok.append(article)
                 util.save_entry(article, zmist)
                 return HttpResponseRedirect(reverse("wiki:wpages", args=(article,)))

                 #return render(request, "encyclopedia/pages.html", {
                  #          "title": article.capitalize(),
                   #         "vmist": markdown2.markdown(util.get_entry(article)),
                    #        "kysok_search_rezult": new_list
                  #})
        else:
            return render(request, "encyclopedia/createpage.html", {
                "error": str("")
            })
#----------------------------------------------------------------------------------------
def correctpage(request, title):
            print(f"request={request.path}")
            print(f"title={title}")
            if util.get_entry(title) is not None:
                corzmist = util.get_entry(title)
                print(f"corzmist={corzmist}")
                return render(request, "encyclopedia/correctpage.html", {
                    "title": title,
                    "corzmist": corzmist
                })
            else:
                 return HttpResponseRedirect(reverse("wiki:index"))
#----------------------------------------------------------------------------------------
def correctpagesave(request):
        if request.method == "POST":
            zakcor = request.POST
            print(f"form={zakcor}")
            articlecor2 = zakcor.get('articlecor2')
            zmistcor = zakcor.get('markcor')
            print(f"articlecor2={articlecor2}")
            print(f"zmistcor={zmistcor}")
            if util.get_entry(articlecor2) is not None:
                util.save_entry(articlecor2, zmistcor)
                return HttpResponseRedirect(reverse("wiki:wpages", args=(articlecor2,)))
            else:
                return render(request, "encyclopedia/correctpage.html", {
                "error": str("Щось піщло не так!")
                })
        else:
            return render(request, "encyclopedia/createpage.html", {
                "error": str("")
            })
#----------------------------------------------------------------------------------------
def randompage(request):
    fromspisok = util.list_entries()
    randomelement = random.choice(fromspisok)
    print(f"fromspisok={fromspisok}")
    print(f"titlerandom={randomelement}")
    return HttpResponseRedirect(reverse("wiki:wpages", args=(randomelement,)))
#----------------------------------------------------------------------------------------
# проект готовий від Bokiss
