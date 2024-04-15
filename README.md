# workday
HR 플랫폼
일반 사용자 페이지, HR 관리자 페이지


## 프로젝트 소개
### 프로젝트 개요
회사 근태 관리, 휴가 신청, 업무 일지 등록 및 관리, 게시판 등을 사용 할 수 있는 사내 HR 플랫폼

사내에 HR 시스템이 열악하여 직접 만들어보았다.

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
