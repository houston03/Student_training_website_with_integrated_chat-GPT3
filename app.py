from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = "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"

'''
@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    generated_text = ""

    if request.method == 'POST':
        text = request.form['text']
        text = text.strip()
        text = text.replace('\n', ' ')

        questions = text.split("?")

        if not questions:  
            return render_template('mainpage.html', generated_text="Ошибка: пожалуйста, введите вопрос.")

        generated_text = ""
        for question in questions:
            question = question.strip()
            if not question:
                continue  
            try:
                # Отправка запроса к API
                response = requests.post(
                    "https://api-inference.huggingface.co/models/google/gemma-2-2b-it",
                    headers={'Authorization': f'Bearer {api_key}'},
                    json={'inputs': question}
                )
                response.raise_for_status()

              
                answer = response.json()
                if isinstance(answer, list) and len(answer) > 0:
                 
                    generated_text += answer[0]['generated_text'].replace(question, '').strip() + " "
                else:
                    generated_text += "Ошибка: нет ответа. " 

            except requests.exceptions.HTTPError as err:
                print(f"Ошибка: {err}")
                return render_template('mainpage.html', generated_text="Ошибка: не удалось получить ответ от API.")

    return render_template('mainpage.html', generated_text=generated_text)
'''


@app.route('/')
def question():
    return render_template('question.html')


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term'].lower()
    search_results = []


    with open('templates/question.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    for container in html_content.split('<div class="container"'):
        if search_term in container.lower():
    
            start_index = container.find('>') + 1  
            end_index = container.rfind('<')  
            extracted_text = container[start_index:end_index].strip()
            search_results.append(extracted_text)


    if not search_results:
        return render_template('search.html', search_results=None) 

    return render_template('search.html', search_results=search_results)

