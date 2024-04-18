from django.db.models import Max, Count, F
from django.shortcuts import render
from django.views import View
# from .models import ...
from .models import Author, AuthorProfile, Entry, Tag

class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])  # TODO Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        self.answer2 = Author.objects.annotate(num_entries=Count('entries')).order_by('-num_entries')[:1]  # TODO Какой автор имеет наибольшее количество опубликованных статей?
        self.answer3 = Entry.objects.filter(tags__name__in=['Кино', 'Музыка']).distinct()  # TODO Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer4 = Author.objects.filter(gender='ж').count()  # TODO Сколько авторов женского пола зарегистрировано в системе?
        self.answer5 = round(Author.objects.filter(status_rule=True).count() * 100 / Author.objects.count(), 2)  # TODO Какой процент авторов согласился с правилами при регистрации?
        self.answer6 = Author.objects.filter(authorprofile__stage__range=(1, 5))  # TODO Какие авторы имеют стаж от 1 до 5 лет?
        max_age= Author.objects.aggregate(Max('age'))
        self.answer7 = Author.objects.get(age=max_age['age__max'])  # TODO Какой автор имеет наибольший возраст?
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()  # TODO Сколько авторов указали свой номер телефона?
        self.answer9 = Author.objects.filter(age__lt=25)  # TODO Какие авторы имеют возраст младше 25 лет?
        self.answer10 = Entry.objects.values('author__username').annotate(count=Count('id'), username=F('author__username'))  # TODO Сколько статей написано каждым автором?
        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}

        return render(request, 'train_db/training_db.html', context=context)

