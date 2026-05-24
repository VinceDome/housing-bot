import requests, os

dirs = ["data", "data/diffs"]
pages = {"geste":"https://www.geste-students.nl/", "5huizen":"https://5huizenvastgoedbeheer.nl/#/student-housing", "roomplaza":"https://www.roomplaza.com/en/html/web/search/home?city=3&startDate=2026-08-01"}

for i in dirs:
    #creates folder structure
    if not os.path.exists(i):
        os.mkdir(i)

    #creates files
    for a in pages.keys():
        with open(f"{i}/{a}.txt", "a+") as f:
            pass


def pageUpdate():
    status = []
    for name, url in pages.items():
        print(name)
        file_path = f"data/{name}.txt"

        session = requests.Session()
        page = session.get(url)
        current_page = page.text.strip()

        # Read previous content if it exists

        with open(file_path, "r", encoding="utf-8") as f:
            old_page = f.read().strip()

        # First run or page changed

        if old_page != current_page:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(current_page)

            #save the difference
            with open("data/diffs/" + name + ".txt", "w", encoding="utf-8") as f:
                f.write(old_page + "\n\n\n\n\n\n\n\n" + current_page)

            
            status.append(name)

    return status
        

