"""Load demo data: >=10 rows per table (lab requirement)."""
import logging
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from insurance import models

log = logging.getLogger("insurance")
N = 10


def _phone_unique(seq: int) -> str:
    n = (1_000_000 + seq * 7919) % 10_000_000
    s = f"{n:07d}"
    return f"+375 (29) {s[:3]}-{s[3:5]}-{s[5:7]}"


def _adult_birth(years: int = 30) -> date:
    return date.today().replace(year=date.today().year - years)


def clear_demo_data() -> None:
    models.Review.objects.all().delete()
    models.PromoCode.objects.all().delete()
    models.Vacancy.objects.all().delete()
    models.ContactPerson.objects.all().delete()
    models.FAQEntry.objects.all().delete()
    models.NewsArticle.objects.all().delete()
    models.CompanyRequisite.objects.all().delete()
    models.CompanyProfile.objects.all().delete()
    models.Contract.objects.all().delete()
    models.InsuredObject.objects.all().delete()
    models.ClientIdentity.objects.all().delete()
    models.Client.objects.all().delete()
    models.Agent.objects.all().delete()
    models.Branch.objects.all().delete()
    models.InsuranceType.objects.all().delete()


def seed() -> None:
    cities = ["Минск", "Гродно", "Брест", "Гомель", "Витебск", "Могилёв", "Бобруйск", "Барановичи", "Пинск", "Орша"]
    branches = [
        models.Branch(
            name=f"Филиал {cities[i]}",
            address=f"ул. Центральная, {10 + i}",
            city=cities[i],
            phone=_phone_unique(i + 1),
        )
        for i in range(N)
    ]
    models.Branch.objects.bulk_create(branches)
    branches = list(models.Branch.objects.order_by("id"))

    types_data = [
        ("Авто от угона", Decimal("0.028000"), Decimal("12.00")),
        ("Имущество граждан", Decimal("0.018000"), Decimal("10.00")),
        ("ДМС", Decimal("0.042000"), Decimal("15.00")),
        ("Жизнь", Decimal("0.012000"), Decimal("8.00")),
        ("КАСКО", Decimal("0.055000"), Decimal("14.00")),
        ("Ответственность ТС", Decimal("0.022000"), Decimal("11.00")),
        ("Несчастный случай", Decimal("0.025000"), Decimal("9.00")),
        ("Путешествия", Decimal("0.015000"), Decimal("7.00")),
        ("Грузоперевозки", Decimal("0.020000"), Decimal("10.50")),
        ("Сельхоз риски", Decimal("0.019000"), Decimal("8.50")),
    ]
    insurance_types = [
        models.InsuranceType(name=name, tariff_rate=tr, agent_commission_percent=cp)
        for name, tr, cp in types_data
    ]
    models.InsuranceType.objects.bulk_create(insurance_types)
    insurance_types = list(models.InsuranceType.objects.order_by("id"))

    agents = []
    for i in range(N):
        br = branches[i % len(branches)]
        agents.append(
            models.Agent(
                last_name=f"Агентов{i + 1}",
                first_name=f"Имя{i + 1}",
                patronymic="Петрович",
                phone=_phone_unique(20 + i),
                birth_date=_adult_birth(25 + (i % 10)),
                branch=br,
            )
        )
    models.Agent.objects.bulk_create(agents)
    agents_by_branch = {}
    for a in models.Agent.objects.select_related("branch"):
        agents_by_branch.setdefault(a.branch_id, []).append(a)

    clients = [
        models.Client(
            full_name=f"Клиент Демо {i + 1}",
            phone=_phone_unique(100 + i),
            email=f"client{i + 1}@example.invalid",
            birth_date=_adult_birth(22 + (i % 8)),
            address=f"г. {cities[i % len(cities)]}, ул. Примерная, д. {10 + i}",
        )
        for i in range(N)
    ]
    models.Client.objects.bulk_create(clients)
    clients = list(models.Client.objects.order_by("id"))

    for i, c in enumerate(clients):
        models.ClientIdentity.objects.create(
            client=c,
            document_id=f"MP{7000000 + i}",
        )

    kinds = [c[0] for c in models.InsuredObject.ObjectKind.choices]
    objects_list = [
        models.InsuredObject(
            object_type=kinds[i % len(kinds)],
            description=f"Объект страхования №{i + 1}",
            value=Decimal(5000 + i * 2500),
        )
        for i in range(N)
    ]
    models.InsuredObject.objects.bulk_create(objects_list)
    objects_list = list(models.InsuredObject.objects.order_by("id"))

    base_signed = date(2024, 1, 10)
    for i in range(N):
        br = branches[i % len(branches)]
        branch_agents = agents_by_branch.get(br.id, [])
        ag = branch_agents[0] if branch_agents else list(agents_by_branch.values())[0][0]
        signed = base_signed + timedelta(days=20 * i)
        contract = models.Contract(
            signed_date=signed,
            end_date=signed + timedelta(days=365),
            insurance_amount=Decimal(8000 + i * 4500),
            branch=br,
            agent=ag,
            client=clients[i],
            insurance_type=insurance_types[i % len(insurance_types)],
        )
        contract.save()
        contract.insured_objects.add(objects_list[i % len(objects_list)])

    profile = models.CompanyProfile.objects.create(
        title="О компании (демо)",
        about_text="Страховая компания демонстрационного стенда.",
    )
    for i in range(N):
        models.CompanyRequisite.objects.create(
            profile=profile,
            label=f"Реквизит {i + 1}",
            value=f"Значение реквизита №{i + 1}",
            sort_order=i,
        )

    news_data = [
        (
            "Запуск программы льготного автострахования КАСКО «Защита плюс»",
            "Наша компания объявляет о старте новой программы комплексного страхования автомобилей с нулевым франшизным порогом.",
            "Мы рады представить обновленную линейку полисов КАСКО, разработанную с учетом актуальных потребностей автовладельцев. Новая программа «Защита плюс» включает круглосуточную эвакуацию при ДТП, бесплатный вызов аварийного комиссара и расширенное покрытие рисков стихийных бедствий. Оформить договор можно онлайн со скидкой 15% при использовании сезонного промокода."
        ),
        (
            "Итоги выплат по добровольному медицинскому страхованию за третий квартал",
            "Общая сумма страховых возмещений по договорам ДМС превысила 2,4 миллиона белорусских рублей.",
            "За отчетный период наша компания оперативно урегулировала более 4 500 страховых случаев по программам медицинского страхования граждан. Благодаря цифровизации процессов и прямой интеграции с ведущими клиниками страны, среднее время согласования амбулаторного лечения сократилось до 15 минут. Мы продолжаем совершенствовать качество сервиса для каждого застрахованного клиента."
        ),
        (
            "Новые правила оформления электронных полисов ОСАГО через личный кабинет",
            "Теперь заключение договора обязательного страхования гражданской ответственности занимает менее пяти минут.",
            "В соответствии с новыми стандартами электронного взаимодействия, клиенты нашей компании могут оформить и продлить полис ОСАГО полностью в удаленном формате через персональный кабинет на портале. Готовый документ с электронной цифровой подписью автоматически поступает на ваш email и в государственную базу данных ГАИ."
        ),
        (
            "Расширение сети региональных филиалов в Гродненской и Витебской областях",
            "Компания открыла три новых современных офиса обслуживания физических и юридических лиц.",
            "В рамках стратегии регионального развития мы расширяем присутствие в районных центрах Беларуси. Новые офисы оснащены комфортными зонами клиентского обслуживания, терминалами самообслуживания и выделенными линиями консультаций по имущественным и рисковым видам страхования. Штат укомплектован сертифицированными экспертами высшей категории."
        ),
        (
            "Защита загородной недвижимости: сезонные скидки на полисы страхования коттеджей",
            "Специальное предложение на комплексное страхование дачных домов и загородного имущества действует до конца месяца.",
            "С приближением дачного сезона актуальным вопросом становится защита загородного жилья от пожаров, затоплений и противоправных действий третьих лиц. Наш новый страховой пакет покрывает конструктивные элементы зданий, внутреннюю отделку и инженерное оборудование без необходимости предварительной описи имущества."
        ),
        (
            "Международная финансовая конференция: тренды страхового рынка 2026 года",
            "Эксперты нашей компании приняли участие в обсуждении цифровой трансформации и киберстрахования.",
            "На прошедшей в Минске ежегодной конференции руководители ведущих страховых организаций поделились прогнозами развития рынка. Особое внимание было уделено защите бизнеса от киберрисков, внедрению систем искусственного интеллекта для оценки ущерба и развитию экосистем непрерывной заботы о клиентах."
        ),
        (
            "Стартовал конкурс профессионального мастерства среди страховых агентов",
            "Лучшие специалисты клиентского сервиса поборются за звание главного эксперта года.",
            "В нашей компании начался ежегодный внутренний конкурс среди сотрудников и агентов всех филиалов. Жюри оценивает уровень клиентской удовлетворенности, скорость обработки договоров и качество консультирования по сложным комплексным программам страхования жизни и здоровья. Победители получат ценные призы и памятные награды."
        ),
        (
            "Безопасные путешествия: что важно знать при оформлении медицинской страховки за рубеж",
            "Обновлены условия полисов выезжающих за границу с включением расширенного покрытия спортивных рисков.",
            "Планируя отпуск или командировку за рубежом, важно позаботиться о надежной медицинской защите. Наша страховая программа для путешественников теперь включает круглосуточную мультиязычную поддержку ассистанс-компании, покрытие расходов на экстренную стоматологию и репатриацию без скрытых лимитов ответственности."
        ),
        (
            "Финансовая грамотность: как правильно рассчитать страховую сумму по договору имущества",
            "Специалисты подготовили подробную инструкцию по определению реальной стоимости страхуемых объектов.",
            "Ошибки при оценке стоимости квартиры или автомобиля могут привести к недострахованию при наступлении страхового случая. В нашей новой статье мы подробно разбираем методику расчета действительной рыночной стоимости имущества и объясняем принципы работы пропорциональной системы возмещения ущерба."
        ),
        (
            "Экологическая инициатива компании: переход на безбумажный документооборот",
            "Полный переход на цифровые полисы позволил сократить бумажный расход на 80% за последний год.",
            "Наша страховая фирма последовательно реализует политику экологической ответственности и устойчивого развития. Отказ от бумажных бланков в пользу защищенных электронных сертификатов позволил не только ускорить обслуживание клиентов, но и внести значительный вклад в сохранение лесных ресурсов Республики Беларусь."
        ),
    ]

    for n, (title, summary, body) in enumerate(news_data):
        models.NewsArticle.objects.create(
            title=title,
            slug=slugify(f"news-{n + 1}-{title[:15]}")[:200],
            summary=summary,
            image_url=f"insurance/images/news_{n + 1}.jpg",
            body=body,
            is_published=True,
            published_at=timezone.now() - timedelta(days=n),
        )

    faq_data = [
        (
            "Что такое страховой случай и как о нем сообщить?",
            "Страховым случаем признается совершившееся событие, предусмотренное договором страхования, с наступлением которого возникает обязанность страховщика произвести выплату. Сообщить можно по телефону горячей линии или через личный кабинет в течение 24 часов."
        ),
        (
            "Как рассчитывается стоимость полиса КАСКО?",
            "Стоимость полиса зависит от марки и модели автомобиля, года выпуска, возраста и стажа водителей, а также выбранной страховой суммы и франшизы. Вы можете рассчитать предварительную стоимость на нашем сайте или у агента."
        ),
        (
            "Можно ли расторгнуть договор страхования досрочно?",
            "Да, страхователь имеет право расторгнуть договор в любое время. При этом производится перерасчет страховой премии с учетом истекшего периода действия договора и расходов компании в соответствии с условиями правил страхования."
        ),
        (
            "Какие документы нужны для получения выплаты по ОСАГО?",
            "Требуется заявление о страховой выплате, извещение о ДТП, документы, удостоверяющие личность, свидетельство о регистрации транспортного средства, водительское удостоверение и справка из ГАИ (при необходимости)."
        ),
        (
            "Действует ли медицинская страховка (ДМС) за рубежом?",
            "Стандартные программы ДМС действуют на территории Республики Беларусь. Для поездок за границу необходимо оформление специального полиса медицинского страхования выезжающих за рубеж (ВЗР)."
        ),
        (
            "Что делать при повреждении застрахованного имущества?",
            "Необходимо незамедлительно зафиксировать повреждения, вызвать профильные службы (МЧС, милицию при краже или пожаре) и обратиться в страховую компанию до проведения восстановительных работ."
        ),
        (
            "Как применить промокод при оформлении полиса?",
            "Введите полученный промокод в специальное поле на странице корзины или при онлайн-оформлении договора, и сумма к оплате автоматически уменьшится на процент скидки."
        ),
        (
            "Какие сроки выплаты страхового возмещения?",
            "Выплата страхового возмещения производится в течение 5-15 рабочих дней после предоставления полного пакета документов и подписания акта о страховом случае."
        ),
        (
            "Нужно ли проходить осмотр автомобиля при продлении КАСКО?",
            "Если полис продлевается в той же компании без перерыва и предыдущий договор закончился без страховых случаев, осмотр транспортного средства, как правило, не требуется."
        ),
        (
            "Как связаться со службой поддержки клиентов?",
            "Наша служба поддержки работает круглосуточно. Вы можете позвонить по номеру +375 (17) 200-00-00 или написать нам на электронную почту support@insurance.by."
        ),
    ]

    for q, a in faq_data:
        models.FAQEntry.objects.create(question=q, answer=a)

    contact_roles = [
        ("Руководитель отдела урегулирования убытков", "Консультирование клиентов по сложным страховым случаям, контроль выплат и взаимодействие с экспертами-оценщиками."),
        ("Главный специалист по автострахованию", "Оформление полисов ОСАГО и КАСКО, расчет рисков, подбор оптимальных тарифных программ для автовладельцев."),
        ("Менеджер по корпоративным клиентам", "Заключение комплексных договоров страхования имущества юридических лиц, сопровождение корпоративных парков."),
        ("Специалист отдела ДМС", "Координация медицинских услуг застрахованных лиц, согласование лечения с ведущими клиниками и центрами."),
        ("Ведущий андеррайтер", "Оценка страховых рисков, анализ заявлений на страхование крупного имущества и определение тарифных ставок."),
        ("Менеджер по работе с агентами", "Обучение страховых агентов, контроль выполнения планов продаж, методическая поддержка."),
        ("Специалист контакт-центра", "Прием входящих звонков, оперативное консультирование по всем видам услуг, регистрация заявлений."),
        ("Эксперт по страхованию жизни", "Консультирование по накопительным и рисковым программам долгосрочного страхования жизни и здоровья."),
        ("Специалист отдела выплат", "Проверка документов, формирование выплатного дела, подготовка распоряжений на перечисление возмещений."),
        ("Руководитель филиала", "Общее руководство деятельностью филиала, развитие региональной сети, представительские функции."),
    ]

    for i, (role, duties) in enumerate(contact_roles):
        br = branches[i % len(branches)]
        models.ContactPerson.objects.create(
            full_name=f"Специалист {i + 1} ({br.city})",
            role_title=role,
            photo_url="insurance/images/contact.svg",
            phone=_phone_unique(300 + i),
            email=f"expert{i + 1}@insurance.by",
            bio=duties,
            birth_date=_adult_birth(30 + (i % 8)),
            branch=br,
        )

    for i in range(N):
        models.Vacancy.objects.create(
            title=f"Вакансия: страховой агент ({i + 1})",
            description="Консультирование, оформление договоров.",
            is_active=i < 8,
        )

    for i in range(N):
        models.Review.objects.create(
            guest_name=f"Гость {i + 1}",
            rating=(i % 5) + 1,
            text=f"Отзыв демо №{i + 1}: понравился сервис, рекомендую коллегам.",
        )

    today = date.today()
    for i in range(N):
        vf = today - timedelta(days=30 + i * 10)
        vt = today + timedelta(days=60 + i * 5)
        models.PromoCode.objects.create(
            code=f"PROMO{i + 1:02d}",
            discount_percent=Decimal(5 + (i % 10)),
            valid_from=vf,
            valid_until=vt,
            is_active=i < 7,
        )

    for group_name in ("client", "employee"):
        Group.objects.get_or_create(name=group_name)


class Command(BaseCommand):
    help = f"Create demo records ({N}+ per table). --force to replace."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        if options["clear"]:
            with transaction.atomic():
                clear_demo_data()
            self.stdout.write(self.style.SUCCESS("Cleared insurance app data."))
            return

        if models.Contract.objects.exists() and not options["force"]:
            self.stdout.write(
                self.style.WARNING("Data exists. Use --force to re-seed.")
            )
            return

        with transaction.atomic():
            if options["force"]:
                clear_demo_data()
            seed()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded: branches={models.Branch.objects.count()}, "
                f"contracts={models.Contract.objects.count()}, "
                f"news={models.NewsArticle.objects.count()}"
            )
        )
