from models import *
from connectdatabase import ConnectDatabase
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


def init_db():
    ConnectDatabase.db.drop_tables([UserStory], safe=True)
    ConnectDatabase.db.create_tables([UserStory], safe=True)


@app.route('/')
@app.route('/list', methods=['GET'])
def list_stories():
    stories = UserStory.select()
    return render_template('list.html', user_stories=stories)


@app.route('/form', methods=["GET"])
def show_form():
    new = True
    return render_template('form.html', u_story=0, button="Create")


@app.route('/story/', methods=['POST'])
def add_new_story():
    user_story = UserStory.create(story_title=request.form['story_title'],
                                  user_story=request.form['user_story'],
                                  acceptance_criteria=request.form['acceptance_criteria'],
                                  business_value=request.form['business_value'],
                                  estimation=request.form['estimation'],
                                  status=request.form['status'])

    return redirect(url_for('list_stories'))


@app.route("/story/<story_id>", methods=["GET"])
def show_edit(story_id):
    new = False
    story = UserStory.get(UserStory.id == story_id)
    return render_template('form.html', u_story=story, button="Update")


@app.route('/story/<story_id>', methods=['POST'])
def update_story(story_id):
    update = UserStory.update(story_title=request.form["story_title"],
                              user_story=request.form["user_story"],
                              acceptance_criteria=request.form["acceptance_criteria"],
                              business_value=request.form["business_value"],
                              estimation=request.form["estimation"],
                              status=request.form["status"]).where(UserStory.id == story_id)
    update.execute()
    return redirect(url_for('list_stories'))


@app.route('/delete/<story_id>', methods=['POST'])
def delete_story(story_id):
    story = UserStory.select().where(UserStory.id == story_id).get()
    story.delete_instance()
    story.save()
    return redirect(url_for('list_stories'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
