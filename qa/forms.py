import os

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, DataRequired
from werkzeug.utils import secure_filename
from wtforms import FileField, StringField, TextAreaField
from wtforms.validators import Length
from flask_ckeditor import CKEditorField

from models import Question, db, QuestionTags


class WriteQuestionForm(FlaskForm):
    img = FileField(label='上传图片', render_kw={
        "accept": ".jpeg, .jpg, .png"
    }, validators=[FileAllowed(['jpg', 'png', 'jpeg'], '请选择合适的图片类型')])

    title = StringField(label='标题', render_kw={
        'class': "form-control",
        'placeholder': '请输入标题（最多50个字）'
    }, validators=[DataRequired('请输入标题'), Length(min=2, max=50, message='标题长度2-50')])

    tags = StringField(label='标签', render_kw={
        'class': "form-control",
        'placeholder': '输入标签，用,分隔'
    }, validators=[])

    desc = TextAreaField(label='描述', render_kw={
        'class': "form-control",
        'placeholder': '简述'
    }, validators=[])

    content = CKEditorField(label='文章内容', render_kw={
        'class': "form-control",
        'placeholder': '请输入正文',
    }, validators=[DataRequired('请输入正文'), Length(min=5, message='标题长度2-50')])

    def save(self):
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        img = self.img.data
        img_name = ''
        if img:
            print('img:', img)
            img_name = secure_filename(img.filename)
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        que_obj = Question(title=title, desc=desc, img=img_name, content=content, user=current_user)
        db.session.add(que_obj)
        tags = self.tags.data
        for tag in tags.split('，'):
            if tag:
                tag_obj = QuestionTags(tag_name=tag, question=que_obj)
                db.session.add(tag_obj)
        db.session.commit()

        return que_obj
