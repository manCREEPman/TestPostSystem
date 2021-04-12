from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from  django.contrib import messages

from .decorators import unauthenicated_user

import re

from .models import (Test, TestTask, UserTest, UserTestTask)
from .forms import (TestForm, TestTaskForm)

def main_page(request):
    return render(request, 'main.html')

@staff_member_required
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

@staff_member_required
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

        max_points = 0
        if formset.is_valid():
            for form in formset.cleaned_data:
                points = form['points']
                if points <= 0:
                    points = 1
                max_points += points
                task = TestTask(
                    test_id=test,
                    type=form['type'],
                    title=form['title'],
                    task_statement=form['task_statement'],
                    correct_answer=form['correct_answer'],
                    points=points
                )
                task.save()
            test.max_points = max_points
            test.save()
        return redirect('/admin/')


@staff_member_required(redirect_field_name='error')
def list_unchecked_user_tests(request):
    # print('popali suda')
    queryset = UserTest.objects.select_related('test_id').filter(
        check_status=False
    )
    context = {}
    # print(queryset[0].test_id.title)
    # print(queryset[0].id)
    if len(queryset) == 0:
        context['notification'] = 'В данный момент нет заданий для проверки'
    context['queryset'] = queryset
    print(context)
    return render(request, 'unchecked_tests.html', context)


def update_user_test_information(user_test_id):
    if user_test_id != 0:
        user_test_tasks = UserTestTask.objects.select_related('user_test_id').filter(
            user_test_id__id=user_test_id,
            check_status=False
        )
        
        if len(user_test_tasks) == 0:
            UserTest.objects.filter(id=user_test_id).update(
                check_status=True
            )
        
        user_test_tasks = UserTestTask.objects.select_related('user_test_id').filter(
            user_test_id__id=user_test_id
        )
        sum_points = 0
        for utt in user_test_tasks:
            sum_points += utt.user_points
        UserTest.objects.filter(id=user_test_id).update(
                result_points=sum_points
        )


@staff_member_required
def check_user_test(request):
    if request.method == 'GET':
        user_test_id = int(re.findall(r'/\w+/(\d+)', request.path)[0])
        unchecked_tasks = UserTestTask.objects.select_related('user_test_id').filter(
            user_test_id__id=user_test_id,
            check_status=False,
            type='TE'
        )
        # print(unchecked_tasks[0].user_test_id)
        # print(unchecked_tasks[0].type)
        # print('user_test_id', unchecked_tasks[0].user_test_id.id)
        context = {}
        if len(unchecked_tasks) == 0:
            context['notification'] = 'В данный момент нет заданий для проверки'
            return render(request, 'unchecked_test_tasks.html', context)
        context['queryset'] = unchecked_tasks
        return render(request, 'unchecked_test_tasks.html', context)
    else:
        print(request.POST)
        user_test_id = 0
        for task in request.POST.keys():
            if task.find('task') != -1:
                user_task_id = re.findall(r'task-(\d+)', task)[0]
                user_task_points = int(request.POST[task])
                if user_task_points < 0:
                    user_task_points = 0
                print('points', user_task_points)
                print('user_task_id', user_task_id)
                user_task = UserTestTask.objects.filter(id=user_task_id)
                if user_task[0].points < user_task_points:
                    user_task_points = user_task[0].points
                UserTestTask.objects.filter(id=user_task_id).update(
                    check_status=True,
                    user_points=user_task_points
                )
                user_task = UserTestTask.objects.select_related('user_test_id').filter(
                    id=user_task_id)
                user_test_id = user_task[0].user_test_id.id
        update_user_test_information(user_test_id)
        return redirect('/user_unchecked_tests')


def pass_test(request):
    if request.method == 'GET':
        print(request.user.id)
        test_id = int(re.findall(r'/\w+/(\d+)', request.path)[0])
        if UserTest.objects.select_related('test_id', 'user_id').filter(
                test_id__id=test_id,
                user_id__id=request.user.id
            ).exists():
            queryset = UserTest.objects.select_related('test_id', 'user_id').filter(
                test_id__id=test_id,
                user_id__id=request.user.id
            )
            user_test = queryset[0]
            user_tasks = UserTestTask.objects.select_related('user_test_id').filter(
                user_test_id=user_test
            )
            context = {'user_tasks': user_tasks}
            return render(request, 'user_test_details.html', context)
        else:
            test = get_object_or_404(Test, id=test_id)
            test_tasks = TestTask.objects.select_related('test_id').filter(
                test_id=test
            )
            user_test = UserTest.objects.create(
                user_id=request.user,
                test_id=test,
                result_points=0,
                check_status=False
            )
            auto_questions = []
            handle_questions = []
            for test_task in test_tasks:
                new_user_task = UserTestTask.objects.create(
                    user_test_id=user_test,
                    type=test_task.type,
                    title=test_task.title,
                    task_statement=test_task.task_statement,
                    points=test_task.points,
                    correct_answer=test_task.correct_answer,
                    user_file=None,
                    user_points=0,
                    check_status=False
                )
                if test_task.type == 'TE':
                    handle_questions.append(new_user_task)
                else:
                    auto_questions.append(new_user_task)
            context = {'auto_questions': auto_questions, 'handle_questions': handle_questions}
            return render(request, 'user_test.html', context)
    else:
        print(request.POST)
        print(request.FILES)
        user_test_id = 0
        for question in request.POST.keys():
            if question.find('task') != -1:
                user_task_id = re.findall(r'auto-task-(\d+)', question)[0]
                user_task = get_object_or_404(UserTestTask, id=user_task_id)
                user_answer = request.POST[question]
                if user_task.correct_answer == user_answer:
                    user_task.user_points = user_task.points
                user_task.user_answer = user_answer
                user_task.check_status = True
                user_test_id = user_task.user_test_id.id
                user_task.save()
        
        for file_input in request.FILES.keys():
            user_task_id = re.findall(r'handle-task-(\d+)', file_input)[0]
            user_task = get_object_or_404(UserTestTask, id=user_task_id)
            user_task.user_file = request.FILES[file_input]
            user_test_id = user_task.user_test_id.id
            user_task.save()
        update_user_test_information(user_test_id)
        return redirect('tests/')


#@login_required(login_url='login')

@unauthenicated_user
def login_page(request):

    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/account/')
            # else:
            #     messages.info(request, 'Пароль или логин введены некорректно.')

    context={
    }
    return render(request,'SignUp.html',context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required(login_url='login')
def account_page(request):
    user_id = request.user.id
    user_tests = UserTest.objects.select_related('user_id', 'test_id').filter(
        user_id=user_id
    )

    context={
        'user_tests': user_tests
    }
    return  render(request,'AccountForm.html', context)


@login_required(login_url='login')
def tests_page(request):
    tests = Test.objects.all()
    context={'queryset': tests}
    return  render(request,'Tests.html', context)
