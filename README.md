# Online class schedule manager
## 설명
2020년 코로나 바이러스 감염증 사태로 인해 진행하는 온라인 수업을 좀 더 쉽게 진행할 수 있도록 도와주는 프로그램입니다.
## 기능
* 수강한 과목 표시
* 현재 교시 표기
* 과목별 메모
* 시간표 작성/수정
## 사용법
### 시간표 설정법
프로그램을 처음 실행하면 시간표를 생성하겠냐는 안내창이 나옵니다. Apply 하시면 프로그램은 C:\OnlineClassScheduleManager 폴더에 schedule.json 파일을 자동으로 생성합니다. <br>
빈 화면이 나타나는데 왼쪽 메뉴 → 시간표 수정을 통해 시간표 수정창을 로드합니다. <br>
왼쪽부터 차례로 시작 시간, 월, 화, 수, 목, 금, 그리고 아래는 수업 시간, 쉬는 시간, 점심 시간 시작을 입력하는 창이 나타납니다. <br>
시간표는 다음과 같이 입력하십시오: <br>

시작 시간: 예) 9:0, 13:50 - 점심 시간 시작 시간도 똑같습니다 <br>
수업 시간 & 쉬는 시간: 예) 50, 10 <br>
시간표: 예) 국어, 과학 등 <br>

시작 시간은 현재 반드시 7교시까지 입력해야 합니다. 수업 시간이 7교시 이전에 끝나더라도 7교시까지 입력해 주십시오. <br>
저장을 누르면 프로그램이 설정값을 저장하고 재시작합니다.
### 메모 저장법
메모는 각 과목 우클릭을 통해 가능합니다. 메모를 입력하고 저장을 누르면 어느 요일 어느 교시든 동일한 과목에 똑같이 저장됩니다. <br>
URL을 자동으로 열어야 하는 경우 다음과 같은 방법으로 메모에 추가해 자동 오픈 기능을 이용할 수 있습니다: <br>
```url:[[https://github.com/]]```
## 직접 빌드하고 싶을 경우
모든 것이 준비되어 있으니 다음 명령어만 따라 치시면 됩니다
```
C:\> git clone https://github.com/dlcjsdltlq/online-class-schedule-manager.git
C:\> cd online-class-schedule-manager
C:\online-class-schedule-manager> pip install -r requirements.txt
C:\online-class-schedule-manager> pyinstaller -w -F main.spec
```
빌드 파일은 /dist에 생성됩니다
