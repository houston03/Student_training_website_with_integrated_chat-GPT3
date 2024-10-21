from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    generated_text = ""

    if request.method == 'POST':
        text = request.form['text']
        text = text.strip()  # Убираем лишние пробелы
        text = text.replace('\n', ' ')  # Заменяем переводы строк на пробелы

        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model_name = "sberbank-ai/rugpt3large_based_on_gpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name).to(DEVICE)

        input_ids = tokenizer.batch_encode_plus(
            [text],
            add_special_tokens=True,
            return_tensors="pt",
            padding="longest",
            truncation=True,
        )['input_ids'].to(DEVICE)
        attention_mask = tokenizer(text, return_tensors="pt")['attention_mask'].to(DEVICE)

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
        )
        generated_text = list(map(tokenizer.decode, out))[0]


    return render_template('mainpage.html', generated_text=generated_text)


@app.route('/')
def question():
    return render_template('question.html')


if __name__ == '__main__':
    app.run(debug=True)