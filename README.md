# workday
HR 플랫폼
일반 사용자 페이지, HR 관리자 페이지


## 프로젝트 소개
### 프로젝트 개요
지역 혹은 특정 목적별로 음식점들을 모아 놓은 테마를 만들고 사용자들끼리 음식점 정보를 공유 가능

원하는 지역이나 종류를 지정해 쉽고 재밌게 음식점을 선택할 수 있는 사이트.

### 개발 기간
- 2024.01.05 ~ 2024.02.10

### 개발 환경
- FrontEnd : HTML5, CSS3, Vanilla JS, Fetch, Bootstrap
- BackEnd : Python, Django, Django REST Framework
- ORM : Maria DB
- IDE : Visual Studio Code

### 주요 기능  
#### 1. 사용자 인증
- Session, Django 내장 User model을 활용한 사용자 인증과 페이지 권한 설정

#### 2. 테마 및 음식점 게시판
- 이미지를 포함한 CRUD 구현
- Kakao 지도 API를 사용하여 음식점의 위치를 검색 후 선택해서 입력하도록 적용
- Chromedriver와 Selenium을 사용한 이미지 클로링을 통해서 원하는 음식의 이미지 자동 등록
- 댓글 등록, 삭제 기능

#### 3. 음식점 선택
- 음식점 선택 전 음식 조건 filtering, 랜덤 배열 후 카드 선택
