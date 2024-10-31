from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    generated_text = ""

    if request.method == 'POST':
        text = request.form['text']
        text = text.strip()
        text = text.replace('\n', ' ')

        questions = text.split("?")

        if not questions:  # Проверка на пустой список
            return render_template('mainpage.html', generated_text="Ошибка: пожалуйста, введите вопрос.")

        generated_text = ""
        for question in questions:
            # Обработайте каждый вопрос отдельно
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch

            DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

            model_name = "sberbank-ai/rugpt3large_based_on_gpt2"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name).to(DEVICE)

            input_ids = tokenizer.batch_encode_plus(
                [question],  # Передаем вопрос в модель
                add_special_tokens=True,
                return_tensors="pt",
                padding="longest",
                truncation=True,
            )['input_ids'].to(DEVICE)
            attention_mask = tokenizer(question, return_tensors="pt")['attention_mask'].to(DEVICE)

            if len(attention_mask[0]) != len(input_ids[0]):
                print("Ошибка: attention_mask не соответствует input_ids")
                return render_template('mainpage.html', generated_text="Ошибка")

            out = model.generate(
                input_ids,
                attention_mask=attention_mask,
                do_sample=True,
                temperature=1.3,
                top_k=20,
                top_p=0.8,
                max_length=50,
                no_repeat_ngram_size=2,
                repetition_penalty=1.2,
            )
            generated_text += question + " " + list(map(tokenizer.decode, out))[0].replace('<s>', '') + " "

    return render_template('mainpage.html', generated_text=generated_text)

@app.route('/')
def question():
    return render_template('question.html')


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term'].lower()
    search_results = []

    # Забираем текст из всех блоков 'container'
    with open('templates/question.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    for container in html_content.split('<div class="container"'):
        if search_term in container.lower():
            # Извлечение текста из блока
            start_index = container.find('>') + 1  # Найти начало текста
            end_index = container.rfind('<')  # Найти конец текста
            extracted_text = container[start_index:end_index].strip()
            search_results.append(extracted_text)

    # Проверка на пустой список
    if not search_results:
        return render_template('search.html', search_results=None)  # Передаем None

    return render_template('search.html', search_results=search_results)

