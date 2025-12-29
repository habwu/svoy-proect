# docs/utils.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfplumber
import io
import logging
import re
from reportlab.platypus import FrameBreak
from main.models import Olympiad, Subject, Stage, Category, LevelOlympiad
from result.models import Result
from users.models import User
from django.conf import settings
import os

logger = logging.getLogger(__name__)

# Сопоставление этапов с их slug на сайте
STAGE_SLUGS = {
    'школьный': 'school',
    'муниципальный': 'mun',
    'региональный': 'region',
}

def determine_status(points, stage_name):
    """
    Определяет статус результата на основе набранных баллов и этапа олимпиады.
    """
    stage = stage_name.strip().lower()
    if stage == 'школьный':
        if points >= 100:
            return Result.WINNER
        elif points >= 50:
            return Result.PRIZE
        else:
            return Result.PARTICIPANT
    elif stage == 'муниципальный':
        if points >= 450:
            return Result.WINNER
        elif points >= 300:
            return Result.PRIZE
        else:
            return Result.PARTICIPANT
    elif stage == 'региональный':
        if points >= 1000:
            return Result.WINNER
        elif points >= 450:
            return Result.PRIZE
        else:
            return Result.PARTICIPANT
    else:
        return Result.PARTICIPANT

def get_subjects_from_site():
    """
    Получает список предметов с сайта cpkimr.ru.
    """
    base_url = 'https://cpkimr.ru'
    subjects = []

    # URL школьного этапа
    school_stage_slug = STAGE_SLUGS.get('школьный')
    if not school_stage_slug:
        logger.error('Slug для школьного этапа не найден.')
        return []

    results_url = f'{base_url}/activity/olimpic/{school_stage_slug}/#result'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(results_url, headers=headers)
        if response.status_code != 200:
            logger.error(f'Не удалось получить страницу результатов: {results_url}, статус {response.status_code}')
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Сохранение HTML для проверки
        with open('page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        logger.info('HTML страницы сохранён в файл page.html для проверки.')

        # Найти все теги <p> с классом "olimplic_page_p"
        p_tags = soup.find_all('p', class_='olimplic_page_p')
        logger.info(f'Найдено {len(p_tags)} <p class="olimplic_page_p"> тегов.')

        for p in p_tags:
            span = p.find('span')
            a_tag = p.find('a', href=True)
            if span and a_tag:
                subject_name = span.get_text(strip=True)
                pdf_url = a_tag['href']
                full_pdf_url = urljoin(base_url, pdf_url)
                subjects.append({
                    'name': subject_name,
                    'pdf_url': full_pdf_url,
                    'stage_slug': school_stage_slug,
                })
                logger.debug(f'Извлечён предмет: {subject_name}, PDF: {full_pdf_url}')
            else:
                logger.debug('Тег <p> не содержит одновременно <span> и <a>.')

    except Exception as e:
        logger.error(f'Ошибка при получении предметов с сайта: {e}')

    # Удалить дубликаты по названию
    unique_subjects = {subject['name']: subject for subject in subjects}
    logger.info(f'Найдено {len(unique_subjects)} уникальных предметов для импорта.')
    return list(unique_subjects.values())

def get_system_subjects():
    """
    Получает список предметов из вашей системы для сопоставления.
    """
    try:
        subjects = Subject.objects.all()
        logger.info(f'Найдено {subjects.count()} предметов в системе.')
        return subjects
    except Exception as e:
        logger.error(f'Ошибка при получении предметов из системы: {e}')
        return []

def get_pdf_links(subject_name, stage_slug):
    """
    Получает список ссылок на PDF-файлы для заданного предмета и этапа.
    """
    base_url = 'https://cpkimr.ru'
    results_url = f'{base_url}/activity/olimpic/{stage_slug}/#result'

    pdf_links = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(results_url, headers=headers)
        if response.status_code != 200:
            logger.error(f'Не удалось получить страницу результатов: {results_url}, статус {response.status_code}')
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Сохранение HTML для проверки
        with open('page_pdfs.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        logger.info('HTML страницы с PDF-файлами сохранён в файл page_pdfs.html для проверки.')

        # Найти все теги <p> с классом "olimplic_page_p"
        p_tags = soup.find_all('p', class_='olimplic_page_p')
        logger.info(f'Найдено {len(p_tags)} <p class="olimplic_page_p"> тегов для PDF.')

        for p in p_tags:
            span = p.find('span')
            a_tag = p.find('a', href=True)
            if span and a_tag:
                current_subject = span.get_text(strip=True)
                logger.debug(f'Найден предмет: {current_subject}')
                if subject_name.strip().lower() == current_subject.strip().lower():
                    pdf_url = a_tag['href']
                    full_pdf_url = urljoin(base_url, pdf_url)
                    pdf_links.append(full_pdf_url)
                    logger.debug(f'Найдена PDF-ссылка для предмета {current_subject}: {full_pdf_url}')

    except Exception as e:
        logger.error(f'Ошибка при получении PDF-ссылок: {e}')

    return pdf_links

def import_pdf(system_subject, stage_slug, manual_school_name, system_school, pdf_url):
    """
    Импортирует данные из заданного PDF-файла для предмета и этапа.
    """
    print(f'\nИмпорт данных из PDF: {pdf_url}')
    print(f'Предмет: {system_subject.name}, Этап: {stage_slug}, Школа: {system_school.name}')

    imported_users = set()  # Множество успешно импортированных пользователей
    errors = []  # Список для сбора ошибок

    try:
        response = requests.get(pdf_url)
        if response.status_code != 200:
            error_message = f'Не удалось скачать PDF-файл: {pdf_url}'
            print(error_message)
            errors.append(error_message)
            return {'imported_users': imported_users, 'errors': errors}

        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            print(f'Открыт PDF-файл: {pdf_url}, страниц: {len(pdf.pages)}')
            for page_num, page in enumerate(pdf.pages, start=1):
                print(f'\nОбработка страницы {page_num}')
                table = page.extract_table()
                if not table:
                    error_message = f'Таблица на странице {page_num} не найдена.'
                    print(error_message)
                    errors.append(error_message)
                    continue

                headers = table[0]
                data_rows = table[1:]
                print(f'Найдено {len(data_rows)} строк данных на странице {page_num}')

                for row_num, row in enumerate(data_rows, start=1):
                    if len(row) < 9:
                        error_message = f'Строка {row_num} на странице {page_num} некорректна (мало колонок): {row}'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    # Извлечение данных из строки
                    number_str = row[0]
                    last_name = row[1]
                    first_name = row[2]
                    patronymic = row[3]
                    school_full_name = row[4]
                    class_current = row[5]
                    class_competition = row[6]
                    participant_status = row[7]
                    result_str = row[8]

                    # Нормализация названий школ
                    normalized_manual_school_name = normalize_string(manual_school_name)
                    normalized_school_full_name = normalize_string(school_full_name)

                    # Проверка совпадения школы
                    if normalized_manual_school_name not in normalized_school_full_name:
                        error_message = f'Названия школ не совпадают в строке {row_num} на странице {page_num}. Пропуск строки.'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    try:
                        number = int(number_str.strip())
                        class_current_int = int(class_current.strip())
                    except ValueError:
                        error_message = f'Некорректные числовые значения для номера или класса в строке {row_num} на странице {page_num}. Пропуск строки.'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    # Обработка результата
                    points = None
                    if result_str and result_str.strip():
                        try:
                            points = float(result_str.strip())
                        except ValueError:
                            error_message = f'Некорректные данные результата в строке {row_num} на странице {page_num}: {result_str}. Пропуск строки.'
                            print(error_message)
                            errors.append(error_message)
                            continue
                    else:
                        error_message = f'Результат отсутствует или некорректен в строке {row_num} на странице {page_num}. Пропуск строки.'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    # Поиск пользователя
                    try:
                        user = User.objects.get(
                            first_name__iexact=first_name.strip(),
                            last_name__iexact=last_name.strip(),
                            surname__iexact=patronymic.strip(),
                            school=system_school
                        )
                    except User.DoesNotExist:
                        error_message = f'Пользователь {first_name} {last_name} {patronymic} в школе {system_school.name} не найден. Строка {row_num}, страница {page_num}.'
                        print(error_message)
                        errors.append(error_message)
                        continue
                    except User.MultipleObjectsReturned:
                        error_message = f'Найдено несколько пользователей с именем {first_name} {last_name} {patronymic} в школе {system_school.name}. Строка {row_num}, страница {page_num}.'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    # Получение этапа
                    stage_name_variants = [stage_slug.capitalize(), "Школьный", "school"]
                    stage = Stage.objects.filter(name__in=stage_name_variants).first()
                    if not stage:
                        error_message = f'Этап не найден для slug: {stage_slug}. Строка {row_num}, страница {page_num}.'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    # Поиск олимпиады
                    olympiad = Olympiad.objects.filter(
                        subject=system_subject,
                        stage=stage,
                        class_olympiad=class_current_int
                    ).first()

                    if not olympiad:
                        error_message = f'Олимпиада для предмета "{system_subject.name}", класса {class_current_int}, и этапа "{stage.name}" не найдена. Строка {row_num}, страница {page_num}. Пропуск строки.'
                        print(error_message)
                        errors.append(error_message)
                        continue

                    # Определение статуса результата
                    status = determine_status(points, olympiad.stage.name)

                    # Создание или обновление результата
                    result_obj, created = Result.objects.update_or_create(
                        info_children=user,
                        info_olympiad=olympiad,
                        defaults={
                            'points': points,
                            'status_result': status,
                            'school': system_school,
                        }
                    )

                    # Добавление пользователя в список успешно импортированных
                    imported_users.add(user)

            print('Импорт завершён успешно.')
            return {'imported_users': imported_users, 'errors': errors}

    except Exception as e:
        error_message = f'Ошибка при парсинге PDF: {e}'
        print(error_message)
        errors.append(error_message)
        return {'imported_users': imported_users, 'errors': errors}

def normalize_string(s):
    """
    Нормализует строку:
    - Удаляет переносы строк.
    - Заменяет несколько пробелов одним.
    - Приводит к нижнему регистру.
    - Удаляет кавычки и специальные символы, если необходимо.
    """
    s = s.replace('\n', ' ').replace('\r', ' ')  # Удаление переносов строк
    s = re.sub(r'\s+', ' ', s)  # Замена нескольких пробелов одним
    s = s.strip().lower()  # Удаление лишних пробелов и приведение к нижнему регистру
    # Удаляем кавычки и специальные символы
    s = s.replace('«', '').replace('»', '').replace('"', '').replace("'", "")
    return s

def extract_pdf_data(pdf_url: str) -> list:
    """
    Функция для извлечения данных из PDF-файла.
    Парсит PDF и возвращает список словарей с данными учеников.
    """
    data = []

    try:
        response = requests.get(pdf_url)
        if response.status_code != 200:
            logger.error(f'Не удалось скачать PDF-файл: {pdf_url}')
            return []

        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                table = page.extract_table()
                if not table:
                    logger.warning(f'Таблица на странице {page_num} не найдена.')
                    continue

                headers = table[0]
                data_rows = table[1:]

                for row in data_rows:
                    if len(row) < 8:
                        logger.warning(f'Некорректная строка (мало колонок): {row}')
                        continue  # Пропускаем некорректные строки

                    # Извлекаем данные из строки
                    last_name, first_name, patronymic, school_full_name, class_current, class_competition, result_str = row[:7]

                    # Формируем словарь с данными
                    try:
                        student_class = int(class_current.strip())
                        points = float(result_str.strip())
                    except ValueError:
                        logger.warning(f'Некорректные данные о классе или результате: {row}')
                        continue  # Пропускаем строки с некорректными числами

                    data.append({
                        'last_name': last_name.strip(),
                        'first_name': first_name.strip(),
                        'patronymic': patronymic.strip(),
                        'school_full_name': school_full_name.strip(),
                        'class_current': student_class,
                        'points': points
                    })
                    logger.debug(
                        f'Извлечены данные ученика: {last_name} {first_name} {patronymic}, Класс: {class_current}, Баллы: {points}')

    except Exception as e:
        logger.error(f'Ошибка при парсинге PDF: {e}')

    return data

def clean_html_content(html_content):
    # Удаляем ненужные атрибуты
    html_content = re.sub(r'\s*(dir|role)="[^"]*"', '', html_content)

    # Преобразуем специфические теги в поддерживаемые
    html_content = re.sub(r'<span[^>]*>', '', html_content)  # Убираем теги <span>
    html_content = re.sub(r'</span>', '', html_content)  # Убираем закрывающие теги </span>
    html_content = re.sub(r'<br[^>]*>', '<br/>', html_content)  # Преобразуем <br> в <br/>

    # Удаляем теги <p> и извлекаем выравнивание
    html_content = re.sub(r'<p\s*style="text-align:\s*([^"]+)\s*;">', r'<p align="\1">', html_content)
    html_content = re.sub(r'<p>', '<p align="left">', html_content)

    return html_content

def create_pdf_for_students_in_class(students_data):
    """Создание PDF файла с двумя заявлениями на одной странице для студентов класса"""

    # Получение активного шаблона из настроек
    try:
        agreement_settings = AgreementSettings.objects.first()
        if not agreement_settings or not agreement_settings.selected_template:
            raise Exception("Не выбран шаблон для согласий. Обратитесь к администратору.")
        pdf_template = agreement_settings.selected_template
    except PDFTemplate.DoesNotExist:
        raise Exception("Шаблон для согласий не найден.")

    # Путь к шрифту
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesnewromanpsmt.ttf')
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Файл шрифта не найден по пути: {font_path}")

    # Регистрация шрифта
    pdfmetrics.registerFont(TTFont('TimesNewRomanPSMT', font_path))

    # Создание буфера для PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    # Настройка Petrovich для склонения
    petrovich = Petrovich()

    def to_accusative(name, gender):
        parts = name.split()
        if len(parts) != 3:
            return name  # Если имя не состоит из трех частей, возвращаем как есть
        last_name, first_name, middle_name = parts

        # Используем Petrovich для склонения имени по падежам
        if gender == User.MALE:
            gender_case = Gender.MALE
        else:
            gender_case = Gender.FEMALE

        return f"{petrovich.lastname(last_name, Case.ACCUSATIVE, gender_case)} {petrovich.firstname(first_name, Case.ACCUSATIVE, gender_case)} {petrovich.middlename(middle_name, Case.ACCUSATIVE, gender_case)}"

    # Группировка олимпиад по ученикам
    students_subjects = defaultdict(list)
    for student, subjects in students_data:
        students_subjects[student].extend(subjects)

    # Создание стилей для текста с различным выравниванием
    styles = getSampleStyleSheet()

    # Основной стиль для текста
    base_style = ParagraphStyle(
        'BaseStyle',
        fontName='TimesNewRomanPSMT',
        fontSize=12,
        leading=14,  # Уменьшенный межстрочный интервал
        spaceAfter=5,  # Отступ после абзаца
    )

    # Функция для уменьшения шрифта, если текст не помещается
    def create_paragraph(text, max_height, style):
        min_font_size = 8
        while style.fontSize > min_font_size:
            para = Paragraph(text, style)
            width, height = para.wrap(doc.width, max_height)
            if height <= max_height:
                return para
            style.fontSize -= 1
            style.leading -= 1
        return Paragraph(text, style)

    # Создание двух рамок на странице для двух заявлений
    width, height = A4
    half_height = height / 2 - 40  # Разделяем высоту страницы на две части

    frames = [
        Frame(30, height / 2 + 10, width - 60, half_height, id='top_frame', showBoundary=0),
        Frame(30, 20, width - 60, half_height, id='bottom_frame', showBoundary=0)
    ]

    page_template = PageTemplate(id='TwoStatements', frames=frames)
    doc.addPageTemplates([page_template])

    story = []
    students_list = list(students_subjects.items())

    for i in range(0, len(students_list), 2):
        added_content = False  # Флаг для отслеживания добавленного контента на текущей странице

        for j in range(2):
            if i + j < len(students_list):
                student, subjects = students_list[i + j]

                # Получаем пол студента из модели User
                gender = student.gender
                full_name_accusative = to_accusative(f"{student.last_name} {student.first_name} {student.surname}", gender)

                context = {
                    'son_or_daughter': 'моего сына' if gender == User.MALE else 'мою дочь',
                    'full_name': full_name_accusative,
                    'classroom': f"{student.classroom.number}{student.classroom.letter}",
                    'olympiad_name': "Пример олимпиады",
                    'subjects': ', '.join(set(subjects)),  # Убираем дублирующиеся предметы
                    'date': datetime.now().strftime("%d.%m.%Y"),
                }

                # Рендеринг шаблона
                template = Template(pdf_template.content)
                rendered_text = template.render(Context(context))

                # Очистка и обработка HTML-контента
                clean_content = clean_html_content(rendered_text)

                # Создание параграфов с автоматическим уменьшением шрифта, если текст не помещается
                paragraphs = re.split(r'(</p>)', clean_content)
                for para in paragraphs:
                    if 'align="center"' in para:
                        style = base_style.clone('CenterStyle', alignment=1)
                    elif 'align="right"' in para:
                        style = base_style.clone('RightStyle', alignment=2)
                    else:
                        style = base_style.clone('LeftStyle', alignment=0)

                    p = create_paragraph(para.replace('</p>', ''), max_height=half_height, style=style)
                    story.append(p)
                added_content = True  # Отмечаем, что контент был добавлен

        if added_content:
            story.append(FrameBreak())  # Переход к следующей рамке

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf