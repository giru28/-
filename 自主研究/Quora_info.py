import json
import requests
from bs4 import BeautifulSoup as Soup
from datetime import datetime

def fetch_answers(my_url, output_file):
    req = requests.get(my_url)

    if req.status_code != 200:
        print("Error: URLを取得できません。")
        return

    page_soup = Soup(req.content, "html.parser")
    main_box = page_soup.findAll("script", {"type": "application/ld+json"})[0].text

    data = json.loads(main_box)
    question = data["mainEntity"]["name"]
    print("質問:")
    print(question)
    print("\n\n")

    answers = []

    try:
        accepted_answers = data["mainEntity"]["acceptedAnswer"]
        for i, answer in enumerate(accepted_answers):
            print(f"回答 #{i+1}:")
            print(answer["text"])
            print("\n\n")
            answers.append(answer["text"])
    except:
        pass

    try:
        suggested_answers = data["mainEntity"]["suggestedAnswer"]
        for i, answer in enumerate(suggested_answers):
            print(f"回答 #{i+1} (Suggested):")
            print(answer["text"])
            print("\n\n")
            answers.append(answer["text"])
    except:
        pass

    # テキストファイルに保存
    with open(output_file, "w", encoding="UTF-8") as f:
        f.write("質問:\n")
        f.write(question)
        f.write("\n\n")

        for i, answer in enumerate(answers):
            f.write(f"回答 #{i+1}:\n")
            f.write(answer)
            f.write("\n\n")

if __name__ == "__main__":
    my_url = input("QuoraのURLを入力してください: ")
    custom_filename = input("保存するファイル名を入力してください (例: my_data.txt): ")

    if not custom_filename.endswith(".txt"):
        custom_filename += ".txt"

    fetch_answers(my_url, custom_filename)
