import requests, os, difflib, textwrap, smtplib, ssl, json
from email.message import EmailMessage

platforms = {"geste":"https://www.geste-students.nl/", "5huizen":"https://api.5huizenvastgoedbeheer.nl/v2/buildings", "roomplaza":"https://www.roomplaza.com/en/html/web/search/home?city=3&startDate=2026-08-01", "plaza":"https://plaza.newnewnew.space/en/availables-places/living-place#?gesorteerd-op=prijs%2B&locatie=Nederland%2B-%2BZuid-Holland"}
platforms["plaza"] = "https://mosaic-plaza-aanbodapi.zig365.nl/api/v1/actueel-aanbod?limit=60&locale=en_GB&page=0&sort=%2BreactionData.aangepasteTotaleHuurprijs"
plaza_payload = {"filters":{"$and":[{"$and":[{"regio.id":{"$eq":"12"}},{"land.id":{"$eq":"524"}}]}]}, "hidden-filters":{"$and":[{"dwellingType.categorie":{"$eq":"woning"}},{"rentBuy":{"$eq":"Huur"}},{"isExtraAanbod":{"$eq":""}},{"isWoningruil":{"$eq":""}},{"$and":[{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]},{"$or":[{"street":{"$like":""}},{"houseNumber":{"$like":""}},{"houseNumberAddition":{"$like":""}}]}]}]}}

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
        else:
            page = session.get(url)
        
        current_page = page.text.strip()

        # Read previous content if it exists

        with open(newfilepath, "r", encoding="utf-8") as f:
            old_page = f.read().strip()

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
        old_page = f.read().strip()

    with open(f"data/diffs/{platform}/new.txt", "r", encoding="utf-8") as f:
        new_page = f.read().strip()


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