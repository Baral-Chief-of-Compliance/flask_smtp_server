from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
from io import TextIOWrapper
import db_tools


load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
APP_PASS_MAIL = os.getenv("APP_PASS_MAIL")
TO_ZAN_CHECK_MAIL = os.getenv("TO_ZAN_CHECK_MAIL")
TO_MAIL_CHECK_MAIL = os.getenv("TO_MAIL_CHECK_MAIL")
TO_MAIL_CHECK_ADMIN = os.getenv("TO_MAIL_CHECK_ADMIN")

recipients = [TO_EMAIL, TO_ZAN_CHECK_MAIL, TO_MAIL_CHECK_MAIL, TO_MAIL_CHECK_ADMIN]

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/API/v1.0/example_vacancy_registration", methods=['GET',])
def get_example_vacancy_registration():
    if request.method == 'GET':
        return send_file("upload/exampleVacancyRegistration.xlsx", download_name="Пример заполнения таблицы.xlsx")
    

@app.route("/API/v1.0/policy_personal_data", methods=['GET',])
def get_policy_data():
    if request.method == 'GET':
        return send_file("upload/policyPD.pdf", download_name="Политика о персональных данных ГОБУ ЦЗН Мурманской области.pdf", as_attachment=True)


@app.route("/API/v1.0/anketa_soiskatel", methods=['POST',])
def send_anketa_soiskatel():

    if request.method == "POST":
        surname = request.form.get("surname")
        name =  request.form.get("name")
        patronymic =  request.form.get("patronymic")
        age =  request.form.get("age")
        email =  request.form.get("email")
        mailArea =  request.form.get("mailArea")
        mailRegistration = request.form.get("mailRegistration")
        mobilePhone =  request.form.get("mobilePhone")
        dreamJob =  request.form.get("dreamJob")
        family =  request.form.get("family")
        childrens =  request.form.get("childrens")
        education =  request.form.get("education")
        nameInstitution =  request.form.get("nameInstitution")
        possibilityOfRelocation =  request.form.get("possibilityOfRelocation")
        needForHousing =  request.form.get("needForHousing")
        desiredSalaryLevel =  request.form.get("desiredSalaryLevel")
        generalExperience =  request.form.get("generalExperience")
        positionAtLastJob =  request.form.get("positionAtLastJob")
        additionalInf =  request.form.get("additionalInf")
        summary = request.files["summary"]
    
        db_tools.update_soiskatel_number()
        anket_number = db_tools.get_soiskatel_number()

        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"Анкета соискателя Сайт Курс на Север! {anket_number}"

        body = f"""
        Фамилия: {surname}\n
        Имя: {name}\n
        Отчество: {patronymic}\n
        Возраст: {age}\n
        Электронный адрес: {email}\n
        Почтовый адрес: {mailArea}\n
        Адрес регистрации: {mailRegistration}\n
        Номер телефона: {mobilePhone}\n
        Желаемая профессия: {dreamJob}\n
        Семейное положение: {family}\n
        Дети: {childrens}\n
        Образование: {education}\n
        Наименование учебного заведения: {nameInstitution}\n
        Возможность переезда в Мурманскую область: {possibilityOfRelocation}\n
        Необходимость жилья: {needForHousing}\n
        Желаемый уровень заработной платы: {desiredSalaryLevel}\n
        Общий стаж: {generalExperience}\n
        Должность на последнем месте работы: {positionAtLastJob}\n
        Дополнительная информация: {additionalInf}\n
        """

        msg.attach(MIMEText(body, 'plain'))

        if summary != "":

            part = MIMEBase('application', 'octet-stream')

            part.set_payload(summary.read())
            encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment; filename="summary.pdf"')

            msg.attach(part)

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)

        server.login(FROM_EMAIL, APP_PASS_MAIL)


        text = msg.as_string()
        server.sendmail(FROM_EMAIL, recipients, text)
        server.quit()


        msg_for_sender = MIMEMultipart()
        msg_for_sender['From'] = FROM_EMAIL
        msg_for_sender['To'] = email
        msg_for_sender['Subject'] = "Спасибо за участие в программе Курс на Север!"

        body = f'''
Ваше обращение зарегистрировано под номером {anket_number}\n
Это автоматическая рассылка. Пожалуйста, не надо отвечать на это письмо.
        '''

        msg_for_sender.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)

        server.login(FROM_EMAIL, APP_PASS_MAIL)

        text = msg_for_sender.as_string()
        server.sendmail(FROM_EMAIL, email, text)
        server.quit()


        return "Status OK", 200
    else: 
        return "Method Not Allowed", 405
    

@app.route("/API/v1.0/anketa_employer", methods=['POST',])
def send_anketa_employer():
    if request.method == "POST":
        nameCompany = request.form.get("nameCompany")
        Address = request.form.get('Address')
        Vacancies = request.files["Vacancies"]
        contact = request.form.get("contact")
        phoneNumber = request.form.get("phoneNumber")
        email = request.form.get("email")
        CompanyCard = request.files["CompanyCard"]

        db_tools.update_employer_number()
        anket_number = db_tools.get_employer_number()

        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = f"Анкета работодателя Сайт Курс на Север! {anket_number}"

        body = f"""
        Полное наименование: {nameCompany}\n
        Юридеский адрес: {Address}\n
        ФИО контактного лица: {contact}\n
        Номер телефона: {phoneNumber}\n
        Электронная почта: {email}\n
        """

        msg.attach(MIMEText(body, 'plain'))

        if Vacancies != "":
            part = MIMEBase('application', 'octet-stream')

            part.set_payload(Vacancies.read())
            encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment; filename="vacancies.xls"')

            msg.attach(part)

        if CompanyCard != "":
            part = MIMEBase('application', 'octet-stream')

            part.set_payload(CompanyCard.read())
            encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment; filename="CompanyCard.pdf"')

            msg.attach(part)


        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)

        server.login(FROM_EMAIL, APP_PASS_MAIL)


        text = msg.as_string()
        server.sendmail(FROM_EMAIL, recipients, text)
        server.quit()

        msg_for_sender = MIMEMultipart()
        msg_for_sender['From'] = FROM_EMAIL
        msg_for_sender['To'] = email
        msg_for_sender['Subject'] = "Спасибо за участие в программе Курс на Север!"

        body = f'''
Ваше обращение зарегистрировано под номером {anket_number}\n
Это автоматическая рассылка. Пожалуйста, не надо отвечать на это письмо.
        '''

        msg_for_sender.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)

        server.login(FROM_EMAIL, APP_PASS_MAIL)

        text = msg_for_sender.as_string()
        server.sendmail(FROM_EMAIL, email, text)
        server.quit()

        return "Status Ok", 200
    else:
        return "Method Not Allowed", 405

if __name__ == "__main__":
    app.run(host='0.0.0.0')