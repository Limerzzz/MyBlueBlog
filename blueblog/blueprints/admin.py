
import os

from flask import render_template,redirect,url_for,Blueprint,flash,current_app,request
from flask_login import login_required, current_user
from flask_ckeditor import upload_success, upload_fail

from blueblog.extensions import db
from blueblog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from blueblog.models import  Post, Category, Comment, Link, Admin
from blueblog.utils import redirect_back, allowed_file

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))        
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form = form)

@admin_bp.route('/post/manage')
def manage_post():
    form = PostForm()    # 如果 request对象没有相应的args的话,默认值为 1 
    page = request.args.get('page', 1, type = int) 
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page = per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html',pagination = pagination, posts=posts)
@admin_bp.route('/post/new', mothods = ['GET' , 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.body = form.body.data
        post.title = form.title.data
        post.category = Category.query.get(form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form = form)
@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        # Update 的操作很简单只需要将数据赋值,而后提交
        post.body = form.body.data
        post.name = form.name.data
        post.author = form.author.data
        db.session.commit()
    form.body.data = post.body
    form.name.data = post.name
    form.author.data = post.author
    return render_template('admin/edit_post.html', form=form)
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.delete()
    return render_template('admin/manage_post.html')

@admin_bp.route('/category/manage')
def manage_category():
    form = CategoryForm()
    # 如果 request对象没有相应的args的话,默认值为 1 
    page = request.args.get('page', 1, type = int) 
    per_page = current_app.config['BLUELOG_category_PER_PAGE']
    pagination = Category.query.order_by(Category.timestamp.desc()).paginate(page, per_page = per_page)
    categories = pagination.items
    return render_template('admin/manage_category.html',pagination = pagination, categories=categories)
@admin_bp.route('/category/new', methods = ['GET' , 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name = name)
        db.session.add(category)
        db.session.commit()
        flash('Category created', 'success')
        return redirect(url_for('blog.show_category'), category_id = category.id)
    return render_template('/admin/new_category.html', form = form)
@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        # Update 的操作很简单只需要将数据赋值,而后提交
        category.name = form.name.data
        db.session.commit()
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)
@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    if category_id is 1:
        pass
        # flash('You can't delete default category ', 'warning')
    category = Category.query.get_or_404(category_id)
    category.delete()
    return render_template('admin/manage_category.html')


@admin_bp.route('/link/manage')
def manage_link():
    # 如果 request对象没有相应的args的话,默认值为 1 
    page = request.args.get('page', 1, type = int) 
    per_page = current_app.config['BLUELOG_link_PER_PAGE']
    pagination = Link.query.all().paginate(page, per_page = per_page)
    links = pagination.items
    return render_template('admin/manage_link.html',pagination = pagination, links=links)
@admin_bp.route('/link/new', methods = ['GET' , 'POST'])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.name.data
        link = Link(name = name, url = url)
        db.session.add(link)
        db.session.commit()
        flash('Link created', 'success')
        return redirect(url_for('blog.show_Link'), link_id = link.id)
    return render_template('/admin/new_link.html', form = form)
@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        # Update 的操作很简单只需要将数据赋值,而后提交
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
    form.name.data = link.name
    form.url.data = link.url
    return render_template('admin/edit_link.html', form=form)
@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
def delete_link(link_id):   
    link = Link.query.get_or_404(link_id)
    link.delete()
    return render_template('admin/manage_link.html')    


@admin_bp.route('/comment/manege')
def manege_comment():   
    # 如果 request对象没有相应的args的话,默认值为 1 
    page = request.args.get('page', 1, type = int) 
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Comment.query.order_by(Post.timestamp.desc()).paginate(page, per_page = per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html',pagination = pagination, comments=comments)