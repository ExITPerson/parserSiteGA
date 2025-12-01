import pytest

from utils.sorter import sorter_product, sort_by_popularity


def test_sorter_product():
    """ Проверка корректного вывода функции """
    data = [
        {'product_type': 'type 1', 'name': 'Product 1'},
        {'product_type': 'type2', 'name': 'Product 2'},
        {'product_type': 'type 1', 'name': 'Product 3'},
        {'product_type': 'type2', 'name': 'Product 4'}
    ]

    result = sorter_product(data)

    assert result == {
        'type 1': [
            {'name': 'Product 1', 'product_type': 'type 1'},
            {'name': 'Product 3', 'product_type': 'type 1'}
        ],
        'type2': [
            {'name': 'Product 2', 'product_type': 'type2'},
            {'name': 'Product 4', 'product_type': 'type2'}
        ]
    }


def test_sorter_product_no_type():
    """ Проверка пропуска товаров без типа """
    data = [
        {'product_type': 'type 1', 'name': 'Product 1'},
        {'product_type': 'type2', 'name': 'Product 2'},
        {'product_type': None, 'name': 'Product 2'},
        {'product_type': 'type 1', 'name': 'Product 4'},
        {'product_type': 'type2', 'name': 'Product 5'}
    ]

    result = sorter_product(data)

    assert result == {
        'type 1': [
            {'name': 'Product 1', 'product_type': 'type 1'},
            {'name': 'Product 4', 'product_type': 'type 1'}
        ],
        'type2': [
            {'name': 'Product 2', 'product_type': 'type2'},
            {'name': 'Product 5', 'product_type': 'type2'}
        ]
    }


def test_sorter_product_raises_on_wrong_type():
    """ Проверка то, что функция возвращает None при неверном типе данных и выдает ошибку """
    assert sorter_product("string") is None
    assert sorter_product(None) is None
    assert sorter_product({"a": 1}) is None


@pytest.fixture
def sample_data():
    return {
        "parfume": [
            {"name": "Product 1", "popularity_coefficient": 10.5},
            {"name": "Product 2", "popularity_coefficient": None},
            {"name": "Product 3", "popularity_coefficient": 44.88},
            {"name": "Product 4", "popularity_coefficient": 2.58},
        ],
        "deo": [
            {"name": "Product 5", "popularity_coefficient": None},
            {"name": "Product 6", "popularity_coefficient": 5.0},
            {"name": "Product 7", "popularity_coefficient": 1.0},
        ],
    }


def test_sort_by_popularity_each_category_descending(sample_data):
    """ Проверка на корректность сортировки """
    sorted_data = sort_by_popularity(sample_data)

    parfume_names = [p["name"] for p in sorted_data["parfume"]]
    assert parfume_names == ["Product 3", "Product 1", "Product 4", "Product 2"]

    deo_names = [p["name"] for p in sorted_data["deo"]]
    assert deo_names == ["Product 6", "Product 7", "Product 5"]


def test_sort_by_popularity_none_is_last(sample_data):
    """ Проверка на то, что последний элемент имеет None """
    sorted_data = sort_by_popularity(sample_data)

    assert sorted_data["parfume"][-1]["popularity_coefficient"] is None
    assert sorted_data["deo"][-1]["popularity_coefficient"] is None


def test_sort_by_popularity_empty_category():
    """ Проверка, если сортируется пустой список """
    data = {"empty": []}
    assert sort_by_popularity(data) == {"empty": []}


def test_sort_by_popularity_all_none():
    """ Проверка, что возвращаются все элементы, если все они имеют коэффициент None """
    data = {"test": [
        {"name": "X", "popularity_coefficient": None},
        {"name": "Y", "popularity_coefficient": None},
    ]}

    sorted_data = sort_by_popularity(data)
    assert len(sorted_data["test"]) == 2


def test_sort_by_popularity_all_numbers():
    """ Проверка на корректность сортировки """
    data = {"nums": [
        {"name": "N1", "popularity_coefficient": 3.0},
        {"name": "N2", "popularity_coefficient": 1.5},
        {"name": "N3", "popularity_coefficient": 7.2},
    ]}

    sorted_data = sort_by_popularity(data)
    coeffs = [p["popularity_coefficient"] for p in sorted_data["nums"]]
    assert coeffs == [7.2, 3.0, 1.5]


def test_sort_by_popularity_key_missing():
    """ Проверка если у товара вообще нет ключа – считаем None """
    data = {"misc": [
        {"name": "no_key"},
        {"name": "with_key", "popularity_coefficient": 5.0},
    ]}

    sorted_data = sort_by_popularity(data)
    names = [p["name"] for p in sorted_data["misc"]]
    assert names == ["with_key", "no_key"]
