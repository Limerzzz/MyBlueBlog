from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField,\
     BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from blueblog.models import Category

class LoginForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired(), Length(1,20)])
    password = StringField('Password', validators = [DataRequired(),Length(1,128)])
    remember_me = BooleanField('Remeber me')
    submit = SubmitField('Log in')

class SettingForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(1,70)])
    blog_title = StringField('Blog title', validators = [DataRequired(), Length(1, 60)])
    blog_sub_title = SelectField('Blog Sub Title', validators = [DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators = [DataRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired(), Length(1,60)])
    body = CKEditorField('Body', validators = [DataRequired()])
    submit = SubmitField()
    # 实现下拉选择的方法
    # 使用 coerce 关键字指定数据类型为整形. default 用来设置默认的选项值为1.
    category = SelectField('Category', coerce = int, default = 1)
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) 
                                    for categoty in Category.query.order_by(Category.name).all()]
    
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField()
    # 自定义含泪验证器
    def validate_name(self, field):
        if Category.query.filter_by(name = field.data).first():
            raise ValidationError('Name already in use.')

class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1,30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1,254)])
    # optional() 使得对应的字段可以为空.
    site = StringField('Site', validators=[Optional(), URL(), Length(0,255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()
# 继承自  CommentForm
class  AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()

class LinkForm(FlaskForm):
    name = StringField('Name', validators=[ DataRequired(), Length(1,30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1,255)])
    submit = SubmitField()
