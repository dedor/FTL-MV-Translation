# 스크립트 개요

## generate-xlsx.py
원본 xml(/orig)에서 텍스트만을 추출해 /xls에 xlsx로 저장.
## fill-kor-at-xlsx.py
기존 번역파일 xml(/kor)에서 텍스트를 추출하고, /xls의 데이터와 병합해 /xls_merged를 생성함.
### 병합 규칙
- 같은 이름의 세그먼트를 지금까지 처리하지 않은 세그먼트에서 찾음.
- 번역되지 않은(원문과 동일한) 세그먼트는 생략.
## generate-xml.py
원본 xml(/orig)에서 텍스트를 /xls의 kor열의 텍스트로 치환한 것을 /kor에 xml로 저장.
병합 규칙과 같은 방식으로 치환.
## update-xlsx.py
업데이트된 xml(/update)으로 /xls을 갱신해 xls_updated에 저장.

# TODO
- 파일 자체가 수정된 경우?
    - 모든 파일을 읽은 후 알맞은 세그먼트 채우기?(TM 구현)
- crowdin 플랫폼에서 TM, comments 기능 지원 여부 파악
- 다른 모드와 호환성을 위해 텍스트 치환형 패치?
- 텍스트 데이터가 없는 xml은 xls 생성하지 않기

# FLOW

## 처음 시작하는 경우
0. 준비해야 할 파일 : 원본 xml
1. 원본 xml을 /orig 폴더를 만들어 위치.
2. generate-xlsx.py를 실행.
3. /xls에 생성된 파일로 작업 시작.

## 업데이트 하는 경우
0. 준비해야 할 파일 : **업데이트된** 원본 xml, 작업 xls
1. 업데이트된 원본 xml을 /update 폴더를 만들어 위치.
2. 기존 번역물 xls을 /xls에 위치.
3. update-xlsx.py를 실행.
4. /xls의 갱신된 파일로 작업 재개.

## 기존 번역 xml이 있는 경우
0. 준비해야 할 파일 : 원본 xml, 기존 번역 xml
1. 원본 xml을 /orig 폴더를 만들어 위치.
2. 번역 xml을 /kor 폴더를 만들어 위치.
3. generate-xlsx.py를 실행.
4. fill-kor-at-xlsx.py를 실행.
5. /xls_merged의 파일로 작업 시작. 
    - /xls의 파일은 원문 데이터만 있는 파일로, fill-kor-at-xlsx.py의 실행이 끝난다면 삭제해도 무방함.

## 번역을 적용하는 경우
0. 준비해야 할 파일 : 작업한 xls, 원본 xml
1. 원본 xml을 /orig 폴더를 만들어 위치.
2. 작업한 xls을 /xls 폴더를 만들어 위치.
3. 결과물이 저장될 /kor 폴더 생성.
4. generate-xml.py를 실행.

### 원본 xml 수정사항
- dlcBlueprints.xml.append xml 태그의 "mod:"를 "mod_"로 치환
- events_mantis.xml.append: line 500, column 56 주석 삭제
#### 삭제 파일
- achievements.xml
- animations.xml
- achievements_unused.xml
- blueprints.xml.rawappend
- bosses.xml.append
- events_imageList.xml.append
- sounds.xml.append
#### names 사용 파일 (검증 필요)
- names.xml.append
- sector_data.xml.append