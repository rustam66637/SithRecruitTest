from django.forms import formset_factory
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import View
from .models import Recruit, Sith, Question, Planet, ResultTest
from .forms import RecruitForm, RecruitQuestionsForm, SithChoiceForm, RecruitChoiceForm
from django.shortcuts import redirect
from django.core.mail import send_mail


class HomeView(View):
    """Обработка главной страницы"""
    def get(self, request):
        return render(request, 'workTest/index.html')


class RecruitView(View):
    """Обработчик формы для рекрута"""
    def get(self, request):
        form = RecruitForm
        return render(request, 'workTest/recruit.html', context={
            'form': form,
        })

    def post(self, request):
        # Создается связанная форма, передается QueryDict
        bound_form = RecruitForm(request.POST)
        # Проверка на валидность формы
        if bound_form.is_valid():
            # Сохраняем нового рекрута
            new_recruit = bound_form.save()

            # Редиректим рекрута на тест
            base_url = reverse('RecruitQuestions_url') # recruitquestions/
            query_string = urlencode({'recruit': new_recruit.id})  # id рекрута в url
            url = '{}?{}'.format(base_url, query_string)  # recruitquestions/?recruit=id

            return redirect(url)
        else:
            return render(request, 'workTest/recruit.html', context={
                'form': bound_form,
            })


class RecruitQuestions(View):
    """Обработчик формы для теста"""
    def get(self, request):
        # Queryset с вопросами
        questions = Question.objects.filter(active=True)
        recruit = None
        # Если находим рекрута в get запросе - достаем объект-рекрут
        if 'recruit' in request.GET.keys():
            recruit = Recruit.objects.get(pk=request.GET['recruit'])
        # Иначе редиректим на форму рекрута
        if not recruit:
            return redirect('RecruitView_url')

        QuestionFormSet = formset_factory(RecruitQuestionsForm, min_num=len(questions),
                                          max_num=len(questions), extra=len(questions))
        formset = QuestionFormSet(initial=[{'question': q, 'recruit': recruit} for q in questions])

        return render(request, 'workTest/test.html', context={
            'formset': formset
        })

    def post(self, request):
        QuestionFormSet = formset_factory(RecruitQuestionsForm)

        formset = QuestionFormSet(request.POST)
        # Если форма валидна - сохраняем
        if formset.is_valid():
            for form in formset:
                form.save()

            return redirect('HomeView_url')
        # Иначе редиректим на ту же форму
        else:
            base_url = reverse('RecruitQuestions_url')  # recruitquestions/
            query_string = urlencode({'recruit': request.POST['form-0-recruit']})
            url = '{}?{}'.format(base_url, query_string)  # recruitquestions/?recruit=id
            return redirect(url)


class SithView(View):
    """Обработчик формы для Ситха"""
    def get(self, request):
        form = SithChoiceForm
        return render(request, 'workTest/sith.html', context={
            'form': form,
        })

    def post(self, request):
        # Редиректим на выбор рекрута
        base_url = reverse('RecruitChoiceView_url')  # chooserecruit/
        query_string = urlencode({'sith': request.POST['sith']})  # id Ситха
        url = '{}?{}'.format(base_url, query_string)  # chooserecruit?sith=id
        return redirect(url)


class RecruitChoiceView(View):
    """Обработчик выбора рекрута"""
    def get(self, request):
        sith = None
        if 'sith' in request.GET.keys():
            sith = Sith.objects.get(pk=request.GET['sith'])
        if not sith:
            return redirect('SithView_url')

        form = RecruitChoiceForm(query=Recruit.objects.filter(planet=sith.planet, reviewed=False),
                                 initial={'sith': sith.pk})

        return render(request, 'workTest/sith.html', context={
            'form': form,
        })

    def post(self, request):
        base_url = reverse('AssessView_url')  # assess/
        query_string = urlencode({'sith': request.POST['sith'], 'recruit': request.POST['recruit']})
        url = '{}?{}'.format(base_url, query_string)  # assess/?sith=id&recruit=id

        return redirect(url)


class AssessView(View):
    """Обработчик оценивания результатов теста"""
    def get(self, request):
        sith = None
        recruit = None
        if 'sith' in request.GET.keys() and 'recruit' in request.GET.keys():
            sith = Sith.objects.get(pk=request.GET['sith'])
            recruit = Recruit.objects.get(pk=request.GET['recruit'])
        if not sith or not recruit:
            return redirect('SithView_url')

        answer = ResultTest.objects.filter(recruit=recruit)
        return render(request, 'workTest/assess.html', context={
            'answers': answer,
            'recruit': recruit,
            'sith': sith,
        })


class ResultTestView(View):
    """Обработчик результата теста"""
    def post(self, request):
        sith = None
        recruit = None
        if 'sith' in request.POST.keys() and 'recruit' in request.POST.keys():
            sith = Sith.objects.get(pk=request.POST['sith'])
            recruit = Recruit.objects.get(pk=request.POST['recruit'])
        if not sith or not recruit:
            return redirect('SithView_url')

        if request.POST.get('result') == '0':
            message = 'Ученик не принят!'
        elif Recruit.objects.filter(hand_shadow=sith).count() >= 3:
            message = 'У вас уже 3 ученика, отказано!'
        else:
            message = 'Ученик принят'
            recruit.hand_shadow = sith
            email(message, recruit)

        recruit.reviewed = True
        recruit.save()

        return render(request, 'workTest/response.html', context={
            'message': message,
        })


def email(message, recruit):
    """Отправка письма"""
    send_mail(subject='Поступление', message=message, from_email='sidiousdarthdarth@yandex.ru',
              recipient_list=[recruit.email], fail_silently=False)
