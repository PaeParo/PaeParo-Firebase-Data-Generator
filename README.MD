# PaeParo Firebase Data Generator
이 프로젝트는 PaeParo의 테스트를 위한 샘플 데이터를 생성하는 파이썬 프로젝트입니다. ChatGPT를 이용하여 생성된 샘플 데이터들을 통해 'Trip'과 'Post' 객체를 무작위로 생성합니다.

<br>

## 구조
### generate_trip_and_post()
Trip과 Post를 생성합니다. 단, Post는 Trip의 status가 "FINISHED"일 경우에만 생성됩니다. 반환값으로 생성된 Trip과 Post가 반환됩니다.

<br>

## 사용법
1) 사용 전 라이브러리 설치가 필요합니다.
```
pip install firebase-admin google-cloud-storage
```

<br>

2) serviceAccount.json 파일이 필요합니다.
해당 파일은 아래 단계를 거쳐 생성할 수 있습니다
```
Firebase Console -> 프로젝트 개요 -> 프로젝트 설정 -> 서비스 계정 -> python -> 새 비공개 키 생성 -> 키 생성
```
키 생성 후 해당 파일을 프로젝트의 local 폴더 아래에 추가합니다.

<br>

## 참고사항
- 새로운 사용자를 추가하여 테스트할 경우 constant/constant.py안의 users에 새로운 사용자의 ID를 추가해야 합니다.
- Trip 생성 시 status를 설정하는 값에 따라 Post를 생성할 수도, 생성하지 않을 수도 있습니다.
  - ```trip['status'] = random.choice(["PLANNING", "ONGOING", "FINISHED"])```: 일정이 "FINISHED"일 경우에만 해당 일정과 관련된 Post가 생성됩니다.
  - ```trip['status'] = random.choice(["FINISHED"])```: 일정을 생성하며 해당 일정과 관련된 Post도 반드시 생성됩니다.
