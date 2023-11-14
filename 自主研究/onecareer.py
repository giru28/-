import requests
import bs4
import datetime

# ログイン情報
username = "nogenora28@gmail.com"
password = "konosuba28"

# セッションの作成
session = requests.Session()

# ログイン処理
def login():
    response = session.get("https://www.onecareer.jp/users/sign_in?store_return_to=https%3A%2F%2Fwww.onecareer.jp%2F")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # CSRF トークンの取得
    csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']

    # ログインリクエスト
    response = session.post(
        "https://www.onecareer.jp/users/sign_in",
        data={
            "user[email]": username,
            "user[password]": password,
            "authenticity_token": csrf_token,
        },
    )
    if response.status_code == 200:
        return True
    else:
        return False

# 企業情報の取得
def get_company_info(company_name):
    response = session.get(f"https://www.onecareer.jp/company/{company_name}")
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return soup

# 企業の採用情報の取得
def get_recruitment_info(company_name):
    company_info = get_company_info(company_name)
    recruitment_info = company_info.find("div", class_="recruitment_info")
    return recruitment_info

# エントリーシートの作成
def create_es(company_name, position_name):
    recruitment_info = get_recruitment_info(company_name)
    es_template = recruitment_info.find("div", class_="es_template")
    es = es_template.text.replace("{会社名}", company_name).replace("{職種名}", position_name)
    return es

# 面接対策の練習
def practice_interview(company_name, position_name):
    recruitment_info = get_recruitment_info(company_name)
    interview_questions = recruitment_info.find_all("div", class_="interview_question")
    for question in interview_questions:
        print(f"Q: {question.text}")
        answer = input("A: ")
        print()

# メイン処理
def main():
    # ログイン
    if login():
        # 企業名と職種名の入力
        company_name = input("企業名を入力してください: ")
        position_name = input("職種名を入力してください: ")

        # 企業情報の取得
        company_info = get_company_info(company_name)
        print(company_info.text)

        # 採用情報の取得
        recruitment_info = get_recruitment_info(company_name)
        print(recruitment_info.text)

        # エントリーシートの作成
        es = create_es(company_name, position_name)
        print(es)

        # 面接対策の練習
        practice_interview(company_name, position_name)
    else:
        print("ログインに失敗しました。")

if __name__ == "__main__":
    main()
