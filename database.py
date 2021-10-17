from datetime import datetime
import sqlite3

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_article(self, identifier):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select titre, identifiant, auteur, date_publication, "
                        "paragraphe "
                        "from article "
                        "where identifiant=? "
                        "limit 1"), [identifier])
        article = cursor.fetchone()
        if article is None:
            return None
        else:
            return article

    def get_articles_index(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("select titre, identifiant, auteur, date_publication, " 
                       "paragraphe "
                       "from article "
                       "where date_publication < ? "
                       "order by date_publication desc "
                       "limit 5 "),
                       [datetime.today().strftime('%Y-%m-%d')])
        articles = cursor.fetchall()
        return articles

    def get_articles_admin(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select id, titre, identifiant, date_publication "
                       "from article")
        articles = cursor.fetchall()
        return articles

    def insert_article(self, article):
        if type(article).__name__ == 'Article':
            insert_data = (article.title, article.identifier,
                           article.author, article.publication_date,
                           article.paragraph)
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(("insert into article(titre, identifiant, auteur, "
                            "date_publication, paragraphe)"
                            "values(?, ?, ?, ?, ?)"), insert_data)
            connection.commit()
        else:
            raise Exception('La variable doit être de type Article.')

    def update_article(self, article):
        if type(article).__name__ == 'Article':
            update_data = (article.title, article.paragraph,
                           article.identifier)
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(("update article "
                            "set titre = ?, paragraphe = ? "
                            "where identifiant = ?"), update_data)
            connection.commit()
        else:
            raise Exception('La variable doit être de type Article.')

    def is_unique_identifier(self, identifier):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select id "
                       "from article "
                       "where identifiant=? "
                       "limit 1", [identifier])
        article = cursor.fetchone()

        if article is None:
            return True
        else:
            return False

    def search_article(self, keywords):
        search = ('%'+keywords+'%', '%'+keywords+'%')
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("select titre, identifiant, date_publication "
                       "from article "
                       "where titre like ? or paragraphe like ?", search)
        search_result = cursor.fetchall()
        return search_result