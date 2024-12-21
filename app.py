from flask import Flask, render_template, request, redirect, url_for, Markup,  jsonify, abort
import markdown2
import bleach

SECRET_KEY = "hr2fM:b[1Tt3wPP"

ALLOWED_TAGS = [
    'b', 'i', 'u', 'em', 'strong', 'p', 'ul', 'ol', 'li',
    'blockquote', 'code', 'pre', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
]

app = Flask(__name__)

pages = [
    {"title": "Checkpoint 4", "link": "/whydiary/page/154", "content": Markup("Thank you. I knew I can trust you.<br> Thank you for being my friend. Thank you for saving my life.")},
    {"title": "I'm tired", "link": "/whydiary/page/1", "content": Markup("I am tired of all this, all I have been given is hate. I can't do this, I'm sorry.")},
    {"title": "What's wrong?", "link": "/whydiary/page/2", "content": Markup("I am not good enough. Everyone is better than me. What am I doing wrong? Can you help me?")},
    {"title": "Help me..", "link": "/whydiary/page/3", "content": Markup("....- ...-- -.... ---.. -.... ..... -.... ...-- -.... -... --... ----- -.... ..-. -.... ----. -.... . --... ....- ..--- ----- ...-- ..--- ...-- .- ..--- ----- ....- -.. --... ----. ..--- ----- -.... -.-. -.... ----. -.... -.... -.... ..... ..--- ----- ..--- ..--- ..... ..--- -.... ..... -.... -.... -.... -.-. -.... ..... -.... ...-- --... ....- -.... ..... -.... ....- ..--- ..--- ..--- ----- -.... ..--- -.... ..... -.... -.... -.... ..-. --... ..--- -.... ..... ..--- ----- -.... -.. --... ----. ..--- ----- -.... ..... --... ----. -.... ..... --... ...-- ..--- .")},
]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/whydiary')
def diary():
    visible_pages = [page for page in pages if page["link"] != "/whydiary/page/154"]
    return render_template('diary.html', pages=visible_pages)

@app.route('/whydiary/page/<int:page_id>')
def view_page(page_id):
    if 0 <= page_id < len(pages):
        page = pages[page_id]
        return render_template('page.html', title=page["title"], content=page.get("content", ""))

    if page_id == 154:
        page = pages[0]
        return render_template('page.html', title=page["title"], content=page["content"])

    return "Page not found", 404


@app.route('/whydiary/page/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        raw_title = request.form.get('title', 'Untitled')
        raw_body = request.form.get('body', '')

        sanitized_body = bleach.clean(raw_body, tags=ALLOWED_TAGS, strip=True)
        rendered_body = markdown2.markdown(sanitized_body)

        new_page = {
            "title": raw_title,
            "link": f"/whydiary/page/{len(pages)}",
            "content": Markup(rendered_body)
        }
        pages.append(new_page)

        return redirect(url_for('diary'))

    return render_template('create.html')

@app.route('/api/checkpoint3')
def get_checkpoint3_flag():
    secret = request.headers.get("X-Header")
    if secret != SECRET_KEY:
        abort(403)
    return jsonify({"checkpoint_3": "There is a hidden page. (maybe 200)"})




if __name__ == '__main__':
    app.run(debug=True)
