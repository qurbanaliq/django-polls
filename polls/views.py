from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    #result = ", ".join([question.question_text for question in latest_questions])
    template = loader.get_template("polls/index.html")
    context = {"latest_questions": latest_questions}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist")
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = Choice.objects.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question,
        "error_message": "You didn't select a choice"})
    # alwasys return HttpResponseRedirect after successfully dealing with
    # post data, this prevents data from being posted twice if user hits
    # back button
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    return HttpResponse("You are voting on question %s"%question_id)
