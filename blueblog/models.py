
from datetime import datetime
# 使用拓展列表说明拓展内容

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from blueblog.extensions import db
#! 注意 sqlchemy 不可以不全相关的内容.


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    # 生成password的hash值
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # 检查password_hash是否有效.
    def vaildate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    #* 建立双向一对多关系,back_populates='多关系的关系名'
    posts = db.relationship('Post', back_populates='category')
    # 当删除一个类别,当前类别的所有文章都被重置为默认的类别
    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integerm, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.Datetime, default=datetime.uctnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)
    # 设置外键
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 设置双向一对多关系
    category = db.relationship('Category', back_populates='posts')
    #  设置级联删除,如果文章被删除,则相关的所有评论均被删除
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    # 确定是否属于 admin的评论
    from_admin = db.Column(db.Boolean, default=False)
    # 确保管理员审查后才可以发布
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # 评论的回复
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 文章的外键
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    
class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
    