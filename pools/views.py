from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import question, choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
# Create your views here.
def index(request):  
    latest_question_list = question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("pools/index.html")
    context = {"latest_question_list" : latest_question_list}
    
    return HttpResponse(template.render(context,request))

def details(request, question_id):
    # return HttpResponse("You are looking at question : %s " % question_id)
    question_val = get_object_or_404(question, pk= question_id)
    return render(request, "pools/details.html", {"question": question_val})


def vote(request, question_id):
    question_val = get_object_or_404(question, pk=question_id)
    try:
        selected_choice = question_val.choice_set.get(pk=request.POST["choice"])
    except (KeyError, choice.DoesNotExist):
      
        return render(
            request,
            "pools/detail.html",
            {
                "question": question_val,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("pools:results", args=(question_val.id,)))
    
def results(request, question_id):
    question_val = get_object_or_404(question, pk=question_id)
    return render(request, "pools/results.html", {"question": question_val})