#!/usr/bin/env python
# encoding: utf-8

"""
@author: 水痕
@contact: 332904234@qq.com
@file: schema.py
@time: 2018/2/25 16:23
@desc:
"""
import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Blog


class UserType(DjangoObjectType):
    class Meta:
        model = User


class BlogType(DjangoObjectType):
    class Meta:
        model = Blog


# 定义动作，类似POST, PUT, DELETE
class UserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    gender = graphene.String(required=True)


class BlogInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    user = graphene.Int(required=True)
    content = graphene.String(required=True)


# 定义一个创建user的mutation
class CreateUser(graphene.Mutation):
    # api的输入参数
    class Arguments:
        user_data = UserInput(required=True)

    # api的响应参数
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    # api的相应操作，这里是create
    def mutate(self, info, user_data):
        user = User.objects.create(name=user_data['name'], gender=user_data['gender'])
        ok = True
        return CreateUser(user=user, ok=ok)


# 定义一个创建博客的mutation
class CreateBlog(graphene.Mutation):
    class Arguments:
        blog_data = BlogInput(required=True)

    blog = graphene.Field(BlogType)

    def mutate(self, info, blog_data):
        # 插入到数据库中
        blog = Blog.objects.create(title=blog_data['title'], user_id=blog_data['user'], content=blog_data['content'])
        return CreateBlog(blog=blog)

# 定义一个查询语句
class Query(object):
    all_user = graphene.List(UserType)
    all_blog = graphene.List(BlogType)

    def resolve_all_user(self, info, **kwargs):
        # 查询所有book的逻辑
        return User.objects.all()

    def resolve_all_blog(self, info, **kwargs):
        # 查询所有title的逻辑
        return Blog.objects.all()
