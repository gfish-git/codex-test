from flask import Flask, render_template_string, request, redirect, url_for
from email_assistant import EmailAssistant, DUMMY_EMAILS

app = Flask(__name__)
assistant = EmailAssistant()

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Email Assistant Demo</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 40px;}
        .container {display: flex;}
        .left {margin-right: 20px;}
        .emails {display: flex; flex-direction: column; gap: 20px; width: 70%;}
        .email-card {border: 1px solid #ccc; padding: 15px; border-radius: 5px; background: #fafafa;}
        .email-header {font-weight: bold; margin-bottom: 10px;}
        textarea {width: 100%; height: 80px;}
        .actions {margin-top: 10px;}
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <form method="post">
                <button type="submit">Go</button>
            </form>
        </div>
        <div class="emails">
            {% for email in emails %}
            <div class="email-card">
                <div class="email-header">{{ email.sender }} &ndash; {{ email.subject }}</div>
                <div class="email-body">{{ email.body }}</div>
                {% if email.sent %}
                <em>Sent!</em>
                {% elif email.draft %}
                <form method="post" action="{{ url_for('send', index=loop.index0) }}">
                    <textarea name="reply">{{ email.draft }}</textarea>
                    <div class="actions">
                        <button type="submit">Send</button>
                    </div>
                </form>
                {% elif email.archived %}
                <em>Archived</em>
                {% endif %}
            </div>
            {% endfor %}
            {% if not emails %}
                <p>Press Go to process emails.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

processed_emails = []


@app.route('/', methods=['GET', 'POST'])
def index():
    global processed_emails
    if request.method == 'POST':
        processed_emails = []
        for email in DUMMY_EMAILS:
            actions = assistant.process_email(email)
            entry = {
                'sender': email.sender,
                'subject': email.subject,
                'body': email.body,
                'draft': None,
                'archived': False,
                'sent': False,
            }
            for act in actions:
                if act[0] == 'draftReply':
                    entry['draft'] = act[1]
                elif act[0] == 'archiveEmail':
                    entry['archived'] = True
            processed_emails.append(entry)
    return render_template_string(HTML_PAGE, emails=processed_emails)


@app.route('/send/<int:index>', methods=['POST'])
def send(index: int):
    global processed_emails
    if 0 <= index < len(processed_emails):
        processed_emails[index]['draft'] = request.form.get('reply', '')
        processed_emails[index]['sent'] = True
        # placeholder for sending logic
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
