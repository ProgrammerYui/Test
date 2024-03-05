







# 캐릭터와 이미지 선언은 init 안에 해주기, show_two_window는 삭제하기
init python:
    speaking = None

    def while_speaking(name, speak_d, done_d, st, at):
        if speaking == name:
        # 현재 대사를 치고 있는 캐릭터 이미지는 변형 없이 출력
            return speak_d, None
        else:
        # 대사를 치고 있지 않은 나머지 캐릭터 이미지를 음영 처리하는 부분
            done_d = im.MatrixColor(
            done_d, 
            im.matrix.tint(0.45, 0.45, 0.45)
            *im.matrix.brightness(-0.07))
            # 여기까지
            return done_d, None
    curried_while_speaking = renpy.curry(while_speaking)

    def WhileSpeaking(name, speaking_d):
        return DynamicDisplayable(curried_while_speaking(name, speaking_d, speaking_d))
        
    def speaker_callback(name, event, **kwargs):
        global speaking
        if event == "show":
            speaking = name
        elif event == "end":
            speaking = None
    Speaker = renpy.curry(speaker_callback)





# 이 파일에 게임 스크립트를 입력합니다.

# image 문을 사용해 이미지를 정의합니다.
# image eileen happy = "eileen_happy.png"

# 게임에서 사용할 캐릭터를 정의합니다.
# define e = Character('아이린', color="#00700f")

# 호감도 변수 테스트
init:
    $ n = 0
    $ Episode1 = 1
    $ tem = 0
    $ miss_count = 0 # 기타 선택 관련 함수
    $ select = 0 # 선택 관련 함수
    $ callormessage = 0 # 전화?문자? 택 함수

    $ Dohee_like = 0
    $ Ruru_like = 0
    $ Sehyuk_like = 0
    $ Soohyun_like = 0
    $ Juhan_like = 0
    $ Siwoon_like = 0

    # 인기도
    $ popular = 0
"""
    # 아이콘 호감도 표시
    image point Dohee = ConditionSwitch(
                                'Dohee_like <= 5' , '0-5.png' ,
                                'Dohee_like >= 6 and Dohee_like <=15 ', '6-15.png',
                                'Dohee_like >= 16 and Dohee_like <= 25', '16-25.png',
                                'Dohee_like >= 26 and Dohee_like < 100', '26.png',
                                'Dohee_like >= 100', '100.png')

    image point Sehyuk = ConditionSwitch(
                                'Sehyuk_like <= 5' , '0-5.png' ,
                                'Sehyuk_like >= 6 and Sehyuk_like <=15 ', '6-15.png',
                                'Sehyuk_like >= 16 and Sehyuk_like <= 25', '16-25.png',
                                'Sehyuk_like >= 26 and Sehyuk_like < 100', '26.png',
                                'Sehyuk_like >= 100', '100.png')
    
    image point Soohyun = ConditionSwitch(
                                'Soohyun_like <= 5' , '0-5.png' ,
                                'Soohyun_like >= 6 and Soohyun_like <=15 ', '6-15.png',
                                'Soohyun_like >= 16 and Soohyun_like <= 25', '16-25.png',
                                'Soohyun_like >= 26 and Soohyun_like < 100', '26.png',
                                'Soohyun_like >= 100', '100.png')

    image point Juhan = ConditionSwitch(
                                'Juhan_like <= 5' , '0-5.png' ,
                                'Juhan_like >= 6 and Juhan_like <=15 ', '6-15.png',
                                'Juhan_like >= 16 and Juhan_like <= 25', '16-25.png',
                                'Juhan_like >= 26 and Juhan_like < 100', '26.png',
                                'Juhan_like >= 100', '100.png')

    image point Siwoon = ConditionSwitch(
                                'Siwoon_like <= 5' , '0-5.png' ,
                                'Siwoon_like >= 6 and Siwoon_like <=15 ', '6-15.png',
                                'Siwoon_like >= 16 and Siwoon_like <= 25', '16-25.png',
                                'Siwoon_like >= 26 and Siwoon_like < 100', '26.png',
                                'Siwoon_like >= 100', '100.png')

    image point popular = ConditionSwitch(
                                'popular <= 5' , '0-5.png' ,
                                'popular >= 6 and popular <=15 ', '6-15.png',
                                'popular >= 16 and popular <= 25', '16-25.png',
                                'popular >= 26 and popular < 100', '26.png',
                                'popular >= 100', '100.png')                            

"""

# 인벤토리 구현
init python :
    class use_itme:
        def __init__ (self, img, value, use):
            self.img = img
            self.value = value
            self.use = False
        def use(self):
            self.use = True
            # 아이템 담을 배열 변수 선언

init:     
# items 선언 
    $ view_items = []
    $ use_items = []

init python:
#인벤토리 버튼 추가 - 신버전
# Inventory button을 선언하고 오버레이에 추가한다
# (오버레이에 추가해야 게임 진행과 상관없이 떠있는 버튼이 된다)
    show_inventory = True

    def inventory_button():
            if show_inventory:
                ui.vbox(spacing=100, xalign=0.99, yalign=0.01)
                # 인벤토리 이미지 버튼
                # click시 show_item_list label 호출
                ui.imagebutton("Inventory.png", clicked=renpy.curried_call_in_new_context("show_item_list"))
                ui.close()
                
    # 오버레이에 추가 
    config.overlay_functions.append(inventory_button)

    # 호감도 버튼 추가
    """
    def like_button():
        ui.vbox(spacing = 100, xalign=0.90, yalign = 0.01)
        ui.imagebutton("like.png",  clicked=renpy.curried_call_in_new_context("info"))
        ui.close()

    config.overlay_functions.append(like_button)
    """
    

# 재시작할 때 인벤토리 초기화 
init python :
    use_itmes = []
    view_items = []
    #show_inventory = False
    
    def init_val():
        #리스트 초기화
        use_itmes.clear()
        view_items.clear()
        #show_inventory = False

            
#init python:
#    _window = False

#init:
#    $ noisedissolve = ImageDissolve(im.Tile("noisetile.png"), 1.0, 1)
#    $ noise_effect = ImageDissolve(im.Tile("noisetile.png"), 0.5, 0.5)
  
#캐릭터 정의
init:
    define narrator = Character(None, kind = nvl) # 전체 나레이터
    define narrator_2 = Character(None) # 일반 나레이터= 독백
    define me = Character("나", color = "#5da9ff") # 나 , 이름 적용 전의 나. 이름 적용 후는 na

    define Juhan = Character("주한" , color = "#187c18", callback=Speaker('주한'))
    define Soohyun = Character("수현" , color = "#e09531", callback=Speaker('수현'))
    define Sehyuk = Character("세혁" , color = "#413dff", callback=Speaker('세혁'))
    define Siwoon = Character("시운" , color = "#fa1eb8", callback=Speaker('시운'))
    define Dohee = Character("도희" , color = "#222222", callback=Speaker('도희'))
    define Ruru = Character("루루" , color = "#56a5ff", callback=Speaker('루루'))

    define moderator = Character("사회자", color = "#5da9ff", callback=Speaker('사회자'))
    define Sehyun = Character("세현" , color = "#5da9ff", callback=Speaker('세현'))
    define bodyguards = Character("경호원", color = "#5da9ff", callback=Speaker('경호원'))
    define ars = Character("ARS", color = "#5da9ff", callback=Speaker('ARS'))

    # 멤버들
    define members = Character("멤버들", color = "#5da9ff" , callback=Speaker('멤버들'))

    # 2챕터 한정 등장 캐릭터
    define ParkPD = Character("박PD" , color = "#5f5f5f", callback=Speaker('박PD'))
    define Lyricist = Character("김율" , color = "#5f5f5f", callback=Speaker('김율'))
    define Composer = Character("이준" , color = "#5f5f5f", callback=Speaker('이준'))
    

    #테스팅
    #define Juhan = Character("주한", show_two_window = True, color = "#5da9ff", callback=Speaker('주한'))
    #define Ruru = Character("루루", show_two_window = True, color = "#5da9ff", callback=Speaker('루루'))


    #캐릭터 사이드 정의
    define Dohee_call = Character("도희", color = "#5da9ff", image="scg_Dohee_call")

    #트랜지션 효과 정의
    define fadehold = Fade(0.5, 1.0, 0.5)
    define fadeslow = Fade(1.0, 0.0, 1.0)
    define dissolveslow = Dissolve(1.5)

    #캐릭터 이미지 설정
    #image scg_Juhan nor:
    #    WhileSpeaking("주한", im.FactorScale("권주한_기본.png", 1.2))
        #im.FactorScale("권주한_기본.png", 1.2)
    #    yalign -0.5
    image scg_Juhan nor = WhileSpeaking("주한","권주한_기본.png")

    #image scg_Soohyun:
    #    im.FactorScale("이수현_기본.png", 1.2)
    #    yalign -0.5
    image scg_Soohyun nor = WhileSpeaking("수현","이수현_기본.png")

    #image scg_Sehyuk:
    #    im.FactorScale("서세혁_기본.png", 1.2)
    #    yalign -0.5
    image scg_Sehyuk nor = WhileSpeaking("세혁","서세혁_기본.png")



    #image scg_Siwoon:
    #    im.FactorScale("강시운_기본.png", 1.2)
    #    yalign -0.5
    image  scg_Siwoon nor = WhileSpeaking("시운","강시운_기본.png")

    image scg_Dohee nor:
        #im.FactorScale("양도희_기본.png", 1.2)
        WhileSpeaking("도희","양도희_기본 - 복사본.png")
        # 앞부분 너비 1000으로 확장시킴. 그 뿐!
        yalign 0.8
    #image scg_Dohee nor = WhileSpeaking("도희","양도희_기본.png"):


    #image scg_Dohee_call:
    #    im.FactorScale("양도희_기본.png", 1.2)
    #    yalign -0.5

    #image side scg_Dohee_call:
    #    im.FactorScale("양도희_사이드.png", 1.0)

    #image scg_Ruru:
    #    im.FactorScale("루루_기본.png", 1.2)
    #    yalign -0.5
    image scg_Ruru nor = WhileSpeaking("루루","루루_기본.png")


##################################################

    image scg_Sehyun:
        im.FactorScale("세현.png", 1.2)
        yalign -0.5

    image scg_bodyguards:
        im.FactorScale("보디가드.png", 1.2)
        yalign -0.5
    # image scg_Ruru nor = WhileSpeaking("루루","루루_기본.png")


    define center = Position(xalign = 0.5, yalign = -0.5)
    define left = Position(xalign = 0.0, yalign = -0.5)
    define right = Position(xalign = 1.0, yalign = -0.5)
    define one = Position(xalign = -0.15, yalign = -0.5)
    define two = Position(xalign = 0.25, yalign = -0.5)
    define three = Position(xalign = 0.67, yalign = -0.5)
    define four = Position(xalign = 1.15, yalign = -0.5)

    # 여캐 전용
    define girl_center = Position(xalign = 0.5, ypos = 1.1)
    define girl_one = Position(xalign = -0.15, yalign = -0.8)
    define girl_two = Position(xalign = 0.25, yalign = -0.8)
    define girl_three = Position(xalign = 0.67, yalign = -0.8)
    define girl_four = Position(xalign = 1.15, yalign = -0.8)

    define item = Position(xalign = 0.5, yalign = 0.5)
    # 세 수 주 시 순서 권장

    #인트로 이미지 삽입
    image intro1 = im.FactorScale("이미지1.png" , 1.5)
    image intro2 = im.FactorScale("이미지2.png" , 1.5)
    image intro3 = im.FactorScale("이미지3.png" , 1.5)
    image intro4 = im.FactorScale("이미지4.png" , 1.5)

    image prologue = im.FactorScale("사무실.jpg", 1.5)

    image black = "검은배경.jpg"
    image white = im.FactorScale("흰색배경.png", 1.0)

    # 배경
    image ben = im.FactorScale("벤.png", 1.5) # 수정전
    image ben2 = im.FactorScale("벤 이미지.png", 1.2) # 수정후 
    image cafe = im.FactorScale("카페.png", 1.0)
    image practice_room = im.FactorScale("연습실.png", 1.0)
    image corridor = im.FactorScale("복도.png", 1.0)
    image menus = im.FactorScale("메뉴화면.png", 1.0)

    # 일러스트
    image first_meeting = im.FactorScale("첫만남.png", 1.0)
    image first_meeting_1 = im.FactorScale("첫만남1.png", 1.4)
    image first_meeting_2 = im.FactorScale("첫만남2.png", 1.4)
    image metting_a = im.FactorScale("보정첫만남.png", 1.0)

    # 임시 사용 이미지
    image imsi = "임의메인메뉴이미지.jpg"

    # 아이템
    image namecard = im.FactorScale("명함.png", 1.0)
    image schedule_table = im.FactorScale("스케줄표.png", 1.0)

#이름 입력받은 후 플레이어 캐릭터 설정

#init python:
    #player_name = 'FlaSh'
    #na = Character('player_name', dynamic = True)





# 한국어 이름 조사 자동 판독기   
init python:

    finalConso = None
    name = ''
    na = Character('name', dynamic = True)
    
    #받침유무판별기
    def finalChecker(name):
        import re
        name = name
        expr = re.compile(r'([a-zA-Z0-9\s~!@#$%^&*()_+|}{:"<>?`\-=\\\[\];\',./])')
        temp = expr.sub('', name)
        
        
        if temp == '':
            return False
         
        last_alphabet = repr(temp[-1])
        dec = int(str(last_alphabet[4:-1]), 16)

        
        
         
        while dec < 0x3164:
            temp = temp[:-1]
            if not temp:
                return False
                 
            last_alphabet=repr(temp[-1])
            dec = int(str(last_alphabet[4:-1]), 16)
            
                 
        dec= (dec-44032) % 588 % 28
  
        if dec == 0: 
            return False
             
        else: 
            return True
             
    #조사 바꾸기
    def pppChanger(input):
        import re
        pppList = [('가', '이'), ('는', '은'),
                        ('를', '을'), ('와', '과'), 
                        ]
                         
        if finalConso:
            #[]로 이름치환 사용시
            input = re.sub('\[name\]야', name + '아', input)
            input = re.sub('\[name\]', name + '이', input)
             
            #%()s로 이름치환 사용시
            input = re.sub('%\(name\)s야', name + '아', input)
            input = re.sub('%\(name\)s', name + '이', input)
                 
            for p, pc in pppList:
                input = re.sub('\[name\]'+ p, "[name]" + pc, input)
                input = re.sub('%\(name\)s' + p, "[name]" + pc, input)
                 
        return input
             
    config.say_menu_text_filter = pppChanger


# Inventory Button 클릭시 item list 보여주기
# item list 스크린에서 for문을 돌면서 item textbutton을 만들어준다.
label show_item_list:
    # item list screen 호출
    $ renpy.call_screen("sc_item_list")

# 호감도 창
#label info:
#    $ renpy.call_screen("info")
#    return


# 우선 음악은 제외시킴~

# 여기에서부터 게임이 시작합니다.
label start:
    # 인벤토리 초기화
    $ init_val()

    if renpy.is_seen(ever=True):
        jump Episode2

    if Episode1 == 0:
        jump Episode2


    #show screen setting_button
    #show screen sc_item_list

    # 인트로
    # S1
    scene intro1 with fade
    narrator_2 "다들 한번 쯤은 상상해 본 적 있지 않나요?" # with vpunch
    narrator_2 "내가 만든 캐릭터와 직접 만나서 웃고 떠드는 순간을"

    # S2
    scene intro2 with dissolve
    narrator_2 "직접 캐릭터를 그리고, 성격을 만들고, 캐릭터들끼리 이야기도 만들고 놀면서 말이에요."
    narrator_2 "오늘도 그랬어요. 일하고, 공부하느라 지친 기분을 달랠 겸, 그림을 그리려고 했죠."
    # 펜으로 뭔가를 쓰는 소리

    # S3
    scene intro3 with dissolve
    narrator_2 "그런 일상은 예전에도, 지금도, 앞으로도 변하지 않을 거라고 생각했어요."
    # 종이 휘날리는 소리(작게)

    # S4
    # 종이 휘날리는 소리(크게)
    scene intro4 with dissolve
    narrator_2 "그런데요, 그런데..."
    me "어...어?"

    # S5
    me "꺄악!!!!" with vpunch

    scene white with pixellate

    scene black with fade

    # 이명같은 소리가 작았다가 점점 커짐. 음원 파일 추가해야함

    # S6
    # 속도 제한
    Dohee "{cps=5}저기요!{/cps}" with vpunch

    #scene ben with fadehold
    scene ben2 with fadehold

    show scg_Dohee nor at girl_center with dissolve

    Dohee "저, 괜찮은 거 맞죠?"

    menu:
        "네?":
            $ n = 1

    narrator_2 "뭐야? 여긴 어디지? 차 안인 것 같은데..."

    # S7

    Dohee "갑자기 멍을 때리고 그래, 아픈 줄 알았잖아요."

    Dohee "오늘부터 바로 일해야 하는데 괜찮은 거 맞죠?"

    me "아, 네..."

    narrator_2 "이상하다?... 난 왜 여기 있는 거고... 게다가... 저 여자, 낯이 익어."

    Dohee "건강관리 잘 해요. 그러다 훅 가. 우리 일이 겉보기엔 쉬워도 진짜 힘들거든요."

    Dohee "아, 당신 이름이 뭐라고 그랬죠?"

    #캐릭터 이름 입력
    $ name = renpy.call_screen("set_name",title=" 제 이름은... ", init_name="이름")
    na "제 이름은 [name]이에요."
    $ player_name = name

    # 그 밑에 이름이 저장된 변수를 finalChecker 함수에 넣어 반환되는 값을 finalConso 에 저장해줍니다.
    $ finalConso = finalChecker(name)


    # S8

    if ( player_name == "이름"):
        Dohee "맞다. 근데 진짜 이름이 이름이에요? 특이하네."
        Dohee "아무튼 [player_name]씨, 다시 한 번 SY엔터테인먼트에 들어온 걸 환영해요."
    else:
        Dohee "맞다, [name]가 그랬죠?"
        Dohee "맞다, [player_name]씨였다. [player_name]씨, 다시 한 번 SY엔터테인먼트에 들어온 걸 환영해요."

    # Dohee "근데 [name]야, 뭐하고 있어? [name]가 그랬다니까?"

    Dohee "[player_name]씨는 앞으로 <스쿨홀릭>의 로드 매니저로 일하게 될 거예요. 멤버들 스케줄이랑 컨디션만 관리해주면 돼요."

    Dohee "간단하죠? 쉽진 않지만요."

    Dohee "너무 겁먹지 마요. 형식상 한 말이고 그냥 잔심부름 같은 거만 하면 되니까요."

    menu:
        "잠, 잠깐만요... 그쪽은 누구시죠?":
            Dohee "처음 본 것 처럼 왜 그래요. 다시 자기소개 해야 해요? 자요."
            $ Dohee_like += 20
        
        "뭔데?":
            Dohee "뭐야, 잠 덜 깼어요? 상사한테 반말? 잠 깨고 이거나 받아요."

        "내가 왜?":
            Dohee "네가, 왜? 네가 지원하셨잖아요? 이런 일인줄 모르고 온 거예요? 네가 다 안 해도 돼요."

    show namecard at item with dissolve

    narrator_2 "<도희의 명함> 획득!"
    $ view_items.append("도희의 명함")

    # 인벤토리에 아이템 추가
    #for "도희의 명함" in view_items:
    #    if "도희의 명함" in view_items:
    #        $ test = 0 # 중복인지 테스트

    #if test == 0: # 중복임
    #    $ n = 1
    #elif:
    #    $ view_items.append("도희의 명함")



    hide namecard

    Dohee "웬만한 일은 치프 매니저인 제가 할테니까요."

    Dohee "형식상 할 말 끝낱으니까 말 놓을게? 꼬우면 [player_name]씨가 상사하면 돼~"

    Dohee "빨리 따라와. 멤버들이 새 매니저를 애타게 기다리거든~"

    # 테스트로 템 하나 더 추가
    narrator_2 "시험용으로 템 하나 더 추가합니다."
    $ view_items.append("스마트폰")

    # S9

    Dohee "들어오면 인사, 기본인 거 알지?"

    hide scg_Dohee
    # 세 수 주 시

    scene black with fadeslow

    Siwoon "형... 팔 무거워요. 내려주세요!"
    
    Sehyuk "주한아, 물 마실래?"

    Juhan "...괜찮아요."

    scene first_meeting_1 with dissolveslow

    scene first_meeting_2 with dissolveslow

    scene first_meeting with fadeslow

    scene metting_a with fade

    narrator_2 "뭐야? 내가 지금 꿈을 꾸는 건가? 그렇다기엔 너무 진짜같은데...?"

    Siwoon "빨리요, 매니저님들 오신다고 했잖아요! 머리 망가지면 안 된단 말이에요..."

    Sehyuk "이미 온 거 같은데?"

    scene practice_room with dissolveslow

    show scg_Soohyun nor at two with dissolve

    narrator_2 ""

    Soohyun "저… 매니저님?"

    na "아... 네?"

    narrator_2 "진짜… 진짜 스쿨홀릭이잖아?"
    
    narrator_2 "내가 방금까지 그리던 애들이… 지금 내 눈 앞에서 살아 움직이고 있다고?"

    narrator_2 "정말? 진짜…? 역시 꿈인가? 꿈인 거지?"

    show scg_Dohee nor at girl_three with dissolve

    Dohee "인사 안 해?"

    na "아...! 이번에 스쿨홀릭 로드 매니저를 맡게 된 [player_name]입니다. 잘 부탁드립니다."

    hide scg_Dohee

    Soohyun "안녕하세요. 스쿨홀릭의 리더 이수현이라고 합니다. 잘 부탁드려요."

    show scg_Sehyuk nor at one with dissolve
    Sehyuk "아아, 반가워요. 서세혁이에요. 앞으로 지겹도록 볼 텐데, 잘 지내봐요."

    show scg_Siwoon nor at four with dissolve
    Siwoon "저야말로 잘 부탁드려요 매니저님! 저는 스쿨홀릭에서 셋째를 맡고 있는 강시운이에요. 오래오래 같이 일하실 수 있도록 저도 열심히 해볼게요."

    show scg_Juhan nor at three with dissolve
    Juhan "…권주한이라고 합니다. 제가 막내라 웬만한 심부름은 제게 시키시면 돼요. 잘 부탁드려요."

    # 1막 엔딩~ 2막 인트로

    # S1

    scene menus with fade

    moderator "올해의 대상은 스쿨홀릭입니다!"

    narrator_2 "드디어, 성공이다."

    narrator_2 "사회자의 입에서 스쿨홀릭의 이름이 나오는 순간, 그간의 고생이 주마등처럼 스쳐지나갔다."

    na "얘들아, 우리가 해냈어! 정말 축하해..!!"

    narrator_2 "그리고 나 자신도 축하해! 드디어 돌아갈 수 있게 됐다니."

    # S2

    scene menus with fade

    show scg_Siwoon nor at four with dissolve
    show scg_Soohyun nor at two with dissolve
    show scg_Juhan nor at three with dissolve
    show scg_Sehyuk nor at one with dissolve

    Soohyun "이 자리에 올라오기까지 함께 해주신 대표님, SY 식구분들, 스텝분들, 그 외에도 수많은 분들께 감사드립니다."

    Soohyun "무엇보다 저희를 응원해주신 스던에게 너무나 감사합니다. 앞으로도 열심히 활동하겠습니다…!"

    # S3

    scene menus with fade 

    na "루루, 너도 고생 많았어. 세상에, 우리가 해냈어 루루야. 믿겨져? 우리 애들이 대상을 받았다구..!"

    narrator_2 "..."

    na "루루야? 어? 얘 어디갔지?"

    if Episode1 == 0:
        jump Episode2

    menu:
        "지나가는 사람한테 물어보자":
            $ n = 1

    # S4

    #show scg_Sehyun with dissolve

    Sehyun "[player_name]씨? 무슨 일 있으세요?"

    na "아 그게.. 루루라는 사람을 찾고 있는데요. 방금 제 옆에 있었는데 사라져서... 혹시 하얀머리 여자아이가 지나가는 걸 보셨나요?"

    Sehyun "하얀머리 여자아이요? 음… 아뇨 보지 못 했어요."

    na "네? 그렇지만… 분명히 여기 있었단 말이에요. 어디로 간 거지…? 화장실이라도 갔나?"

    narrator_2 "근데 루루가 왜 말을 안하고 갔지?"

    Sehyun "정 걱정되시면 저기 경호원한테 찾아가서 물어보시는 건 어떠세요?"

    na "아 네... 감사합니다."

    #hide scg_Sehyun

    narrator_2 "하지만 시상식이 곧 끝나간다. 멤버들과 도희 팀장님이 곧 나를 찾을 것이다. 어떻게 하지?"

    menu:
        "루루를 찾으러 가자": # S5

            #show scg_bodyguards with fade

            bodyguards "흐음... 하얀머리 여자는 보지 못했습니다만. 연락은 취해보셨습니까?"

            na "아, 아뇨..! 잠시만요."

            #hide scg_bodyguards with dissolve

            # 전화번호 누르는 효과음

            ars "지금 거신 번호는 없는 번호 입니다."

            narrator_2 "뭐? 그럴리가...!"


        "일단 멤버들과 만나서 말하자":
            $ n = 1

    # S6
    # 브금 멈춤

    show scg_Dohee nor at girl_center with dissolve

    Dohee "어디 갔었어? 없어져서 놀랐잖아, 빨리와."

    na "아, 죄송합니다. 그게 루루양이 사라져서 찾고 있었어요. 주한이 동창이라던 그 친구요. 혹시 팀장님께선 보셨나요?"

    Dohee "그게 누군데? 주한이 동창? 그런 애는 처음 들어 보는데. 이상한 소리 하지 말고 얼른 와."

    hide scg_Dohee nor

    # S7
    show scg_Siwoon nor at four with dissolve
    show scg_Soohyun nor at two with dissolve
    show scg_Juhan nor at three with dissolve
    show scg_Sehyuk nor at one with dissolve

    Soohyun "저희 왔어요. 무슨 일이에요?"

    na "주한아! 루루가 사라졌어. 네 중학교 친구 하얀 머리 여자애!"

    # S8

    Juhan "네? …무슨 말이에요? 루루가 누구에요?"

    na "뭐?"

    # S9

    Soohyun "…네? 루루…요? 그런 사람은 없는 걸로 아는데…"
    hide scg_Soohyun nor with noisedissolve

    Sehyuk "난 처음 듣는 사람인데? 잘못 안 거 아니야?"
    hide scg_Sehyuk nor with noisedissolve

    Siwoon "[player_name]씨 친구랑..  헷갈리신거 아니에요..?"
    hide scg_Siwoon nor with noisedissolve

    # 대사치면서 하나씩 노이즈

    Juhan "저… 매니저님, 괜찮으세요?"
    hide scg_Juhan nor with noisedissolve

    
    $ Episode1 = 0

    $ renpy.pause(delay = 3, music= None, with_none=None,hard=True,checkpoint=None)
    # $ renpy.quit(relaunch=True, status=0, save = True)
    # $ renpy.reload_script()
    # $ renpy.quit_event()

    scene black with noise_effect

    if Episode1 == 0:
        jump Episode2



    # 권주한도 사라지면서 게임 강제종료


    # 여기까지가 1페이즈~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

















label Episode2:

    scene black

    # S10

    Dohee "저기요!" with vpunch

    scene corridor with fadehold

    show scg_Dohee nor at girl_center with dissolve 

    Dohee "저, 괜찮은 거 맞죠?"

    menu:
        "네?":
            $ n = 1
    
    # S11

    Dohee "갑자기 멍을 때리고 그래, 아픈 줄 알았잖아요."

    Dohee "오늘부터 바로 일해야 하는데 괜찮은 거 맞죠?"

    Dohee "건강관리 잘 해요. 그러다 훅 가. 우리 일이 겉보기엔 쉬워도 진짜 힘들거든요."

    narrator_2 "뭐? 이게 무슨 상황이야?"

    Dohee "아, 당신 이름이 뭐라고 그랬죠?"

    narrator_2 "뭐? 도희가 내가 누군지 모른다고? 어떻게 대답해야 하지?"

    menu:
        "제 이름은 [player_name]입니다.":
            $ n = 2



    if ( player_name == "이름"):
        Dohee "맞다. 근데 진짜 이름이 이름이에요? 특이하네."
        Dohee "아무튼 [player_name]씨, 다시 한 번 SY엔터테인먼트에 들어온 걸 환영해요."
    else:
        Dohee "맞다, [player_name]씨였다. [player_name]씨, 다시 한 번 SY엔터테인먼트에 들어온 걸 환영해요."

    # Dohee "근데 [name]야, 뭐하고 있어? [name]가 그랬다니까?"

    Dohee "[player_name]씨는 앞으로 <스쿨홀릭>의 로드 매니저로 일하게 될 거예요. 멤버들 스케줄이랑 컨디션만 관리해주면 돼요."

    na "제가 누군지 모르시겠어요?"

    $ Dohee_like = Dohee_like - 3

    Dohee "무슨 소리죠? 오늘 초면인 걸로 알고 있는데. 뭔가 착각이라도 한 거 아니에요?"
    
    Dohee "어쨌든, [player_name]씨는 앞으로 <스쿨홀릭>의 로드 매니저로 일하게 될 거예요. 멤버들 스케줄이랑 컨디션만 관리해주면 돼요."
    
    Dohee "간단하죠? 쉽진 않지만요."

    Dohee "너무 겁먹지 마요. 형식상 한 말이고 그냥 잔심부름 같은 거만 하면 되니까요."

    narrator_2 "세상에, 이곳에 처음 왔을 때와 똑같은 상황이잖아?! 기억대로라면 이제…"

    menu:
        "혹시, 명함 주실 수 있나요?":
            $ Dohee_like += 3
            Dohee "어머, 어떻게 알았대? 안 그래도 주려고 했어요. 자요, 안 잃어버리게 조심해요."
        
        "저, 연락처 좀 받을 수 있을까요?":
            $ Dohee_like += 5
            Dohee "[player_name]씨는 제 스타일이 아닌데. 농담이고, 안그래도 명함 주려고 했어요. 자요."


    show namecard at item with dissolve

    narrator_2 "<도희의 명함> 획득!"

    hide namecard

    Dohee "형식상 할 말 끝낱으니까 말 놓을게? 꼬우면 [player_name]씨가 상사하면 돼~"

    Dohee "빨리 따라와. 멤버들이 새 매니저를 애타게 기다리거든~"

    narrator_2 "이건... 이건 정말 말도 안 돼."


    # S12
    Dohee "들어오면 인사, 기본인 거 알지?"


    hide scg_Dohee nor
    # 세 수 주 시

    scene black with fadeslow

    Siwoon "형... 팔 무거워요. 내려주세요!"
    
    Sehyuk "주한아, 물 마실래?"

    Juhan "...괜찮아요."


    scene first_meeting_1 with dissolveslow

    scene first_meeting_2 with dissolveslow

    scene first_meeting with fadeslow

    narrator_2 "또... 같은 상황이야."

    Siwoon "빨리요, 매니저님들 오신다고 했잖아요! 머리 망가지면 안 된단 말이에요..."

    Sehyuk "이미 온 거 같은데?"

    scene practice_room with dissolveslow

    show scg_Soohyun nor at two with dissolve

    Soohyun "저… 매니저님?"

    menu:
        "네, 수현씨?":
            $ tem = 2
            $ Dohee_like += 5
            Soohyun "아, 안녕하세요. 이미 알고 계시네요."
            Soohyun "스쿨홀릭의 리더인 이수현이라고 합니다."

        "네, 세혁씨?":
            $ tem = 1
        "왜, 주한아?":
            $ tem = 3
            $ Juhan_like -= 3
        "왜, 시운아?":
            $ tem = 4
            $ Siwoon_like -= 2

    if tem == 1:
        Soohyun "아, 저는 이수현입니다. 세혁이 형은 이쪽이에요."
        show scg_Sehyuk nor at one with dissolve
        
    elif tem == 3:
        Soohyun "아, 저는 이수현입니다. 주한이는 이쪽이에요."
        show scg_Juhan nor at three with dissolve
    elif tem == 4:
        Soohyun "아, 저는 이수현입니다. 시운이는 이쪽이에요."
        show scg_Siwoon nor at four with dissolve

    if tem != 2:
        Soohyun "…아무튼. 저는 스쿨홀릭의 리더 이수현이라고 합니다."

    narrator_2 "뭐야… 스쿨홀릭 애들도 나를 못 알아보는 건가? 이럴수가...."

    if tem != 3:
        show scg_Dohee nor at girl_three with dissolve
    else:
        show scg_Dohee nor at girl_four with dissolve

    Dohee "자기소개 안 해?"

    na "아...! 이번에 스쿨홀릭 로드 매니저를 맡게 된 [player_name]입니다. 잘 부탁드립니다."

    hide scg_Dohee

    if tem == 1:
        Sehyuk "아아, 반가워요. 서세혁이에요."

        show scg_Siwoon nor at four with dissolve
        Siwoon "잘 부탁드려요, 매니저님. 전 강시운 이라고 해요!"

        show scg_Juhan nor at three with dissolve
        Juhan "…권주한이라고 합니다. 잘 부탁드려요."

    elif tem == 2:
        show scg_Sehyuk nor at one with dissolve
        Sehyuk "아아, 반가워요. 서세혁이에요."

        show scg_Siwoon nor at four with dissolve
        Siwoon "잘 부탁드려요, 매니저님. 전 강시운 이라고 해요!"

        show scg_Juhan nor at three with dissolve
        Juhan "…권주한이라고 합니다. 잘 부탁드려요."

    elif tem == 3:
        show scg_Sehyuk nor at one with dissolve
        Sehyuk "아아, 반가워요. 서세혁이에요."

        show scg_Siwoon nor at four with dissolve
        Siwoon "잘 부탁드려요, 매니저님. 전 강시운 이라고 해요!"

        Juhan "…권주한이라고 합니다. 잘 부탁드려요."
    
    elif tem == 4:
        show scg_Sehyuk nor at one with dissolve
        Sehyuk "아아, 반가워요. 서세혁이에요."

        Siwoon "잘 부탁드려요, 매니저님. 전 강시운 이라고 해요!"

        show scg_Juhan nor at three with dissolve
        Juhan "…권주한이라고 합니다. 잘 부탁드려요."

    narrator_2 "확실해, 내가 몇 달 전에 이곳에 처음 왔을 때와 똑같은 상황이야."

    narrator_2 "그런데…도대체 왜, 다시 여기로 돌아온거지?"

    # S13

    #hide scg_Sehyuk nor and scg_Soohyun nor and scg_Juhan nor and scg_Siwoon nor
    #$ renpy.scene()
    #scene practice_room
    $ renpy.hide("scg_Sehyuk nor", layer='master')
    $ renpy.hide("scg_Soohyun nor", layer='master')
    $ renpy.hide("scg_Juhan nor", layer='master')
    $ renpy.hide("scg_Siwoon nor", layer='master')

    show scg_Dohee nor

    Dohee "자, 자기소개는 이만하면 됐겠지? 이거받아. 애들 스케줄이야."

    show namecard at item with dissolve # 스케줄표

    narrator_2 "<스케줄표> 획득"

    hide namecard

    Dohee "아직은 공백기라 무대준비보다는 따로따로 봐줘야 할 일이 많을거야. 멤버별로 스케줄 따로 뽑아 놨으니까 실수하지 않게 잘 외워둬."

    narrator_2 "어? 공백기라니! 분명 전에는 바로 무대에 올라갔었는데…! 잠깐만, 그러면 지금은 무슨 활동을 하고 있는 거지?"

    menu:
        "\[세혁의 개인 스케줄을 확인한다]":
            $ n = 2

        "\[수현의 개인 스케줄을 확인한다]":
            $ n = 2

        "\[시운의 개인 스케줄을 확인한다]":
            $ n = 2

        "\[주한의 개인 스케줄을 확인한다]":
            $ n = 2

    narrator_2 "뭐야? 이 노래를 준비 중이라는건…!"

    Dohee "확인은 이따하고, 이거 받아."

    narrator_2 "<휴대폰> 획득"

    Dohee "멤버들 번호랑 내 번호가 저장된 폰이야. 잃어버리지 말고, 번호 유출 안되게 조심하고. 알지?"

    Dohee "그리고 지금은 애들 연습시간이니까, 방해하지 말고 옆에 가만히 있어. 난 이만 바빠서. 연습 열심히들 해~"

    hide scg_Dohee nor at dissolve

    narrator_2 "잠깐의 정적 후, 시운이 반가운 표정으로 다가왔다."

    $ renpy.show("scg_Siwoon nor", layer='master')
    $ renpy.with_statement(dissolve)

    Siwoon "매니저님 굉장히 성실해 보이세요, 저희를 돌봐주는게 힘드실텐데.. 폐 안가도록 부지런히 움직여 볼게요."
    
    Siwoon "아, 좋아하시는 음료 있어요? 회사 앞에 카페에 마들렌이 굉장히 맛있는데.."

    narrator_2 "들뜬 얼굴로 설명하던 시운이가 갑자기 헉 소리를 내며 입을 가렸다."

    Siwoon "팀장님껜 비밀이에요, 다이어트 하라고 하셔서... 나중에 몰래 사와서 같이 먹어요."

    $ renpy.show("scg_Sehyuk nor", layer='master')
    $ renpy.with_statement(dissolve)

    Sehyuk "그래? 몰래 마들렌 사와서 먹는다고? 재밌겠네."

    Siwoon "세혁이 형 이르실 거 아니죠?"
    
    Sehyuk "글쎄."
    
    Siwoon "수현이 형…"

    Soohyun "무리가 갈 정도로 먹지만 마."

    Sehyuk "우리 리더는 너무 무르다니까~"

    Siwoon "그정도로는 안 먹어요..! 멤버들 것도 사올거니까 비밀로 해줘요."
    
    Siwoon "그럴 거죠 매니저님?"

    menu:
        "앗 네…! 물론이죠!":
            Siwoon "역시 매니저님..! 저희 분명 잘 맞을 것 같아요..!"
        "싫은데?":
            Siwoon "...매니저님도.. 세혁이 형 편이셨구나.. 알았어요.."

    Sehyuk "그쯤하고 마저 연습하자. 아, 매니저님. 물 좀 사와줄 수 있어요?"

    menu:
        "내가 왜? 네가 사와":
            Sehyuk "오, 의왼데?"

            Sehyuk "매니저면 매니저 일 해야죠? 우리 연습할 동안 좀 부탁해요."

        "아 물론이죠! 금방 다녀올게요!":
            Soohyun "다녀오세요, 매니저님."
            
        "알겠습니다! 물 말고 또 필요한 거 있나요?":
            Siwoon "저, 저.. 저..? 아 밴드! 밴드 사다주세요."

            narrator_2 "네에, 금방 다녀올게요!"

            Juhan "감사합니다, 매니저님."

    menu:
        "\[연습실을 나간다.]":
            $ n = 2
    
    na "좋아, 내가 지갑을 어디다 뒀더라?"

    narrator_2 "지갑을 찾기 위해 주머니를 뒤적이다가 무언가가 내 손에 걸렸다."

    na "…어? 이건.. 아까 루루가 줬던 편지잖아. 뭐야? 어째서 남아있는 거야?"

    # 루루의 편지

    narrator_2 "맞아, 주한이는 루루랑 이어졌었지! 내가 만들어놓고 이걸 놓치고 있었을 줄이야."

    narrator_2 "그치만 다들 알아서 사귀고 있는 줄 알았는데…그게 아니었나?"

    narrator_2 "으음… 나중에 주한이에게 더 물어봐야겠어."


###########################################################################################################
################################### 2챕터 시작#######################################################################################################
################################### #######################################################################################################
    
    # S1

    narrator_2 "며칠 뒤, 회의실"

    narrator_2 "오늘은 앨범 타이틀곡에 대한 설명을 듣는 날이다. 이번 앨범 이름이…"


    menu:
        "School Holic 1st story":
            narrator_2 "맞아, \[School Holic 1st story]였어."

        "우당탕탕 스쿨홀릭":
            $ miss_count += 1
            narrator_2 "\[우당탕탕 스쿨홀릭]...? 그런 이름이었던가?"

            narrator_2 "아 그래, \[School Holic 1st story]였어. 이런, 헷갈렸네."

    Soohyun "안녕하세요, 감독님."

    ParkPD "아, 왔군요."

    members "안녕하세요. 스쿨홀릭입니다!"

    ParkPD "네네, 반가워요"

    ParkPD "오늘은 우리 타이틀 곡 안내하고, 가사 파트 확인 할겁니다. 앨범 컨셉은 지난번에 소개해줬으니 알고 있겠죠?"
    
    narrator_2 "맞아, 앨범 타이틀 곡부터 준비했었지. 앨범의 컨셉은.."

    menu:
        "학생의 풋풋함":
            Soohyun "네. 저희 컨셉은 \[학생의 풋풋함]이죠?"
            narrator_2 "다행이야, 맞췄다!"
        
        "어른의 섹시함":
            Soohyun "네. 저희 컨셉은 \[학생의 풋풋함]이죠?"
            $ miss_count += 1

        "늑대의 야성미":
            Soohyun "네. 저희 컨셉은 \[학생의 풋풋함]이죠?"
            $ miss_count += 1

    if miss_count == 1:
        narrator_2 "아 이번에는 틀렸네…"

    elif miss_count == 2:
        narrator_2 "아이 진짜, 또 틀렸잖아."

    ParkPD "좋아요, 잘 알고 있군요. 그럼 전체적인 곡 소개부터 할게요."

    narrator_2 "타이틀곡 제목은 또 뭐였더라..."

    menu:
        "School at sunset":
            narrator_2 "맞아, School at sunset. 내가 지었지만 이쁜이름이었어"
        "After School":
            narrator_2 "애프터스쿨은...다른 그룹 이름 표절이잖아!!!"
        "School Holic":
            narrator_2 "스쿨 홀릭은 애들 이름이고..나 바보야? 내가 지어놓고 뭐하는거람..."

    Composer "저희 이번 곡 제목은 <School at sunset>입니다."

    Composer "제목에서 볼 수 있다시피 방과후 학교가 배경이에요."

    Siwoon "저희랑 잘 맞는 배경이네요."

    Lyricist "전체적으로는 학생이라는 컨셉에 맞춰서 밝고 산뜻하게 진행됩니다."

    Lyricist "다만 방과후 비밀 연애라는 컨셉을 넣어서 대중적인 선호도 잡으려고 해요. 요즘 트랜드가 비밀연애잖아요?"

    Siwoon "아..그런가요? ..좋네요."

    narrator_2 "맞아, 내가 애들 컨셉 생각할 때 그런 내용이 유행하긴 했었지."

    ParkPD "그럼. 우리 김율 작사가님이 이 mz세대라 이런거를 또 잘 알거든."

    Lyricist "아, 아니에요. 저는 아직 많이 부족한걸요.."

    Composer "하하, 박피디님 칭찬은 보통 칭찬이 아니니 겸손 떨 필요 없어요. 나한테도 저런 칭찬 잘 안해주신다니까?"

    narrator_2 "음...이야기가 딴길로 새는 것 같은데."

    menu:
        "조용히 있기":
            Soohyun "저기, 그럼 가사를 좀 볼 수 있을까요?"

            Lyricist "아, 네네. 여기 있습니다."

        "저기, 그럼 가사지는 어디에 있나요?":
            Lyricist "아! 여기있어요."

            narrator_2 "수현이 고맙다는 듯한 눈빛을 보내왔다."

        "하하, 대단하신데요, 작사가님?":
            Lyricist "아 하하, 고마워요… 매니저님? 맞으신가요?"

            Sehyuk "칭찬은 이만하면 충분한 것 같으니, 가사 좀 보여주실래요?"

            Lyricist "아, 네. 죄송해요, 바로 드렸어야 했는데."


    narrator_2 "<가사집> 획득"

    # 이미지

    narrator_2 "어..? 근데 이거..."

    menu:
        "멤버들과 눈짓하기":
            narrator_2 "세혁이와 눈이 마주쳤다. 세혁이가 할 말이 있느냐는 듯 시선을 보내온다."

            narrator_2 "나는 가사지와 세혁이를 번갈아가며 쳐다봤다."

            Sehyuk "저기, 질문이 있는데요."

            Lyricist "네?"

            Sehyuk "이 가사, 학교 컨셉이랑 좀 안 맞지 않나요?"

        "가사가 야한데요?":
            Lyricist "무, 뭐라고요?"

            Siwoon "헉...! 매, 매니저님?"

            ParkPD "아이고, 우리 매니저님이 돌직구시네, 하하. 그래도 일할 때는 말을 가려서 하도록 해요."

            narrator_2 "아니 이거 내가 처음에 썼던 가사잖아! 미친 거 같아서 지웠었는데 왜 여기서 나오냐고.."

            Soohyun "아… 죄송합니다. 매니저님께서 오신지 얼마 안 되셔서 아직 일이 익숙하지 않으세요. 작사가님께 달리 나쁜 뜻이 있었던 게 아닐 거예요."

            Soohyun "그럼에도 기분이 나쁘셨다면 제가 매니저님 대신에 사과 드리겠습니다."

            narrator_2 "수현이가 고개를 숙여 사과했다. 수현아...! 이 천사!! 역시 제일 효자야."

            Lyricist "아, 아니에요, 괜찮아요. 하하, 처음이면 그럴 수도 있죠. 저도 처음에는 실수를 했는걸요.."

            Sehyuk "아, 그런데요. 질문이 있습니다."

            Lyricist "아, 네?"

            Sehyuk "가사가 학교 컨셉과는 좀 다르지 않나요?" 

        "저어, 학생 컨셉인데 가사 괜찮은건가요..?":
            narrator_2 "시운이가 기다렸다는 듯 말을 꺼냈다."
            
            Siwoon "저도.. 매니저님 말이 맞다고 생각해요. 가사가 정말 예쁘고 좋은데.. 학교라는 전체 컨셉과는 조금 거리가 먼 것 같은 느낌이라서요."

        
    Lyricist "아, 그렇지 않아요. 비밀연애의 간질거리는 느낌을 조금 더 강조했을 뿐이에요. 전반적으로는 학교 컨셉으로 가고있어요."

    Composer "맞아요, 멜로디 라인도 풋풋한 학생의 느낌이 나도록 짜여있어요."

    Sehyuk "아, 네. 근데 풋풋한 느낌은 별로 안드는 것 같은데요."
        
    narrator_2 "이거 어째 분위기가..어떻게 할까?"

    menu:
        "가만히 있는다":
            Lyricist "네? 음, 저는 그렇지 않은데요."

            Sehyuk "아뇨. 풋풋함과 비밀연애는 컨셉 충돌이 발생하지 않나요?"

            ParkPD "아, 그 부분은 프로듀싱 팀 내에서도 나왔던 말이에요."

        "그러면, 먼저 가사를 전체적으로 설명해주시겠어요?":
            Lyricist "아 네! 학교 배경에 맞추어서, 도입부는 방과 후의 학교로 잡았어요. 수업이 끝난 교실에 멤버들과 애인이 단둘이 남게돼요."

            Lyricist "두사람은 비밀연애를 하고 있기 때문에, 은밀하고 간질거리는 느낌이 들도록 했어요. 그래서 애인과의 거리가 가깝다는 걸 보여주려고 구체적인 묘사를 넣은거예요."

            ParkPD "아, 그 부분은 프로듀싱 팀 내에서도 나왔던 말이에요."

        "가사가 나쁘다는 뜻이 아니에요.":

            na "그치만, 풋풋한 학교의 느낌과는 거리가 있는 느낌이지 않나요..?"

            Lyricist "네, 하지만 은밀하고 간질거리는 느낌을 조금 더 살렸을 뿐이에요."

            Sehyuk "그 은밀하고 간질거리는 느낌이 풋풋한 학생 컨셉과 충돌하고 있는 것 같습니다만."

            ParkPD "아, 그 부분은 프로듀싱 팀 내에서도 나왔던 말이에요."

        "그러니까요, 학생 컨셉에 스킨십을 암시하는 가사는 아니지 않나요?":
            Sehyuk "제 말이 그 말입니다."

            Lyricist "그런건 아니에요!"

            ParkPD "아이고, 요즘 세상에 그랬다가는 큰일납니다. 그런건 절대 아니에요."

            ParkPD "다만, 그부분은 프로듀싱 팀 내에서도 나왔던 말이에요."


    ParkPD "단순 학생컨셉으로 가면 기존의 다른 아이돌들과 비슷해지는 것 같아서, 비밀연애라는 설정곡을 추가 했습니다."

    Composer "그리고 충분한 회의를 거쳐서 최종적으로 나온 곡이니 너무 염려하지 않아도 됩니다."
    
    narrator_2 "아, 그런 말이 아닐텐데..."

    narrator_2 "수현이가 세혁이와 PD측을 난감한 눈으로 번갈아 보았다."

    Soohyun "하지만… 풋풋한 느낌과 은밀한 느낌 두 가지를 다 살릴 수는 없을 거 같아요."

    Lyricist "그 두 개를 살리는 게 이번 앨범의 컨셉이에요."

    Lyricist "그리고, 감독님께서 말씀하셨다시피 이미 프로듀서분들께서 의논을 끝내고 완성한 곡이라서, 바꾸기가 어려워요."

    Sehyuk "글쎄요. 어쨌든 그 곡을 부르는 건 저희예요. 그리고 저희는 두 컨셉을 다 살리기가 어려울거 같다고 지금 말씀드리고 있고요"

    Lyricist "세혁씨, 이러시면 곤란해요. 이미 다른 전문가분들이 다 검토하신 내용이고, 여러분들 회사측에서도 확인하고 승인 내어준 곡입니다."
    
    Lyricist "여러분들 마음에 안든다고 곡을 맘대로 바꿀 수는 없어요."

    Sehyuk "곤란한 건 제쪽이죠. 제가 곡을 바꿔달라고 했습니까?"

    Sehyuk "저는 저희 스쿨홀릭의 컨셉과 맞지 않다고 아까부터 재차 말씀드리고 있습니다."

    Lyricist "아니, 그게 컨셉이라니까요! 그걸 살리는 게 여러분들의 역할이라고요. 가사가 바꾸고 싶다고 마음대로 바뀌는 줄-!"

    ParkPD "그만, 그만! 둘 다 진정해요."

    ParkPD "우선 세혁군? 이 가사는 작사님이 몇날며칠을 걸려서 쓴 가사입니다. 그렇게 쉽게 바꿀 수 있지가 않아."

    ParkPD "또한 김율씨 말대로 이미 윗선에서 오더가 내려진 상황이라 우리도 마음대로 컨셉을 바꾸기도 어렵고."

    Sehyuk "하… 이해했습니다."

    narrator_2 "세혁이는 상당히 열이 받아 보였지만 한발 물러선다는 듯 자리에 앉았다."

    ParkPD "그리고 김율씨, 언성을 낮추도록 해요. 이 자리는 멤버들에게 곡 컨셉을 알려주고 디렉팅하는 자리도 맞긴 하지만, 멤버들의 의견을 듣고 곡을 어떻게 디렉팅할지 의논하기 위한 자리이기도 합니다."

    ParkPD "또한 디렉터는 나지, 당신이 아닙니다. 조심하세요."

    Lyricist "죄, 죄송합니다, 감독님..."
    
    narrator_2 "으아, 분위기가 살벌해졌어! 어떡하면 좋지..."

    ParkPD "우선, 멤버들 의견은 잘 알겠어요."

    ParkPD "우리쪽에서도 한 번 나왔던 의견이니, 다시 검토해보도록 하지. 그럼-"

    Juhan "저, 죄송하지만 한가지 여쭤볼 게 있는데요. 괜찮을까요?"

    Composer "아 네, 편하게 말하세요. 어떤거죠?"

    Juhan "실례가 안 된다면 제가 다시 가사를 써 봐도 괜찮을까요?"

    Juhan "…아무래도 아직 학생인 제가 써보면 새로운 느낌을 낼 수 있지 않을까 싶어서요."

    Lyricist "...괜찮은 건가요, 감독님?"

    ParkPD "율씨만 괜찮다면, 좋은 생각인거 같은데."

    Lyricist "뭐, 그럼. 그렇게 해 보세요."

    Juhan "감사합니다."

    ParkPD "좋아, 좋아. 자, 그럼 다음 미팅때 보도록 하죠. 날짜는 매니저한테 나중에 알려주겠어요."

    Composer "다들 수고하셨어요."

    members "네, 수고하셨습니다."


    # S2

    Soohyun "주한아, 무슨 생각인 거야?"

    narrator_2 "내가 만든 자식이지만 나도 궁금하다."

    Juhan "…말 그대로였어요, 형."

    Juhan "작사가님께 다시 써달라고 하는 것도 문제가 있을 것 같고, 이 가사를 그대로 사용하는 것도 아닌 것 같아서요. 그래서 제가 하겠다고 했어요."

    Juhan "…혹시 민폐였을까요."

    narrator_2 "주한이가 멤버들의 눈치를 살폈다. 나는 내가 만들었지만 얘를 제일 모르겠어."

    Sehyuk "난 가끔 보면 주한이가 제일 모르겠단 말이지? 조용한 거 같은데 은근히 할 말은 다 하잖아?"

    narrator_2 "내 말이 그말이야!"

    Siwoon "아, 매니저님. 오늘 고생 많으셨어요. 생각보다 길고.. 일도 많았네요."

    menu:
        "별말씀을요.":
            Siwoon "다음엔 더 빨리 원활하게 끝나길 바래야죠.."

            Siwoon "설마 매번 다투어야 하는 건 아니겠죠? 으으.."

        "고마워요? 고마우면 보너스나 줘요.":
            Siwoon "보너스요? 으음.. 보너스로 마들렌에 커피! 아니면 밥으로 사드릴게요. 이번 활동 끝나면요."

        "아니에요, 저는 별로 한것도 없는걸요.":
            Siwoon "왜 하신게 없어요! 회의 참여 같이 해주셨잖아요. 할 일을 다 하신 것 만으로 수고하셨는걸요."

    Soohyun "그런데 주한아. 가사를 어떻게 쓸 생각이야? 우리가 도와줄 게 있을까?"

    Juhan "아, 괜찮아요. …제가 예전에 겪었던 일을 생각하며 써보려고요. 신경써줘서 고마워요, 형."

    Sehyuk "그래? 뭐, 생각해둔 게 있으니 나섰겠지. 우린 너무 간섭하지 말자. "
    
    narrator_2 "세혁이가 수현이를 가볍게 툭툭 쳤다."

    Soohyun "…그래도 정 어려우면 우리한테 말해줘. 도와줄 수 있는 건 뭐든 도와줄게."

    Juhan "네, 형. 너무 걱정하지 마세요."

    Sehyuk "알아서 잘 하겠지, 뭐. 누구랑 다르게 말이야?"

    Siwoon "...설마 저한테 하신 말은 아니죠?"

    Sehyuk "맞는데?"

    narrator_2 "세혁이가 뻔뻔하게 맞받아쳤다. 내가 만들었지만 정말 재수없다..."

    Siwoon "저도 잘 하거든요? 나빠요, 형"
    
    Sehyuk "아, 진짜? 그렇지. 우리 시운이도 잘하지~ "

    narrator_2 "세혁이가 능청맞게 시운이의 머리를 쓰다듬곤 지나갔다."

    na "자, 자. 다들 연습실로 돌아가죠."

    Soohyun "저희 다음 스케줄이 뭔가요, 매니저님?"

    # 스케줄표 뜸

    narrator_2 "헉... 다음 스케줄이 가사 암기하고 연습하는 거였잖아..! 어떡하지..."

    menu:
        "도희에게 오늘 있었던 일을 알리고 도희의 말을 기다린다.":
            na "잠시만요, 여러분."

            Soohyun "무슨 일 있나요?"

            na "아니, 잠시 도희팀장님에게 전화를 해야할 것 같아서.."

            Soohyun "도희 매니저 님께요? 왜요?"
            
            na "아, 그.. 우리 스케줄이 조금 바뀌어서, 일단 여쭤봐야 할 것 같아서요"

            Soohyun " 아, 그렇겠네요."

            Soohyun "저희는 여기 계속 서 있을 순 없으니까, 연습실에 들어가 있을게요. 문제가 생기면 알려주세요."

            na "아, 네! 그럼 저는 얼른 통화하고 올게요."

            $ miss_count == 1

        "일단 멤버들에게 연습을 마저 하라 한다.":
            na "이런, 아무래도 뒤에 스케줄을 조정해야할 것 같네요."
            
            na "일단... 그동안 다들 들어가서 연습 마저 하고 있어요. 조정되는 대로 다시 알려 드릴게요."

            Sehyuk "오, 일 잘하시네요? 그럼 우린 들어가 있을게요."

            Soohyun "감사합니다, 매니저님."

            Siwoon "수고하셨어요! 고마워요."

            $ miss_count == 1

        "나도 모르겠다고 한다.":
            na "아.. 저도 잘 모르겠어요. 저희 원래 스케줄이 가사 받아서 외우고 연습하는 거였는데.. 어떡하면 좋죠?"

            Sehyuk "그걸 우리한테 물어보면 곤란한데~ 매니저님 일이잖아요? "

            Siwoon "아... 너무 그러지 마세요 형.. 처음이신데 실수하실 수도 있죠."

            Siwoon "저, 매니저님? 이런 일이 있으면 보통은 도희 매니저님께 알려드리고 연습시간으로 대체하고는 했어요."

            Juhan " …네 맞아요. 저희는 연습하면 될 것 같아요."

            Soohyun "아, 매니저님. 제가 도희 매니저님께 연락 드렸어요. 곧 도희 매니저님께서 전화 주실 거예요."

            Soohyun "다음에 비슷한 문제 생기시면 팀장님께 연락 드려서 조치 취하시면 돼요."

            na "아, 고마워요...그리고 죄송합니다."

            Soohyun "괜찮아요. 처음에는 모르는 게 당연하잖아요."

            Sehyuk "우리 리더님, 매니저님 그만 다독이고 슬슬 와."

            Sehyuk "매니저님? 우린 연습실 가있을게요. 도희 매니저님이랑 끝나는 대로 알려줘요. 가자, 얘들아."

            $ miss_count == 0

    # 멤버들 퇴장


    # S3

    Dohee_call "어, 왜? 무슨 일이야."

    na "저, 팀장님. 오늘 회의에 있었던 일 때문에 말씀드릴 게 있는데요.."

    Dohee_call "회의? 어어, 그래. 말해봐. 나 바쁘니까 핵심만 말해줄래?"

    menu:
        "스케줄 문제를 먼저 언급한다.":
            
            na "회의때 문제가 생겨서 뒤의 스케줄이 밀렸습니다. 어떻게 할까요?"

            Dohee_call "무슨 문제가 있었는데?"
            
            na "가사 컨셉에 대해 멤버들과 작사가님의 의견이 달라서 의논이 진행 됐는데 결국 끝이 나지 않았거든요. 그런데 주한씨가 직접 가사를 써오겠다 해서 우선 그렇게 일단락 되었습니다."

            Dohee_call "뭐? 주한이가 가사를 쓰기로 했다고? 참신하네."

            Dohee_call "그래서 스케줄이 어떻게 밀렸는데?"

            na "원래는 가사지를 받아서 가사를 외우고 연습해야하는데, 가사지를 받지 못했어요. 그래서 그부분 스케줄이 비게 되었어요."

            Dohee_call "그럼 멤버들은 뭐하고 있는데?"

        "세혁이와 작사가의 다툼을 먼저 언급한다.":
            na "회의때 세혁씨랑 작사가님이 싸워서...회의가 흐지부지 끝났어요."

            Dohee_call "세혁이랑 작가님이 싸워?"

            na "그게...세혁씨는 은밀하고 성적인 느낌이 싫은데 작사가님은 그게 컨셉이라고 하셔가지고요.."

            na "결국 두사람의 의견이 좁혀지지 않아서 주한이가 가사를 써오는 걸로 끝이 났어요."

            Dohee_call "세혁이랑 작사가랑 싸웠는데 주한이가 가사를 써오기로 결론났다고? 뭔 일이래."

            Dohee_call "뭐, 유혈사태만 없으면 됐지. 그래서?"

            na "네? 아, 그래서 뒤에 가사 암기하고 노래 연습하는 스케줄이 비게 되었어요."

            Dohee_call "아하.. 지금 애들은 뭐하는데?"

    
    na "일단 연습실에 들어가서 연습하고 있어요."

    Dohee_call "그래.. 그럼 나머지 시간도 연습하라 그래. 대신 오늘 스케줄은 좀 일찍 끝내는 걸로 할까? 애들 좋아하겠네."

    na "네, 알겠습니다."

    if miss_count == 1: #주인공이 전화 건 경우
        Dohee_call "바로 전화한거지? 잘했어."

        Dohee_call "앞으로 비슷한 일 있으면 바로 전화해줘. 특히 애들 끼리 무슨 일 생기면 반드시! 알았지?"

        na "네. 감사합니다."

    elif miss_count == 0: # 도희가 전화 건 경우
        Dohee_call "앞으로 비슷한 일 있으면 바로 나한테 전화해. 애들 통하지 말고. 매니저는 너지 멤버들이 아니잖아? 특히 외부 프로듀서들과 만날 땐 반드시."

        Dohee_call "알아들었지"

        na "네. 죄송합니다."

    Dohee_call "스케줄 밀릴 일이 있는건 [player_name]씨가 알아서 조정해도 괜찮아. 괜히 매니저가 있는게 아니지. 나한텐 얘기만 즉각적으로 해주면 돼."

    na "네, 명심하겠습니다."

    Dohee_call "그래, 수고 했고 더 수고해~"

    # 전화 끊김음

    na "휴... 대충..된건가. 이제 애들한테 다시 알려줘야겠다."

    # S4

    narrator_2 "나는 통화를 마치고 다시 연습실로 돌아왔다."

    na "여러분, 도희 팀장님께 말씀 드렸는데 나머지 시간에는 개인 연습 하는게 좋을 것 같다네요."

    na "대신 오늘 스케줄을 조금 일찍 끝내도 된다고 하셨어요! 그런 김에,"

    menu:
        "저녁을 다같이 먹는 건 어떤가요?":

            Sehyuk "저녁? 괜찮은데? 다들 딱히 개인 스케줄 없잖아, 좋지?"

            Siwoon "저는 좋아요! 매니저님 환영회도 같이 하면 좋을 것 같은데…"

            Juhan "…저도 좋아요."
            
            Siwoon "그런데.. 회식이면 팀장님도 불러야 하지 않을까요?"

            Soohyun "매니저님 환영회라면 부르는 게 좋을 것 같아."

            Soohyun "매니저님, 혹시 팀장님도 괜찮으신지 여쭤봐주실 수 있을까요?"

        "저녁에 술 한잔 할까요?":
            Sehyuk "술? 난 좋은데?"

            Soohyun "네? 음… 그래도 처음 뵈었는데 술은 조금 이르지 않을까요?"

            Siwoon "저.. 우리 주한이 아직 성인이 아니잖아요? 우리 막내 좀 신경 써주세요…!"

            Juhan "…저는 먼저 숙소에 들어가있어도 괜찮아요."

            Sehyuk "그러게. 우리 막내 아직 술집도 못 들어가는데? 매니저님, 너무 무신경한 거 아니야?"

            na "아, 제가 그 생각을 못했네요, 죄송해요.."

            Soohyun "괜찮아요. 아직 처음이시니까 헷갈릴 수도 있죠. 아니면 저녁이라도 다 같이 먹으면 어떨까요?"

            Siwoon "저녁..! 저는 좋아요! 다들 어때요?"

            Sehyuk "좋은데? 매니저님 환영식 해 줘야지. 어때요, 매니저님?"

            menu:
                "좋아요! 저야 감사하죠..":
                    Soohyun "그럼 개인 연습 끝나고 이따 저녁 먹으러 가요."
                    
                    Soohyun "아, 혹시 팀장님도 괜찮으신지 여쭤봐주실 수 있나요?"

                    Sehyuk "팀장님도 부르게?"

                    Soohyun "매니저님 환영회니까 다 같이 먹는 게 좋을 것 같아서요. "

                    Sehyuk "하긴 그렇겠네."

                    Soohyun "그럼.. 매니저님, 팀장님께 연락해주시겠어요?"
                    
                    menu:
                        "도희 한테 전화 걸기":
                            $ callormessage == 0

                            narrator_2 "뚜르르… 뚜르르…"

                            narrator_2 "뚝."

                            narrator_2 "연결이 되지 않아 음성사서함으로 연결되오며…"
                            # 음성으로 바꿔야함

                            na "아, 팀장님께서 안 받으시네요."

                            Sehyuk "바쁜 거 아니에요?"

                            Soohyun "부재중 찍혔으니까 나중에 보시면 다시 연락 주실 거예요. 연락 닿으시면 저희한테 알려주세요."

                            Siwoon "그럼 기다리는 동안 저희 뭐 먹을지 생각해봐요..!"

                            na "아, 그럴까요? 다들 어떤 음식 좋아하세요?"

                        "도희 한테 문자하기":
                            $ callormessage == 1

                            na "팀장님 바쁘셔서 일단 문자로 넣었어요. 이따 답장 오면 알려 드릴게요."

                            Siwoon "그럼 기다리는 동안 저희 뭐 먹을지 생각해봐요..!"

                            na "좋네요. 다들 어떤 음식 좋아하세요?"
                    
                    # 메뉴 고르기 힌트
                    Siwoon "저는 음.. 다 잘 먹는데, 매운 건 잘 못 먹겠더라구요."

                    Sehyuk "애기 입맛이네."

                    Siwoon " 매운 거 좀 못 먹을 수도 있죠.. 형이 어른 입맛인거예요..!"

                    narrator_2 "세혁이는 표정변화 하나 없이 입을 다물었다. 일부러 무시한 건가…?"

                    narrator_2 "가만히 대화를 듣고있던 주한이가 조심스럽게 앞으로 나섰다."

                    Juhan "…저도 다 먹긴 한데… 자극적인 건 안 좋아해요."

                    Soohyun "저는 갑각류 알러지가 있어서… 이것만 빼면 다 먹어요."

                    Sehyuk "난 양식. 한식은 별로 안 좋아해요."

                    Sehyuk "잡담은 이쯤하면 됐으니까, 슬슬 연습할까? 들어가자."

                    narrator_2 "세혁이가 주한이와 시운이를 끌고 안으로 들어갔다."

                    Siwoon "앗 형..! 이거 놔 주세요...!"

                    Soohyun "그럼 매니저님. 저희 연습하는 동안 음식점 고르는 것 좀 부탁드릴게요."

                    na "네, 알겠습니다."

                "아, 죄송하지만 오늘은 조금 어려울 것 같아요…": # 저녁 이벤트 패스
                    Soohyun "그런가요? 아쉽지만 어쩔 수 없죠."

                    Siwoon "맞아요..! 오늘은 안되지만 다음에 되는 날이 있겠죠, 그 때는 꼭 같이 먹어요!"

                    Juhan "…다음에 먹어요."

                    narrator_2 "그 후 애들은 각자 나머지 연습을 마치고 나서, 숙소로 돌아갔다."

                    narrator_2 "나도 애들을 데려다 주고 나서, 내 숙소로 돌아갔다."

                    jump S9

        "일찍 들어가서 쉴까요?":
            Soohyun "음… 그럴까요? 다들 피곤할텐데."

            Siwoon "그래도 돼요? 오랜만에 자유시간…!"

            Sehyuk "그렇게 기뻐할 일이야?"

            Siwoon "그렇지만.. 요즘 잘 못 쉬었단 말이에요."

            Sehyuk "연습은 안 할 거야?"

            Siwoon "알았어요.. 연습할게요.."

            Sehyuk "..아, 그런데 시운아. 그거 알아?"

            Siwoon "뭐를요..?"

            narrator_2 "세혁이가 한껏 목소리를 낮추었다. 무슨 얘기를 하려고 저러지...?"

            Sehyuk "연습실 있잖아. 밤늦게 연습하고 있으면 귀신 나온다던데?"

            Siwoon "…귀신…이 어딨어요…! 절 너무 바보로 아시는 거 아니에요?"

            Sehyuk "왜? 진짜 있을 수도 있지. 진짜 봤다는 사람도 있던데?"

            Siwoon "거짓말하지 마세요, 전 그런 말 못 들어봤단 말이에요…!"

            Soohyun " …형, 너무 그러지 마세요."

            Sehyuk "알았어, 알았어. 장난이야~"

            Siwoon "미안하시면 맛있는 거 사주세요."

            Sehyuk "맛있는 거? 뭐 먹고 싶은데?"

            Siwoon "진짜 사주시게요..? 정말..?"

            Sehyuk "왜, 싫어?"

            Siwoon "아뇨, 아뇨! 안 싫어요…!"

            Sehyuk "그럼 됐네. 스테이크 괜찮지?"

            Siwoon "스테이크.. 맛있겠다, 좋아요…! 그럼 둘이 가는 거예요?"

            Sehyuk "어. 둘도 낄래?"

            Soohyun "아, 저는 팀장님 찾아뵈야 할 것 같아서… 괜찮아요."

            Juhan "…저도 볼 일이 있어서, 죄송해요."

            Sehyuk "죄송할 것까지야. 무슨 볼일인데 그래?"

            Juhan "아… 그게… 매니저님께 드릴 말씀이 있어서요."

            na "네? 저요?"

            narrator_2 "엥? 갑자기 나...? 주한이가 내게 할만한 말이 있나?"

            Juhan "그, 네. 개인적으로 드릴 말씀이 있어서… 이따 시간 괜찮으세요?"

            na "네, 저는 언제든지 괜찮아요."

            Sehyuk "아, 그래요? 그러면 뭐 둘이 잘 얘기해요."

            Sehyuk "주한이 잘 챙겨줘요, 매니저님?"

            Siwoon "우리 주한이도 다 컸는데 알아서 하겠죠~"

            Juhan "…형들.."

            na "푸핫, 물론이죠! 걱정하지 마세요. 주한씨는 제가 잘 챙길게요."

            na "그보다 오늘 연습 끝나고 따로 제가 해야할 일이 있을까요?"

            Sehyuk "주한이만 얘기 끝내고 숙소로 데려다 주시면 될 거 같아요. 저희는 다 따로 갈 것 같아서."

            Sehyuk "수현이도 따로 갈거지?"

            Soohyun "네. 아.. 형 혹시 술 마실 거예요"

            Sehyuk "아니, 운전해야해서 안 마실 거야."

            Soohyun "아.. 네. 혹시라도 술 먹으면 매니저님 불러주세요. 내일 스케줄도 있고… 너무 늦게 들어오면 피곤하니까-"

            Sehyuk "나참. 날 뭐로 보는 거야?"

            Sehyuk "술도 안 마시고 일찍 들어갈테니 걱정은 넣어둬, 리더님~"

            narrator_2 "세혁이가 피식 웃으면서 수현의 어깨를 툭툭 두드렸다."

            Soohyun "…네. 알겠어요. 그럼 주한이 잘 부탁드려요, 매니저님."

            na "네, 걱정마세요. 주한씨, 이야기는 연습 끝나고 할까요?"

            Juhan "…네. 그렇게 해요."

            Sehyuk "그럼 얘기는 대충 끝났지? 이제 들어가서 연습하자."

            narrator_2 "세혁이가 애들의 등을 떠밀었다. 애들은 다같이 연습실로 돌아갔다."

            Soohyun "나중에 뵐게요, 매니저님."

            jump S7_2

    # S5

    narrator_2 "애들이 연습 하는 동안 뒤에 앉아서 저녁을 먹을만한 식당을 찾아보았다."
    
    narrator_2 "와, 이 근처에 맛집이 되게 많네...어딜 가는게 좋을까?"

    # 음식점 이미지

    narrator_2 "아.. 어디를 가지? 정말 고민이네... 애들한테 물어볼까?"

    menu:
        "물어본다":
            Sehyuk "미안한데 연습하느라 바빠서요. 알아서 적당히 골라줄래요?"

            na "미안해요.."

            narrator_2 "그냥 내가 골라야겠다.."

        "물어보지 않는다":
            narrator_2 "아냐, 애들 연습중인데 괜히 방해하지 말고 내가 알아서 하자..."

    narrator_2 "어디로 갈까?"

    menu:
        "닭볶음탕집":
            narrator_2 "좋아, 닭볶음탕집으로 가자."
            $ select == 0

        "꽃게탕집":
            narrator_2 "좋아, 꽃게탕집으로 가자."
            $ select == 1

        "레스토랑":
            narrator_2 "좋아, 레스토랑으로 가자."
            $ select == 2


    narrator_2 "음식점을 다 고르자, 도희 팀장님 한테서 전화가 걸려왔다."

    menu:
        "전화를 받는다":
            Sehyuk "전화 벨소리 누구야?"

            Siwoon "매니저님 같은데요? 매니저님, 전화 여기서 받으시려고요?"

            na "아, 죄송합니다. 나가서 받겠습니다."

            Juhan "…괜찮아요. 다녀오세요."

            $ n = 0 # 전화를 받는다

        "밖으로 나간다":
            na "저 죄송한데, 전화 좀 받고 오겠습니다."

            Soohyun "아, 네. 도희 팀장님 전화죠? 천천히 다녀 오세요."

            na "네, 고마워요."

            $ n = 1 # 밖으로 나간다

    # S6

    narrator_2 "나는 복도로 나와 전화를 받았다."

    if callormessage == 0: #전화
        Dohee_call "여보세요? [player_name]씨 부재중 찍혀있던데. 뭐 때문에 전화 했어?"

        na "앗, 드릴 말씀이 있어서요."

        Dohee_call "그래? 그럼 그건 이따 하고, 내 말부터 들어봐."

    elif callormessage == 1: #문자
        Dohee_call "여보세요? 어, [player_name]씨. 문자보고 전화했어. 통화 괜찮아?"

        na "아, 네 괜찮아요!"

    Dohee_call "박 피디님이랑 방금 연락했거든. 주한이가 가사 쓰면 작사가 쪽에서 한 번 컨펌 해야할거 같다고하던데. 내일 저녁까지 회의실로 가져와달라고 그러시더라."

    Dohee_call "[player_name]씨가 주한이한테 전달해줄래?"

    Dohee_call "그리고 회의 날짜는 컨펌까지 생각해서 3일 뒤로 잡아 뒀어. 이것도 전달하고."
    
    na "아 네! 주한씨에게 제가 이따 물어보겠습니다. 다음 회의 날짜도 멤버들에게 전달하도록 하겠습니다."

    Dohee_call "그래, [player_name]씨 특별히 더 전달할 사항은 없고?"

    menu:
        "허락부터 받는다":
            na "아, 네. 저, 아까 멤버들이랑 이야기하다가 오늘 스케줄 일찍 끝난 김에 같이 저녁 한번 먹자고 말이 나왔었어요. 혹시 괜찮을까요?"

            Dohee_call "음? 저녁? 흐음... "

            Dohee_call "그래, 뭐. 새로운 매니저 환영회도 할 겸 괜찮겠네. 대신, 어디 가는지 나한테 말하고 가. 어지간하면 사람 많은 데는 피하고."

            na "아, 네. 감사합니다! 그럼 혹시 팀장님도 같이 와주실 수 있나요?"

            Dohee_call "그럼 나 빼놓고 먹으려 했어? 신입 왔으니까 챙겨줘야지."

            Dohee_call "난 알아서 갈테니까 식당 위치 찍어서 보내놔."

            na "와, 정말 감사합니다! 이따 6시 반에 식당 앞에서 뵐게요."

            Dohee_call "응 그래, 이따 봐."
            
        "간결하게 본론부터 말한다":
            na "오늘 저녁에 멤버들이랑 밥먹기로 했는데 팀장님도 오실래요?"

            Dohee_call "그런 일정을 잡았어? 바로바로 말 하라고 했던 것 같은데."

            Dohee_call "멤버들이랑 약속도 일정이니까 나한테 바로 말 해줘, 알았지."

            na "죄송합니다..."

            Dohee_call "죄송할거 있나, 다음에 안 그러면 되지."

            na "네, 조심하겠습니다."

            Dohee_call "응, 그래서 저녁먹기로 했다고?"

            na "아, 네. 멤버분들과 친해질 겸 같이 밥 먹으면 괜찮을 거 같아서요."

            Dohee_call "[player_name]씨 환영회도 같이 하면 되겠네. 알았어 다녀와."

            na "으아..감사합니다! 저기, 그럼 혹시 팀장님도 오실 수 있나요?"

            Dohee_call "나? 그거 수현 씨가 물어보라고 시킨 거지?"

            na "네? 어떻게 아셨어요?"

            Dohee_call "뻔하지. 알았어, 이따 갈테니까 위치만 보내놔."

            na "아, 네! 감사합니다. 이따 6시 반에 식당 앞에서 뵐게요."

            Dohee_call "응, 이따가 봐."
    
    narrator_2 "나는 통화를 마치고 다시 연습실 안으로 들어갔다. 문이 열리자 멤버들이 나를 돌아봤다."

    Sehyuk "시운아, 왜 눈이 딴 데로 가지?"

    Siwoon "아, 집.. 집중할게요. 죄송해요"

    Juhan " …죄송합니다."

    if n == 0: # 전화를 받는다.
        Soohyun "매니저님 오셨어요? 혹시 팀장님이랑 통화하신 거예요?"

        na "아, 네네!"

        Siwoon "팀장님 뭐라고 하셨어요? 와주신대요?"

    elif n == 1: # 밖으로 나간다.
        Soohyun "통화 잘 마치고 오셨어요? 팀장님께서는 뭐라고 하셨어요?"

        menu:
            "질문에 대한 답부터 한다.":
                na "팀장님도 오신다고 하셨어요."

                Siwoon "정말요? 잘됐다!"

                Soohyun "잘 됐네요."

                na "그리고, 아까 회의 일에 대해 전달사항이 있어요. 이건 이따 연습 끝나고 알려 드릴게요."

                Juhan "..네. 감사합니다, 매니저님."

            "전달 사항부터 얘기한다.":
                na "그보다, 먼저 아까 회의 일에 대해서 전달할 게 있는데요."

                Siwoon "회의요? 뭔데요?"

                na "네. 주한씨한테 말씀 드릴 부분인데..."

                Sehyuk "그럼 이따 주한이한테만 따로 알려줘요. 지금 연습 시간이니까"

                na "아, 네! 미안해요. 그, 그럼 연습 열심히 하세요.."


    # S7_1
    # 이벤트 자체를 패스하거나(S9로 건너뜀),
    # 주한이랑만 이벤트 할 경우(S7_2로 건너뜀)
    # 가 아니면 일반적으로 모두와 식사를 하는 경우로 옴(S7_1로 쭉 진행)

    narrator_2 "두 시간 뒤."

    narrator_2 "연습이 끝나고 멤버들이 옷을 갈아 입으러 숙소에 잠깐 들렸다. 나는 건물 밑에다가 밴을 세워두고 그 안에서 기다리고 있었다."

    narrator_2 "오래 기다리지 않아 주한이가 제일 먼저 나왔다."

    Juhan " …매니저님, 많이 기다리셨죠. 죄송해요. 형들도 금방 내려올 거예요."

    na "에이, 아니에요. 저도 스케줄 정리하고 있었는걸요."

    Juhan "아… 네."

    Juhan "그… 오늘 스케줄이 더 있나요?"

    na "그런건 아니고, 내일 스케줄 보고 있었어요."

    na "...아! 그보다 아까 팀장님이 주한씨한테 전달하라고 하신 말이 있는데요."

    Juhan "그래요? 뭔가요?"

    menu:
        "가사 언제까지 쓸 수 있을 거 같아요?":
            Juhan "음… 하루 정도면 충분할 것 같아요. 많이 급한가요? "

            na "다음 회의 전에 주한씨가 쓴 가사를 작사가님이 한 번 확인을 해봐야 할거 같다고 하시더라고요."

            Juhan "아… 그렇겠네요."

            Juhan "…그럼 내일 저녁까지 써서 드리면 괜찮을까요?"

            na "네, 충분해요. 작사가님도 내일 저녁까지 달라고 하셨거든요."

            na "주한씨가 저한테 먼저 보내주시면, 제가 작사가님께 전달하도록 할게요."

            Juhan "아, 네. 그럼 제가 내일 저녁까지 매니저 님께 보내드릴게요. 번거롭게 만들어서 죄송합니다."

            na "아니에요, 제가 해야하는 일인걸요."

            Juhan "…그래도 죄송합니다."

            Juhan "..."

            Juhan "아… 저기 형들 오네요."
            
            
        "내일까지 가사 다 쓸 수 있으세요?":
            Juhan "아... 네. 할 수 있을 것 같아요."

            na "네, 부탁드려요. 혹시라도 다 못 쓸 것 같으면 저한테 알려주세요. 일정 다시 조정해 달라고 말씀드려 볼게요."

            Juhan "아니에요. 내일까지면 충분히 할 수 있을 것 같아요."

            na "힘들면 말해줘요, 제가 도울 수 있는 일이라면 얼마든 도와드릴테니까요."

            Juhan "..네. 신경써주셔서 감사합니다."

            Juhan "아, 형들 내려오네요."





        




    return


label S9:

    return

label S7_2:

    return


            


    












"""
    #$ renpy.quit(relaunch=False, status=0, save = False)
    #강제종료시키기(저장 없이)

    #call screen Force_quit #버튼 누르면 강제종료

    Ruru "다음은 트랜지션 효과 테스팅"

    scene intro1 with fade
    narrator_2 "fade"

    scene intro2 with dissolve
    narrator_2 "dissolve"

    scene intro3 with pixellate
    narrator_2 "pixellate"

    show scg_Ruru


    show scg_Ruru at right with move
    narrator_2 "move"

    show scg_Juhan with moveinright
    narrator_2 "moveinright"

    hide scg_Juhan with moveoutleft
    narrator_2 "moveoutleft"

    show scg_Ruru at left with ease
    narrator_2 "ease"

    narrator_2 "ease는 move와 비슷하지만, 트랜지션 시작 시에는 천천히 동작했다가 점점 빨라지며 트랜지션 종료시에 다시 속도가 줄어드는 트랜지션."

    #show scg_Ruru at center with move
    hide scg_Ruru

    show scg_Ruru at center with zoomin
    narrator_2 "zoomin"

    hide scg_Ruru with zoomout
    narrator_2 "zoomout"

    # scg_Ruru at center with zoominout
    #narrator_2 "zoominout"

    show scg_Juhan at center

    with vpunch
    narrator_2 "vpunch, 화면을 0.25초간 세로로 흔든다"

    with hpunch
    narrator_2 "hpunch, 화면을 0.25초간 가로로 흔든다"

    Juhan "다음은 눈 깜빡임 효과 테스팅"

    
    scene intro3 with fadehold
    scene intro3 with fadehold

    narrator_2 "이정도면 충분해? 아무튼 연출은 돼."

    return
"""
