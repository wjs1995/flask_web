from flask import Blueprint, render_template, request, abort, flash, url_for, redirect
from flask_login import login_required

from models import Question
from qa.forms import WriteQuestionForm

qa = Blueprint('qa', __name__, template_folder='templates', static_folder='../assets')


@qa.route('/')
def index():
    return render_template('index.html')


@qa.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = WriteQuestionForm()
    if form.validate_on_submit():
        try:
            que_obj = form.save()
            if que_obj:
                flash('发布成功', 'success')
                return redirect(url_for('qa.index'))
        except Exception as e:
            print(e)
            flash('发布失败', 'danger')
    return render_template('write.html', form=form)


@qa.route('/follow')
def follow():
    # 关注
    per_page = 20
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).paginate(page=page, per_page=per_page)
    return render_template('follow.html', page_data=page_data)


@qa.route('/detail/<int:q_id>')
def detail(q_id):
    question = Question.query.get(q_id)
    if not question.is_valid:
        abort(404)
    answer = question.answer_list.filter_by(is_valid=True).first()
    return render_template('detail.html', question=question, answer=answer)
