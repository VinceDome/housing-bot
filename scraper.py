import requests, os, difflib, textwrap, smtplib, ssl, json
from email.message import EmailMessage
from bs4 import BeautifulSoup

platforms = {"geste":"https://www.geste-students.nl/", "5huizen":"https://api.5huizenvastgoedbeheer.nl/v2/buildings", "roomplaza":"https://www.roomplaza.com/en/html/web/search/home?city=3&startDate=2026-08-01", "plaza":"https://mosaic-plaza-aanbodapi.zig365.nl/api/v1/actueel-aanbod?limit=60&locale=en_GB&page=0&sort=%2BreactionData.aangepasteTotaleHuurprijs", "room":"https://roommatching-aanbodapi.zig365.nl/api/v1/actueel-aanbod?limit=30&locale=en_GB&page=0&sort=%2BreactionData.aangepasteTotaleHuurprijs"}

plaza_payload = {"filters":{"$and":[{"$and":[{"regio.id":{"$eq":"12"}},{"land.id":{"$eq":"524"}}]}]}, "hidden-filters":{"$and":[{"dwellingType.categorie":{"$eq":"woning"}},{"rentBuy":{"$eq":"Huur"}},{"isExtraAanbod":{"$eq":""}},{"isWoningruil":{"$eq":""}},{"$and":[{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]},{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]}]}]}}
room_payload = {"filters":{"$and":[{"$and":[{"city.id":{"$eq":"4"}},{"municipality.id":{"$eq":"23"}},{"regio.id":{"$eq":"1"}}]},{"$or":[{"model.modelCategorie.id":{"$eq":"3"}},{"model.modelCategorie.id":{"$eq":"2"}}]}]},"hidden-filters":{"$and":[{"dwellingType.categorie":{"$eq":"woning"}},{"rentBuy":{"$eq":"Huur"}},{"isExtraAanbod":{"$eq":""}},{"isWoningruil":{"$eq":""}},{"$and":[{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]},{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]}]}]}}

def CreateFileStructure():
    dirs = ["data", "data/diffs", "data/settings"]

    for i in dirs:
        #creates folder structure
        if not os.path.exists(i):
            os.mkdir(i)

        if i == "data/diffs":
            #creates files
            for a in platforms.keys():
                #normal data files
                    if not os.path.exists(i+"/"+a):
                        os.mkdir(i+"/"+a)

                    for e in ["old", "new"]:
                        with open(f"{i}/{a}/{e}.txt", "a+") as f:
                            pass
        elif i == "data/settings":
            with open(f"{i}/mailcreds.txt", "a+") as f:
                pass
            

def WholePageUpdate():
    status = []
    for name, url in platforms.items():
        
        newfilepath = f"data/diffs/{name}/new.txt"
        oldfilepath = f"data/diffs/{name}/old.txt"

        session = requests.Session()
        if name == "plaza":
            page = session.post(url, json=plaza_payload)
            response = json.loads(page.text)

            #total_search_count
            current_page = str(response["_metadata"]["total_search_count"])

        elif name == "geste":
            page = session.get(url)
            page = page.text
            soup = BeautifulSoup(page, "html.parser")
            
            #block-block-9 --> a --> value
            current_page = soup.find_all(id="block-block-9")[0].a.text

        elif name == "room":
            page = session.post(url, json=room_payload)
            response = json.loads(page.text)

            #total_search_count
            current_page = str(response["_metadata"]["total_search_count"])   

        else:
            page = session.get(url)
            current_page = page.text

        # Read previous content if it exists

        with open(newfilepath, "r", encoding="utf-8") as f:
            old_page = f.read()

        # First run or page changed

        if old_page != current_page:
            with open(newfilepath, "w", encoding="utf-8") as f:
                f.write(current_page)

            with open(oldfilepath, "w", encoding="utf-8") as f:
                f.write(old_page)

            status.append(name)

    return status


def Diff(platform):
    with open(f"data/diffs/{platform}/old.txt", "r", encoding="utf-8") as f:
        old_page = f.read()

    with open(f"data/diffs/{platform}/new.txt", "r", encoding="utf-8") as f:
        new_page = f.read()


    d = difflib.ndiff(textwrap.wrap(old_page), textwrap.wrap(new_page))

    
    final = ""
    for a in d:
        if not a.startswith("   ") and not a.startswith("  ") and not a.startswith(" ") and a != "\n" and a != "":
            final+=("\n"+a)

    return "```"+final+"```"

def SendMail(subject, content):
    with open("data/settings/mailcreds.txt", "r", encoding="utf-8") as f:
        creds = f.read().strip().split("\n")

    if len(creds) != 3:
        return None
    
    sender, password, recipient = creds
    context = ssl.create_default_context()
       
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(sender, password)
        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(content)

        server.send_message(msg)