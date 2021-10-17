from article import Article
from database import Database
from flask import abort, flash, Flask, g, get_flashed_messages, jsonify, \
                  redirect, request, render_template, url_for
import json

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = b'lol'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

@app.route('/')
def index_page():
    articles = get_db().get_articles_index()
    return render_template('index.html', articles=articles)

@app.route('/article/<identifier>')
def article_page(identifier):
    article = get_db().get_article(identifier)
    if article is not None:
        return render_template('article.html', article=article)
    else:
        abort(404)

@app.route('/article/<identifier>/edit', methods=['POST', 'GET'])
def edit_article_page(identifier):
    article_db = get_db().get_article(identifier)

    if article_db is not None:
        if request.method == 'POST':
            article = Article()
            article.identifier = identifier
            validation = validate_edit_article(article, request.form)

            if validation.get('err') != {}:
                return json.dumps(validation)
            else:
                try:
                    get_db().update_article(article)
                    flash("L'article a été modifié.", 'success')
                    return json.dumps({'redirect': url_for('admin_page')})
                except Exception as e:
                    abort(500)
        elif request.method == 'GET':
            return render_template('article-edit.html', article=article_db)
    else:
        abort(404)

def validate_edit_article(article, form):
    err, ok = {}, {}

    try:
        article.title = form['title']
        ok['title'] = "Le titre est valide."
    except Exception as e:
        err['title'] = str(e)
    try:
        article.paragraph = form['paragraph']
        ok['paragraph'] = "Le paragraphe est valide."
    except Exception as e:
        err['paragraph'] = str(e)

    result = {'err': err, 'ok': ok}
    return result

@app.route('/admin')
def admin_page():
    articles = get_db().get_articles_admin()
    return render_template('admin.html', articles=articles)

@app.route('/admin-nouveau', methods=['POST', 'GET'])
def new_article_page():
    if request.method == 'POST':
        article = Article()
        validation = validate_new_article(article, request.form)

        if validation.get('err') != {}:
            return json.dumps(validation)
        else:
            try:
                get_db().insert_article(article)
                flash("L'article a été ajouté.", 'success')
                return json.dumps({'redirect': url_for('admin_page')})
            except Exception as e:
                abort(500)
    else:
        return render_template('article-new.html')

def validate_new_article(article, form):
    err, ok = {}, {}

    try:
        article.title = form['title']
        ok['title'] = "Le titre est valide."
    except Exception as e:
        err['title'] = str(e)
    try:
        article.identifier = form['identifier']
        validate_new_article_identifier(article.identifier)
        ok['identifier'] = "L'identifiant est valide."
    except Exception as e:
        err['identifier'] = str(e)
    try:
        article.author = form['author']
        ok['author'] = "L'auteur est valide."
    except Exception as e:
        err['author'] = str(e)
    try:
        article.publication_date = form['publication_date']
        ok['publication_date'] = "La date de publication est valide."
    except Exception as e:
        err['publication_date'] = str(e)
    try:
        article.paragraph = form['paragraph']
        ok['paragraph'] = "Le paragraphe est valide."
    except Exception as e:
        err['paragraph'] = str(e)

    result = {'err': err, 'ok': ok}
    return result

def validate_new_article_identifier(identifier):
    if not get_db().is_unique_identifier(identifier):
        raise Exception("L'identifiant est déjà utilisé. Veuillez en "
                        "choisir un autre.")
    else:
        return True

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        keywords = request.form['keywords']
        results = get_db().search_article(keywords)
        return render_template('results.html', results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')