---
title: IR 센서를 활용한 혼잡도 분석
author: Nam Jonghyeon, Kim jungun
date: 2022-12-01 21:40:00 +0900
categories: [Exhibition,2022년]
tags: [post,namjonghyeon]
---

# IR 센서를 활용한 혼잡도 분석

## 작품 설명
연구 내용은 라즈베리 파이, 아두이노 두 가지로 구분할 수 있습니다. 우선 아두이노 부분은 IR 센서와 레이저 센서를 이용하여 사람의 출입 방향을 감지하고 이를 바탕으로 혼잡도를 측정하게 됩니다.
라즈베리 파이 부분은 깃허브 Repository에서 페이지를 생성한 다음 아두이노에서 보내는 센서 값을 받아 주기적으로 정보를 commit 하는 기능을 구현하게 됩니다.
![4](https://user-images.githubusercontent.com/68436389/211976554-d9a147f7-9b86-4bc7-8d29-21a64bfda605.jpg)
![1](https://user-images.githubusercontent.com/68436389/211976555-29733e6d-8ce1-4a51-bef7-72d6c4961a80.jpg)


## Hardware

### 1. Sensor

- 'TOF10120' 레이저 센서

  - Serial 통신으로 아두이노와 연결되며 레이저를 이용하여 바로 앞의 사물을 감지하게 됩니다.

- 'GP2Y0A02' IR 센서

  - 아두이노의 아날로그 포트를 통해 연결되며 적외선을 이용하여 레이저 센서에 비해 비교적 넓은 범위를 감지할 수 있으나 감지 속도는 레이저 센서에 비해 느립니다.

### 2. Arduino Uno
- 'TOF10120' 레이저 센서와 'GP2Y0A02' IR 센서의 거리 측정 데이터를 수신하며 이를 가공한 데이터를 라즈베리파이로 보내게 됩니다.

### 3. Raspberry Pi 4
- USB 케이블을 통해 아두이노와 연결되며 아두이노와 각종 센서에 전원을 공급하게 됩니다.

- 아두이노에서 수신한 데이터를 이용하여 혼잡도를 측정한 다음 이를 html 파일에 저장하고 깃허브 원격 저장소인 'innovation_hanyang.github.io' 의 웹페이지에 html 파일을 업로드하는 역할을 수행합니다.


## Software

### 1. Arduino Uno

- Final_code.ino

  - 레이저 센서와 IR 센서에서 측정된 각각의 거리 데이터를 이용하여 사람의 출입 방향을 판단하고 현재 인원수를 측정합니다.

### 2. Raspberry Pi 4

- test.py

  - 핵심 기능
 
    - 아두이노로부터 현재 인원수 데이터를 받아온 뒤 20명 미만이면 '양호', 40명 미만이면 '혼잡', 60명 이상이면 '매우 혼잡'을 측정 시각과 함께 웹페이지에 표시합니다.

  - 원리

    - 웹페이지 디자인의 skeleton이 저장된 index_origin.html 파일을 불러와서 'data' 문자열을 상태메세지(양호, 혼잡 등)으로 변환하고 'time' 문자열을 데이터 수신 시각으로 변환한 다음 index.html 파일에 저장합니다.

    - 아두이노로부터 데이터를 수신할 때마다 'can' 변수를 1씩 증가시키며 can == 1070을 만족하기까지 약 1분 정도가 소요됩니다. 깃허브 웹페이지가 새로운 commit을 받을 경우 갱신될 때까지 대략 1분 정도 소요되므로 1분마다 출입 인원수가 갱신되도록 하였습니다.

    - git 패키지를 활용하여 파이썬으로 'git add', 'git commit -m changed_2022-11-28 16:54:06 ' 명령을 구현하였으며 subprocess 패키지를 활용하여 'git push -u origin master' 명령을 구현하였습니다.

- index_origin.html

  - 핵심 기능

    - 'innovation_github.io' 저장소의 웹페이지를 구현할 html 코드입니다.

  - 원리

    - test.py 코드가 실행되면서 라즈베리파이 내부 저장소의 'index_origin.html'을 가공하여 'index.html' 파일에 저장하고 해당 파일이 원격저장소로 업로드됩니다.
