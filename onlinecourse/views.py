from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    if request.method == 'POST':
        selected_choices = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choices.append(int(value))
        
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_choices:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    
    total_score = 0
    questions = course.question_set.all()
    selected_ids = [c.id for c in selected_choices]

    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context['course'] = course
    context['grade'] = total_score
    context['submission'] = submission
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
