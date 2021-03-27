import universities

uni = universities.API() # can specify encoding for use in Python 2

def search_by_country(country):
    search = uni.search(country=country)
    data = []
    for item in search:
        data.append(item)
    return data

def get_countries():
    all_data = uni.get_all()
    countries = []
    for item in all_data:
        if not item.country.lower() in countries:
            countries.append(item.country.lower())
    return countries

def search_by_univ(univ):
    search = uni.search(name=univ)
    data = []
    for item in search:
        data.append(item)
    return data[0]

def get_universities():
    all_data = uni.get_all()
    univ_name = []
    for item in all_data:
        if not item.name.lower() in univ_name:
            univ_name.append(item.name.lower())
    return univ_name