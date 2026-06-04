import requests, os

dirs = ["data", "data/diffs"]
wholePages = {"geste":"https://www.geste-students.nl/", "5huizen":"https://api.5huizenvastgoedbeheer.nl/v2/buildings", "roomplaza":"https://www.roomplaza.com/en/html/web/search/home?city=3&startDate=2026-08-01", "plaza":"https://plaza.newnewnew.space/en/availables-places/living-place#?gesorteerd-op=prijs%2B&locatie=Nederland%2B-%2BZuid-Holland"}

for i in dirs:
    #creates folder structure
    if not os.path.exists(i):
        os.mkdir(i)
    
    #creates files
    for a in wholePages.keys():
        #normal data files
        if i == "data":
            with open(f"{i}/{a}.txt", "a+") as f:
                pass
        else:
            if not os.path.exists(i+"/"+a):
                os.mkdir(i+"/"+a)

            for e in ["old", "new"]:
                with open(f"{i}/{a}/{e}.txt", "a+") as f:
                    pass

def WholePageUpdate():
    status = []
    for name, url in wholePages.items():
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
            with open("data/diffs/"+name+"/old.txt", "w", encoding="utf-8") as f:
                f.write(old_page)

            with open("data/diffs/"+name+"/new.txt", "w", encoding="utf-8") as f:
                f.write(current_page)

            
            status.append(name)

    return status