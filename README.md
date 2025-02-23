# Hello Django
<br>

## Django의 CBV(generic view)
<br>

### CBV의 기본 특징
- render(requset, html파일, ctx) 함수를 기본으로 사용하는 FBV와 달리, 별도의 render 함수를 사용하지 않는다.
- urls.py 파일의 path 함수에서 개별적인 함수(render함수 return)들을 url pattern과 매핑하는 대신, 각 generic view의 기본 메소드를(ex.as_view()) url pattern과 매핑한다.
    ```
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    ```
<br>

### ListView
```
class IndexView(generic.ListView):
```
- template_name : 해당 view에서 render 할 html 파일 이름
- context_object_name : render 시, request, html파일명과 함께 argument로 보낼 ctx의 변수 명 
- def get_queryset(self) : 가져올 인스턴스들에 대한 설정
    ```
    return Question.objects.order_by('-pub_date')[:5]
    ```
<br>

### DetailView
``` 
class DetailView(generic.DetailView):
```
- model : 해당 view에서 나타낼 인스턴스가 속한 모델. 어떤 인스턴스를 가져올 지는 해당 generic view와 매핑된 url pattern에 들어오는 인자값에 따라 (해당 인스턴스의 pk?) 정해지는 듯 하다(?).

<br><br><br>
***
<br>

## mysql DB 연동하기

### 1. mysql 설치하기
- https://www.edwith.org/boostcourse-web/lecture/16717/ 를 차근차근히 따라갈 것

### 2. package 설치하기
```
>pip install mysqlclient
```
- 만약 설치 안될 경우, 별도의 파일(ex. mysqlclient-1.4.4-cp37-cp37m-win32.whl)을 직접 다운받아서 프로젝트 디렉토리 내에 넣어서 `pip install mysqlclient-1.4.4-cp37-cp37m-win32.whl` 명령어 실행
- 그래도 안된다면... ~~알아서해라~~

### 3. settings.py 수정하기
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB이름',                       #python manage.py migrate시 테이블 자동생성
        'USER': 'root',                         #root 유저(기본값) 사용
        'PASSWORD': '비밀번호',
        'HOST': '127.0.0.1',
        'PORT': '3306',                         #mysql 설치 시에 설정한 포트번호
    }
}
```

### 4. terminal에서 mysql 명령어 통해 확인하기
```
> mysql -u 유저이름 -p패스워드          #terminal에서 mysql 실행
```

```
mysql> show databases;                #모든 DB 확인
+--------------------+
| Database           |
+--------------------+
| hello_django       |
| information_schema |
| mysql              |
| performance_schema |
| sakila             |
| sys                |
| world              |
+--------------------+
7 rows in set (0.03 sec)

mysql>mysql> use hello_django;       #모든 DB 중 hello_django DB 선택
Database changed

mysql> show tables;                  #helllo_django DB 내의 table 확인
+----------------------------+       #models.py에 명시된 데이터들의 필드 확인
| Tables_in_hello_django     |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
....
```
<br>

###### mysql db 연동 문제
- 문제상황
    - 기존의 sqlite를 사용하고, migration도 다 끝낸 상태였으나, setting을 바꿔서 mysql로 db 연동 전환
    - 그 과정에서 기존에 sqlite로 migration 했던 기록 지움(디렉토리 삭제)
    - `python manage.py migrate polls` : makemigrations 명령어와 migrate 명령어를 사용해 장고앱 polls 내의 models.py 내용에 대한 migration 진행
    - **BUT** mysql db내에 각 모델(`Question`,`Choice`)에 대한 테이블 생성 안 됨
- 해결 방안1
    - `python manage.py migrate --fake polls zero` 명령어를 통해 장고앱 polls의 migration에 대해 set 되어있던 false 설정을 zero 값으로 바꿔줌 (https://stackoverflow.com/questions/35494035/django-migrate-doesnt-create-tables)
- 문제 상황2
    - migration이 DB로 제대로 이루어지지 않는 문제는 해결 **BUT** 기존에 이상하게 migrate 되어 models.py 내용의 일부만 mysql DB에 몇 개의 테이블과 필드만 migrate 되어 있었음을 확인(migration error 발생 `table 'polls_question' already exists`)
- 해결 방안2
    - mysql 내 table에 직접 접근해서 해당 table(이상하게 migrate된 table) drop
        ```
        >mysql -uroot -p비밀번호     #기존 terminal에서 mysql 실행
        
        mysql>show databses;        #모든 DB 확인
        ...
        
        mysql>use hello_django;     #hello_django DB로 접근
        ...
        
        mysql>show tables;         #hello_django 내 table 확인
        +----------------------------+
        | Tables_in_hello_django     |
        +----------------------------+
        | auth_group                 |
        | auth_group_permissions     |
        | auth_permission            |
        | auth_user                  |
        | auth_user_groups           |
        | auth_user_user_permissions |
        | django_admin_log           |
        | django_content_type        |
        | django_migrations          |
        | django_session             |
        | polls_question             |
        +----------------------------+
        12 rows in set (0.00 sec)

        mysql>drop table polls_question  # hello_django에서 polls_question 테이블 제거
        ```   
    - table drop 후 새롭게 `python manage.py migrate polls` 실행하니 db 정상 작동 확인
        ```
        mysql>show tables;
        +----------------------------+
        | Tables_in_hello_django     |
        +----------------------------+
        | auth_group                 |
        | auth_group_permissions     |
        | auth_permission            |
        | auth_user                  |
        | auth_user_groups           |
        | auth_user_user_permissions |
        | django_admin_log           |
        | django_content_type        |
        | django_migrations          |
        | django_session             |
        | polls_choice               |
        | polls_question             |
        +----------------------------+
        12 rows in set (0.00 sec)
        
        mysql> show full columns from polls_choice;
        +-------------+--------------+--------------------+------+-----+---------+----------------+---------------------------------+---------+
        | Field       | Type         | Collation          | Null | Key | Default | Extra          | Privileges                      | Comment |
        +-------------+--------------+--------------------+------+-----+---------+----------------+---------------------------------+---------+
        | id          | int(11)      | NULL               | NO   | PRI | NULL    | auto_increment | select,insert,update,references |         |
        | choice_text | varchar(200) | utf8mb4_0900_ai_ci | NO   |     | NULL    |                | select,insert,update,references |         |
        | votes       | int(11)      | NULL               | NO   |     | NULL    |                | select,insert,update,references |         |
        | question_id | int(11)      | NULL               | NO   | MUL | NULL    |                | select,insert,update,references |         |
        +-------------+--------------+--------------------+------+-----+---------+----------------+---------------------------------+---------+
        4 rows in set (0.01 sec)
        ```
    


<br><br><br>
***
<br>

## 자동화 된 test 하기

- django tutorial Part5. https://docs.djangoproject.com/ko/2.2/intro/tutorial05/
- ~~테스트 주도 개발...?~~
- test.py의 코드가 방대해진다고 해서 걱정하지 말아라. 버그를 확인하고 사전에 예방하는 건 좋은거다.

### test.py
- django app 생성 시 app마다 기본적으로 가지고 있는 python 파일
- `test.py`내에 `from django.test import TestCase`를 통해 import 한 TestCase 클래스를 상속받아 새로운 testcase 클래스를 만들고, 그 안에 test를 위한 메소드 구현  
- `py manage.py test app명`의 명령어로 test.py 실행
- 상속받은 클래스 내에 여러 메소드를 구현함으로써 여러 경우에 대한 test를 한번에 수행 가능

### Client
- test를 위한 테스트 클라이언트 클래스


<br>

###### cfs)
- timezone package의 datetime.timedelta(int)는 int만큼의 시간차이(delta)를 나타내는 인스턴스를 반환
- python 명령어 실행 시, python 말고 py라고만 써도 실행 가능
```
>python manage.py runserver 
>py manag.py runserver      #동일한 효과
```

<br><br><br>
***
<br>

## STATIC 파일 사용하기
- css, gif, png 등 정적파일을 django 내에서 사용하기 위해 장고앱마다 `static`이라는 하위 디렉토리를 만들어 그 디렉토리에 저장해야 한다.
    ```
    mysite
        \mysite
        \polls
            \migrations
            \templates
            \static
                \polls
                    \css
                        \style.css
                    \images
                        \background.png
            \__init__.py
            \admin.py
            ... 
    ``` 
- template(html 파일) 내에 static file들을 불러오기 위한 코드를 삽입해야 한다.
    ```
    {% load static %}

    <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">
    ```
    
<br><br><br>
***
<br>

## django admin page 커스터마이징

- django tutorial part 7 (https://docs.djangoproject.com/ko/2.2/intro/tutorial07/)

### 모델 내 필드에 대한 관리 
- `admin.py` 코드 수정을 통한 관리자 옵션 변경은 `ModelAdmin class 생성 -> admin.site.register()의 두번째 인자로 클래스 전달`의 패턴을 따른다.
    ```
    from django.contrib import admin
    
    from .models import Question
    
    
    class QuestionAdmin(admin.ModelAdmin):
        fieldsets = [
            (None,               {'fields': ['question_text']}),
            ('Date information', {'fields': ['pub_date']}),
        ]
    
    admin.site.register(Question, QuestionAdmin)    
    ```
- 위 코드를 통해 아래 스크린샷과 같은 admin page를 만들 수 있다.
    ![admin08](./polls/static/polls/images/admin08.png)
- `admin.ModelAdmin` 클래스에서 `fields` 속성을 사용하면, 단순히 여러 필드를 나열하게 되고, `fieldsets` 속성을 사용하면, 몇개의 필드들을 하나로 묶어 필드셋으로 사용 가능하다. 이 경우, 각 필드셋에 대한 명명도 가능하다.
 
    
### 연결된 다른 모델(Foreign Key)에 대한 관리
- `ModelAdmin` 클래스 내의 `inlines` 속성에 새로운 `Inline` 클래스들을 리스트 형태로 대입하면 일대다 관계로 연결된 객체들도 함께 관리할 수 있다.
    ```
    from django.contrib import admin
    
    from .models import Choice, Question
    
    
    class ChoiceInline(admin.TabularInline):
        #현재 Question 인스턴스와 연결된 Choice 모델의 인스턴스를 가져옴
        model = Choice
        extra = 3       #추가적으로 3개를 넣을 수 있도록 보여줌
    
    
    class QuestionAdmin(admin.ModelAdmin):
        fieldsets = [
            (None,               {'fields': ['question_text']}),
            ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]
        inlines = [ChoiceInline]
    
    admin.site.register(Question, QuestionAdmin)
    ```
   
### change list 관리
- `ModelAdmin` 클래스의 `list_display` 속성에 `tuple` 형태로 어드민 페이지의 인스턴스 리스트(change list)의 column값들을 입력해준다
    ```
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    ``` 

### admin page template 관리
- `settings.py`의 `TEMPLATES`에서 `DIRS` 리스트 내에 `os.path.join(BASE_DIR, 'templates')`를 넣어주고, 프로젝트 디렉토리 내에 새로운 `templates` 디렉토리를 만들어준다.
    ```
    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
    ```
- shell에서 `py -c "import django`, `print(django.__path__)"`의 명령어를 통해 개발 환경 내에 django가 설치된 위치를 파악한다.
- 파악한 위치를 통해 `django/contrib/admin/templates`에 있는 `admin/base_site.html` 파일을 찾아 프로젝트 내 `templates/admin`에 복사한 뒤, 해당 html을 수정해 커스터마이징 한다.
    
    
    
    