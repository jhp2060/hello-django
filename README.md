# Hello Django

## Django의 CBV(generic view)
<br>

####CBV의 기본 특징
- render(requset, html파일, ctx) 함수를 기본으로 사용하는 FBV와 달리, 별도의 render 함수를 사용하지 않는다.
- urls.py 파일의 path 함수에서 개별적인 함수(render함수 return)들을 url pattern과 매핑하는 대신, 각 generic view의 기본 메소드를(ex.as_view()) url pattern과 매핑한다.
    ```
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    ```
<br>

####1. ListView
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

####2. DetailView
``` 
class DetailView(generic.DetailView):
```
- model : 해당 view에서 나타낼 인스턴스가 속한 모델. 어떤 인스턴스를 가져올 지는 해당 generic view와 매핑된 url pattern에 들어오는 인자값에 따라 (해당 인스턴스의 pk?) 정해지는 듯 하다(?).
