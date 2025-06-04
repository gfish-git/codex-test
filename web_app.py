from flask import Flask, render_template_string, request
from email_assistant import EmailAssistant, DUMMY_EMAILS

app = Flask(__name__)
assistant = EmailAssistant()

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Email Assistant Demo</title>
    <style>
        body {font-family: Arial, sans-serif;}
        .container {display: flex;}
        .left {margin-right: 20px;}
        .emails {border: 1px solid #ccc; padding: 10px; width: 70%;}
        pre {background: #f4f4f4; padding: 5px;}
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
            {% for item in results %}
                <pre>{{item}}</pre>
            {% endfor %}
            {% if not results %}
                <p>Press Go to process emails.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        for email in DUMMY_EMAILS:
            actions = assistant.process_email(email)
            result_lines = [f"From: {email.sender}", f"Subject: {email.subject}"]
            for act in actions:
                if act[0] == 'labelEmail':
                    _, label, color, priority = act
                    result_lines.append(f"labelEmail({label}, {color}, {priority})")
                elif act[0] == 'draftReply':
                    _, body = act
                    result_lines.append(f"draftReply: {body}")
                elif act[0] == 'archiveEmail':
                    result_lines.append('archiveEmail()')
            results.append('\n'.join(result_lines))
    return render_template_string(HTML_PAGE, results=results)

if __name__ == '__main__':
    app.run(debug=True)
