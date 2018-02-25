#!/usr/bin/env python
# encoding: utf-8

"""
@author: 水痕
@contact: 332904234@qq.com
@file: schema.py.py
@time: 2018/2/25 15:54
@desc:
"""
import graphene
import blog.schema


class Query(blog.schema.Query, graphene.ObjectType):
    # 总的Schema的query入口
    pass


class Mutations(graphene.ObjectType):
    # 总的Schema的mutations入口
    create_user = blog.schema.CreateUser.Field()
    create_blog = blog.schema.CreateBlog.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
