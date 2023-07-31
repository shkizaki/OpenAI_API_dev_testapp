import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import openai

app = Flask(__name__)

# OpenAI APIキーを設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# レスポンスの最大トークン数を指定
max_tokens = 256

# 過去の会話履歴を保持するリスト
conversation = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patient_input = request.form['input']

        # 会話履歴にユーザーの入力を追加
        conversation.append({"role": "user", "content": patient_input})

        # 医者としての振る舞いを設定（会話履歴の長さが偶数の場合医者としてのメッセージを追加する）
        if len(conversation) % 2 == 0:
            conversation.append({"role": "system", "content": "患者の病状を聞いて、適切なアドバイスをしてください。"})

        # OpenAI APIによる回答を取得
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.7,  # temperatureを0.7に設定して回答のランダム性を制御
            max_tokens=max_tokens,
        )

        # ユーザーの入力とAIドクターの回答を保持
        conversation.append({"role": "system", "content": response['choices'][0]['message']['content'].strip()})
        reply = conversation[-1]['content']

        # レスポンス全体をHTMLに出力
        return render_template('index.html', conversation=conversation, reply=reply)
    else:
        return render_template('index.html', conversation=conversation)

@app.route('/reset', methods=['POST'])
def reset():
    # 会話履歴を空にする
    global conversation
    conversation = []
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
