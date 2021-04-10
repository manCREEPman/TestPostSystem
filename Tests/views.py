from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
import json

from .models import (Test, TestTask, UserTest, UserTestTask)
from .forms import (TestForm, TestTaskForm)

def create_test(request):
    if request.method == 'GET':
        return render(request, 'create_test.html')
    if request.method == 'POST':
        try:
            number_of_tasks = int(request.POST.get('number_of_tasks'))
        except:
            number_of_tasks = 1
        if number_of_tasks <= 0:
            number_of_tasks = 1
        test_title = request.POST.get('test_title')
        test_picture = request.FILES['test_picture']
        test = Test.objects.create(title=test_title, picture=test_picture)
        test.save()
        created_test_id = test.id
        return redirect(
            '/create_tasks?id={}&number_of_tasks={}'.format(
                created_test_id, number_of_tasks
                )
            )


def create_tasks(request):
    if request.method == 'GET':
        test_id = request.GET['id']
        number_of_tasks = int(request.GET['number_of_tasks'])
        tasks_forms = modelformset_factory(TestTask, TestTaskForm, extra=number_of_tasks)
        context = {
            'test_title': Test.objects.get(id=test_id).title,
            'test_id': test_id,
            'tasks_forms': tasks_forms
        }
        return render(request, 'create_tasks.html', context)
    if request.method == 'POST':
        test_id = int(request.GET.get('test_id'))
        test = get_object_or_404(Test, id=test_id)
        TestTaskFormSet = modelformset_factory(TestTask, form=TestTaskForm)
        formset = TestTaskFormSet(request.POST)

        if formset.is_valid():
            for form in formset.cleaned_data:
                points = form['points']
                if points <= 0:
                    points = 1
                task = TestTask(
                    test_id=test,
                    type=form['type'],
                    title=form['title'],
                    task_statement=form['task_statement'],
                    correct_answer=form['correct_answer'],
                    points=points
                )
                task.save()
        return redirect('/admin/')

        


def sample(request):
    if request.method == 'GET':
        return render(request, 'create_test.html')
    else:
        # print(request.POST)
        # for filename, file in request.FILES.items():
        #     print(request.FILES[filename].name)
        # return render(request, 'base.html')
        print(request.FILES["file_field"])
        file_image = request.POST.get('test_picture')
        request.session['file_image'] = file_image
        context = {'image': request.FILES["file_field"]}
        return render(request, 'base.html', context)

        test_form = TestForm(data=request.POST)
        if test_form.is_valid():
            test_form.save(commit=False)
        return HttpResponseRedirect('admin')

    #     postForm = PostForm(request.POST)
    #     formset = ImageFormSet(request.POST, request.FILES,
    #                            queryset=Images.objects.none())
    
    
    #     if postForm.is_valid() and formset.is_valid():
    #         post_form = postForm.save(commit=False)
    #         post_form.user = request.user
    #         post_form.save()
    
    #         for form in formset.cleaned_data:
    #             #this helps to not crash if the user   
    #             #do not upload all the photos
    #             if form:
    #                 image = form['image']
    #                 photo = Images(post=post_form, image=image)
    #                 photo.save()
    #         # use django messages framework
    #         messages.success(request,
    #                          "Yeeew, check it out on the home page!")
    #         return HttpResponseRedirect("/")
    #     else:
    #         print(postForm.errors, formset.errors)
    # else:
    #     postForm = PostForm()
    #     formset = ImageFormSet(queryset=Images.objects.none())
    # return render(request, 'index.html',
    #               {'postForm': postForm, 'formset': formset})

