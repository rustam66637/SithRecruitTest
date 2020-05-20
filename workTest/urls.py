from django.urls import path
from .views import HomeView, RecruitChoiceView, SithView, RecruitQuestions, AssessView, ResultTestView, RecruitView

urlpatterns = [
    # Главная
    path('', HomeView.as_view(), name='HomeView_url'),
    # Обработчик формы для рекрута
    path('recruit/', RecruitView.as_view(), name='RecruitView_url'),
    # Обработчик формы для Ситха
    path('sith/', SithView.as_view(), name='SithView_url'),
    # Обработчик выбора рекрута
    path('chooserecruit/', RecruitChoiceView.as_view(), name='RecruitChoiceView_url'),
    # Обработчик формы для теста
    path('recruitquestions/', RecruitQuestions.as_view(), name='RecruitQuestions_url'),
    # Обработчик результата теста
    path('resultest/', ResultTestView.as_view(), name='ResultTest_url'),
    # Обработчик оценивания результатов теста
    path('assess/', AssessView.as_view(), name='AssessView_url')
]