>[官网地址](http://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/#)

### 一、开发环境
* 1、`python3.6`
* 2、`django2.0`
* 3、`window10`

### 二、项目搭建
* 1、创建一个虚拟空间`mkvirtualenv 空间名`
* 2、创建一个`django`项目
* 3、安装`graphql`的依赖包

    ```python
    pip install graphene-django
    ```
    
* 4、创建一个组件`blog`
* 5、把组件`blog`及`graphene_django`注入到`app`中
* 6、在`settings.py`中配置`mysql`数据库连接

### 三、书写`blog`的内容
* 1、在`models.py`中写上数据模型

    ```python
    from django.db import models
    
    
    # Create your models here.
    class User(models.Model):
        name = models.CharField(max_length=100, verbose_name="博主名字")
        gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', '女')), default='female',
                                  verbose_name='性别')
        create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    
    class Blog(models.Model):
        title = models.CharField(max_length=100, verbose_name='标题')
        user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='博主名字')
        content = models.TextField(verbose_name='博客内容')
        create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
        update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    ```
    
* 2、新建一个`schema.py`文件

    ```python
    #!/usr/bin/env python
    # encoding: utf-8
    
    import graphene
    from graphene_django.types import DjangoObjectType
    from .models import User, Blog
    
    
    class UserType(DjangoObjectType):
        class Meta:
            model = User
    
    
    class BlogType(DjangoObjectType):
        class Meta:
            model = Blog
    
    
    # 定义动作约素输入类型
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
    
    ```
    
* 3、在跟目录(和`settings.py`同级)创建一个项目的总`schema.py`

    ```python
    import graphene
    import book.schema, blog.schema
    
    
    class Query(blog.schema.Query, graphene.ObjectType):
        # 总的Schema的query入口
        pass
    
    
    class Mutations(graphene.ObjectType):
        # 总的Schema的mutations入口
        create_user = blog.schema.CreateUser.Field()
        create_blog = blog.schema.CreateBlog.Field()
    
    
    schema = graphene.Schema(query=Query, mutation=Mutations)
    ```
    
* 4、配置`url`地址

    ```python
    from django.contrib import admin
    from django.urls import path
    from graphene_django.views import GraphQLView
    from .schema import schema
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    ]
    ```
    
* 5、生成数据库映射及启动项目,直接在浏览器上访问

### 四、可以对上面的代码调整
* 1、把`Mutations`也单独定义在各自的`schema.py`中

    ```python
    # 定义一个总的mutation出口
    class Mutation(graphene.AbstractType):
        create_user = CreateUser.Field()
        create_blog = CreateBlog.Field()
    ```
    
* 2、在总的`schema.py`中引入类型`Query`一样的操作

    ```python
    class Mutations(blog.schema.Mutation, graphene.ObjectType):
        # 总的Schema的mutations入口
        pass
    ```
    
* 3、输入数据类型可以直接定义在`mutation`里面

    ```python
    class CreateUser(graphene.Mutation):
        # api的输入参数(类名可以随便定义)
        class Arguments:
            name = graphene.String(required=True)
            gender = graphene.String(required=True)
    
        # api的响应参数
        ok = graphene.Boolean()
        user = graphene.Field(UserType)
    
        # api的相应操作，这里是create
        def mutate(self, info, name, gender):
            user = User.objects.create(name=name, gender=gender)
            ok = True
            return CreateUser(user=user, ok=ok)
    ```
    
### 五、`Query`语句中使用条件查询
* 1、`app`的`schema`(官方案例)

    ```python
    import graphene
    from graphene_django.types import DjangoObjectType
    from .models import Category, Ingredient
    
    
    class CategoryType(DjangoObjectType):
        class Meta:
            model = Category
    
    
    class IngredientType(DjangoObjectType):
        class Meta:
            model = Ingredient
    
    
    # 定义一个查询
    class Query(object):
        # 定义一个根据id或者name查询的
        category = graphene.Field(CategoryType,
                                  id=graphene.Int(),
                                  name=graphene.String())
        # 查询全部的
        all_categories = graphene.List(CategoryType)
        # 根据条件查询
        ingredient = graphene.Field(IngredientType,
                                    id=graphene.Int(),
                                    name=graphene.String())
        # 查询全部的
        all_ingredients = graphene.List(IngredientType)
    
        def resolve_all_categories(self, info, **kwargs):
            return Category.objects.all()
    
        def resolve_all_ingredients(self, info, **kwargs):
            # We can easily optimize query count in the resolve method
            return Ingredient.objects.select_related('category').all()
    
        # 定义查询语句
        def resolve_category(self, info, **kwargs):
            id = kwargs.get('id')
            name = kwargs.get('name')
    
            if id is not None:
                return Category.objects.get(pk=id)
    
            if name is not None:
                return Category.objects.get(name=name)
    
            return None
    
        def resolve_ingredient(self, info, **kwargs):
            id = kwargs.get('id')
            name = kwargs.get('name')
    
            if id is not None:
                return Ingredient.objects.get(pk=id)
    
            if name is not None:
                return Ingredient.objects.get(name=name)
    
            return None
    ```