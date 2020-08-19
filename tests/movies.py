from utils import apis

def main():
    api = apis.get_tmdb_api()
    search = api.Search()
    response = search.movie(query='Blade Runner')

    for result in search.results:
        print(result["title"])

if __name__ == "__main__":
    main()