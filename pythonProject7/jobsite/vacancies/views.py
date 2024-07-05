import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import VacancySearchForm

# Фиксированные курсы валют для примера (рублей за единицу валюты)
CURRENCY_RATES = {
    'USD': 88,  # 1 доллар США = 75 рублей
    'EUR': 95,  # 1 евро = 85 рублей
    'RUB': 1,
    'BYR': 27
}


def convert_to_rub(amount, currency):
    if currency in CURRENCY_RATES:
        return amount * CURRENCY_RATES[currency]
    return amount


def fetch_vacancies(title, page):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': title,
        'per_page': 100,
        'page': page - 1  # API hh.ru использует нумерацию страниц, начиная с 0
    }

    response = requests.get(url, params=params)
    data = response.json()

    vacancies = []
    for item in data['items']:
        title = item['name']
        salary = item['salary']
        if salary:
            if salary['from'] and salary['to']:
                salary_from_rub = convert_to_rub(salary['from'], salary['currency'])
                salary_to_rub = convert_to_rub(salary['to'], salary['currency'])
                salary_text = f"{salary_from_rub} - {salary_to_rub} RUB"
            elif salary['from']:
                salary_from_rub = convert_to_rub(salary['from'], salary['currency'])
                salary_text = f"from {salary_from_rub} RUB"
            elif salary['to']:
                salary_to_rub = convert_to_rub(salary['to'], salary['currency'])
                salary_text = f"up to {salary_to_rub} RUB"
            else:
                salary_text = 'Не указана'
        else:
            salary_text = 'Не указана'

        url = item['alternate_url']
        company_name = item['employer']['name']

        vacancies.append({
            'title': title,
            'salary': salary_text,
            'url': url,
            'company_name': company_name
        })

    return vacancies, data['pages']  # Возвращаем количество страниц


def search_vacancies(request):
    form = VacancySearchForm(request.GET)
    vacancies = []
    total_pages = 0

    if form.is_valid():
        title = form.cleaned_data.get('title', '')
        page = request.GET.get('page', 1)
        vacancies, total_pages = fetch_vacancies(title, int(page))

    # Пагинация
    paginator = Paginator(vacancies, 10)
    page = request.GET.get('page', 1)

    try:
        vacancies_page = paginator.page(page)
    except PageNotAnInteger:
        vacancies_page = paginator.page(1)
    except EmptyPage:
        vacancies_page = paginator.page(paginator.num_pages)

    return render(request, 'vacancies/search.html', {
        'form': form,
        'vacancies': vacancies_page,
        'total_pages': total_pages,
        'search_query': request.GET.get('title', '')
    })