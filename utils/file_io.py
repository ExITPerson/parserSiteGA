import csv
import json
from datetime import datetime
from pathlib import Path

from utils.cleaner import clean_cell

data = {'туалетная вода': [{'article': '7192200017', 'name': 'DIOR Miss Dior Blooming Bouquet', 'product_type': 'туалетная вода', 'country': 'Франция', 'price_actual': '16300', 'price_loyalty': '16300', 'url': 'https://goldapple.ru/7192200017-miss-dior-blooming-bouquet', 'popularity_coefficient': 787.72, 'description': 'Miss Dior Blooming Bouquet - это мгновенное удовольствие, признание в любви к жизни, которое вовлекает Вас.\nПоявившись в 1947 году, Miss Dior исполнил мечту Кристиана Диора о создании средства от печали и тоски. С тех пор Miss Dior не изменил своего предназначения, он все также воплощает красоту и счастье.\nТуалетная вода Miss Dior Blooming Bouquet была создана словно цветочное прикосновение, одновременно чувственное и нежное. Это многогранный и неповторимый букет только что распустившихся цветов. Его контрастный шлейф вызывает ощущение подобное любви с первого взгляда, переданной в нотах полевых цветов и бергамота. \nДуэт нот дамасской розы и пиона раскрывается благородством, подобно страстным и сияющим эмоциям. Мягкий, легкий аккорд белого мускуса завершает букет этого аромата, рассказывающего историю любви.\nАромат Miss Dior Blooming Bouquet помещен во флакон в особенном стиле: бант Miss Dior, сотканный из тысячи разноцветных нитей, придает аромату кутюрный штрих. Этот необыкновенный жаккардовый бант, вдохновленный букетом из тысячи переливающихся цветов, был создан в мастерской одного из самых известных французских производителей лент: Maison Faure, основанной в 1864 году.\nЭта нежная и свежая туалетная вода также выпускается в формате роликовой жемчужины, которую удобно брать с собой.', 'application': 'Небольшое количество аромата аккуратно нанести на зону шеи, декольте, запястьев.'}, {'article': '81101200001', 'name': 'BANDERAS The Secret', 'product_type': 'туалетная вода', 'country': 'Испания', 'price_actual': '4242', 'price_loyalty': '2969', 'url': 'https://goldapple.ru/81101200001-the-secret', 'popularity_coefficient': 257.28, 'description': 'Туалетная вода Banderas The Secret — роскошный аромат, который непременно придется по вкусу истинным джентльменам. Раскрывается парфюмерная композиция The Secret пряными коричными оттенками, плавно перетекающими в свежесть мяты и грейпфрута. В сердце туалетной воды от Banderas мягко переливаются соблазнительный мускус и легкая острота перца, а в шлейфе остаются благородные кожаные нотки и древесные акценты.', 'application': None}, {'article': '19000284704', 'name': 'YOU & WORLD Believe me You like the sun', 'product_type': 'туалетная вода', 'country': 'Россия', 'price_actual': '885', 'price_loyalty': '734', 'url': 'https://goldapple.ru/19000284704-believe-me-you-like-the-sun', 'popularity_coefficient': 244.4, 'description': 'Мир прекрасен! Наслаждайся! \nНовый аромат BELIEVE ME You like the sun перенесет тебя на живописную прогулку , где солнце нежно греет кожу. \nТы почувствуешь, как его ласковые лучи расслабляют и заряжают энергией. Аромат вдохновляет наслаждаться жизнью и уметь находить радость в мелочах.         \n Сияй! Мечтай! Улыбайся!', 'application': 'Нанести на шею, запястье, локтевые сгибы.'}, {'article': '19000122335', 'name': 'HELLO KITTY WEDDING DRESS', 'product_type': 'туалетная вода', 'country': None, 'price_actual': '858', 'price_loyalty': '531', 'url': 'https://goldapple.ru/19000122335-wedding-dress', 'popularity_coefficient': 175.68, 'description': 'Туалетная вода Hello Kittty- это ода нежной и радостной юности, которую парфюмеры, будто особенные волшебники, поместили во флакон. Некоторые могут обмануться названием данного аромата и посчитать, что его создали для совсем юной аудитории, но это не совсем так… Мы уверены- многие молодые девушки захотят ощутить, как это быть частью волшебного мира Hello Kitty, как верить в добрые сказки.\nНоты: цитрус, пион, мандарин, османтус, роза, сандал, пачули, розовый перец. Аромат весна! Аромат влюблённость! Облако нежности, идеальное чистое звучание, как раз под стать такому же чистому и воздушному белому свадебному платью, о котором мечтают девочки всех возрастов!', 'application': 'Парфюм\xa0всех типов наносится на чистую, слегка увлаженную кожу.'}, {'article': '19000133630', 'name': 'MANDARINA DUCK Woman', 'product_type': 'туалетная вода', 'country': 'Италия', 'price_actual': '8887', 'price_loyalty': '5332', 'url': 'https://goldapple.ru/19000133630-woman', 'popularity_coefficient': 84.48, 'description': 'Свежий цветочный аромат отражает главные ценности бренда MANDARINA DUCK: яркость, позитивные эмоции, инновации и движение вперед. \nЯркая, но в то же время подходящая для любого дня парфюмерная композиция стартует с бодрящего звучания бергамота, нежности желтой фрезии и дерзкого акцента белого перца. \nВ чарующем цветочном сердце аромата раскрывается изысканная нота гардении, украшенная аккордами жасминового чая и жимолости. \nВдохновляющее сочетание нот дополняют чувственные кедр, мускус и амбретта.', 'application': 'Только для наружного применения.'}, {'article': '26421100019', 'name': 'ACQUA DI PARMA ARANCIA DI CAPRI', 'product_type': 'туалетная вода', 'country': 'Италия', 'price_actual': '7990', 'price_loyalty': '7990', 'url': 'https://goldapple.ru/26421100019-arancia-di-capri', 'popularity_coefficient': 72.96, 'description': 'Символ итальянского Средиземноморья. Остров Капри. Искрящийся. Солнечный. Успокаивающий. Аромат, объединяющий эфирные масла апельсина, мандарина и лимона. В сердце аромата Петит Грейн  идеально сочетается с насыщенным оттенком кардамона. В шлейфе мягко звучит нежная нота карамели, украшенная чувственным мускусом.', 'application': None}]}

ROOT_DIR = Path(__file__).resolve().parent.parent

def save_json(data):

    filepath = ROOT_DIR / 'data' / 'json'
    filepath.parent.mkdir(parents=True, exist_ok=True)

    now_date = datetime.now().date()

    try:
        with open(f'{filepath}/{now_date}_products.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f'Ошибка сохранения json файла: {e}')

def save_csv(data, file_name):

    filepath = ROOT_DIR / 'data' / 'csv'
    filepath.parent.mkdir(parents=True, exist_ok=True)

    now_date = datetime.now().date()

    fieldnames = data[0].keys()

    for item in data:
        item['description'] = clean_cell(item['description'])
        item['application'] = clean_cell(item['application'])

    try:
        with open(f'{filepath}/{now_date}_{file_name}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)

    except Exception as e:
        print(f'Ошибка записи файла в csv: {e}')


for key, value in data.items():
    save_csv(value, key)
