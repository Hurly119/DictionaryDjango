from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Definitions,Words,Sentences
from django.contrib import messages
from django.utils.safestring import mark_safe
import re


# Create your views here.

def index(request):
    AllWordObjects = Words.objects.all();
    AllWords = list(Words.objects.values_list("word",flat=True))
    AllWordsID = list(Words.objects.values_list("id",flat=True))
    AllDefinitions = list(Definitions.objects.values_list("definition",flat=True))
    AllSentences = list(Sentences.objects.values_list("sentence",flat=True))


    for index,DefSent in enumerate(zip(AllDefinitions,AllSentences)):
        definition = DefSent[0]
        sentence = DefSent[1]
        for word in AllWords:
            url = reverse("viewWord", args=(AllWordsID[index],))
            pattern = re.compile(rf"({word})",re.IGNORECASE);
            sentence = (re.sub(pattern, (f"<a href={url}>{word}</a>"),sentence))
            definition = (re.sub(pattern, (f"<a href={url}>{word}</a>"),definition))
        AllDefinitions[index] = (definition)
        AllSentences[index] = (sentence)

    ModifiedWordObject = zip(AllWordsID,AllWords,AllDefinitions,AllSentences)
    context = {
        # "Words": Words.objects.all()
        "Words": (ModifiedWordObject)
    }
    return render(request, "sitefordictionary/home.html",context)

def viewWord(request,wordID):
    word = Words.objects.get(pk=wordID)
    context = {
    "Word": word
    }
    return render(request,"sitefordictionary/viewWord.html",context)

def addWords(request):
    if(request.method == "POST"):
        word = request.POST["word"].strip()
        definition = request.POST["definition"]
        sentence = request.POST["sentence"].strip()
        if(word and definition and sentence):
            newSentenceObject = Sentences(sentence=sentence)
            newSentenceObject.save()

            newDefinitionObject = Definitions(definition=definition,dictionarySentence=newSentenceObject)
            newDefinitionObject.save()
            newWordObject = Words(word=word)
            newWordObject.save()
            newWordObject.dictionaryDefinition.add(newDefinitionObject)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO,"Field(s) not filled.")
            return HttpResponseRedirect(reverse("addWords"))
    return render(request, "sitefordictionary/addWords.html")
