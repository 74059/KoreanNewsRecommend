# DKN 기반 한국어 뉴스 추천 모델

## 개요
### 프로젝트 동기
* 하루에도 수많은 양의 뉴스가 업데이트 되는 온라인 뉴스 플랫폼
    * 기사를 찾아 읽는 시간이 부담
    * 정보 과다 현상 발생
* 이를 완화하기 위해 사용자의 관심사를 찾는 것을 목표로 하여 개인화된 추천을 받도록 하고자 함

### 개발 내용
* Knowledge Graph 기반 사용자 맞춤 뉴스 추천 

## TECH 
<!-- tech stack button: https://cocoon1787.tistory.com/689 -->
<div>
    <img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=macos&logoColor=white">
    <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
    <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
</div>
<div>
    <img src="https://img.shields.io/badge/vscode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white">
    <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
    <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
</div>
<div>
    <img src="https://img.shields.io/badge/oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white">
    <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=mysql&logoColor=white"> 
    <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=docker&logoColor=white">
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</div>

### etc.
* 한국어 형태소 분석기 [Khaiii](https://github.com/kakao/khaiii)
* 사전 학습된 한국어 embedding을 위한 [KoBERT](https://github.com/SKTBrain/KoBERT)
* [GENSIM Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)

## 관련 연구
### Knowledge graph
* item에 대한 특성 뿐만 아니라, item-item의 관계에 대한 정보를 가지고 있음
* 다수의 연결을 가지는 복합적인 관계 데이터를 관리할 수 있고, 쉽게 탐색할 수 있다는 장점을 가지고 있음   
<div style="text-align:center;">
    <img src='https://miro.medium.com/v2/resize:fit:617/1*chWX0v67nJ0JUzbGiN8ulQ.png' width=400px>
</div>

### TransE

### DKN(Deep Knowledge-Aware Network)
* [Microsoft research Asia 연구 논문](https://arxiv.org/pdf/1801.08284v2.pdf)
    * DKN: Deep Knowledge-Aware Network for News Recommendation
    * [코드](https://github.com/recommenders-team/recommenders#algorithms)
* 뉴스와 한 사용자의 클릭 기록을 입력으로 받아 사용자가 뉴스를 클릭할 확률을 출력하는, 즉, <b style="color:red;">클릭률 예측을 위한 content based 모델</b>
* 단어 자체로부터 계산한 word embedding과 knowledge graph로부터 구한 entity, context embedding을 CNN의 입력으로 전달 &rarr; 하나의 뉴스를 word-level, entity-level, context-level로 동시에 분석 가능
* 사용자가 <b style="color:red;">과거에 본 뉴스기사와 후보 뉴스</b>(candidate news)의 attention weight를 반영하여 최종적으로 <b style="color:red;">사용자가 후보 뉴스를 클릭할 확률(click probability)를 계산</b>한다.

## 진행 내용
1. 데이터
    * 네이버 뉴스의 제목, 신문사, url 크롤링
    * 크롤링한 뉴스의 댓글을 남긴 (암호화된) user 크롤링
    * Wikipidia API 를 이용해 뉴스 제목에 담긴 고유명사에 대한 설명
    * KoBERT에서 pre-trained Korean embedding 가져오기
2. 전처리
    * 뉴스 제목이기 때문에 따로 맞춤법 교정은 해주지 않음
    * Khaiii를 이용해 뉴스 제목, 고유명사 설명 토큰화
    * user 데이터를 바탕으로 사용자가 클릭한 뉴스에 관한 데이터 생성
3. embedding
    * TransE
