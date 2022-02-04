from random import *

# 일반 유닛

class Unit:
    def __init__(self, name, hp, speed):
        self.name = name
        self.hp = hp
        self.speed = speed
        print("{0} 유닛이 생성되었습니다.".format(name))

    def move(self, location):
        #print("[지상 유닛 이동]")
        print("{0} : {1} 방향으로 이동합니다. [속도 {2}]".format(self.name, location,
                                                      self.speed))

    def damaged(self, damage):
        print("{0} : {1} 데미지를 입었습니다.".format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1} 입니다.".format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴되었습니다.".format(self.name))


# 공격 유닛
class AttackUnit(Unit):
    def __init__(self, name, hp, speed, damage):
        Unit.__init__(self, name, hp, speed)
        self.damage = damage

    def attack(self, location):
        print("{0} : {1} 방향으로 적군을 공격 합니다. [공격력 {2}]"\
        .format(self.name, location, self.damage))  #self.name 이라고 한거는 Class 내에 있는 내가 가지고 있는 변수를 가져오겠다.


# 마린:
class Marine(AttackUnit):
    def __init__(self):  #self라고만 입력한 이유는 추가로 받을 변수가 없고, 상속해서 받을 변수가 전부여서
        AttackUnit.__init__(self, "마린", 40, 1, 5)  # 이부분은 초기화라고 한다.

        # 스팀팩 : 일정 시간 동안 이동 및 공격 속도를 증가, 체력 10 감소
    def stimpack(self):
        if self.hp > 10:
            self.hp -= 10
            print("{0} : 스팀팩을 사용합니다. (HP 10 감소)".format(self.name))
        else:
            print("{0} : 체력이 부족하여 스팀팩을 사용하지 않습니다.".format(self.name))


# 탱크
class Tank(AttackUnit):
    # 시즈모드 : 탱크를 지상에 고정시켜, 더 높은 파워로 공격 가능. 이동 불가
    seize_developed = False  # 시즈모드 개발여부

    def __init__(self):
        AttackUnit.__init__(self, "탱크", 150, 1, 35)
        self.seize_mode = False

    def set_seize_mode(self):
        if Tank.seize_developed == False:
            return
        # 현재 시즈모드가 아닐 때 -> 시즈모드
        if self.seize_mode == False:
            print("{0} : 시즈모드로 전환합니다.".format(self.name))
            self.damage *= 2
            self.seize_mode = True
        # 현재 시즈모드일 때 -> 시즈모드 해제
        else:
            print("{0} : 시즈모드를 해제합니다.".format(self.name))
            self.damage /= 2
            self.seize_mode = False


# 드랍쉽 : 공중 유닛, 운송 공격력 없음


# 비행 기능을 가진 클래스
class Flyable:
    def __init__(self, flying_speed):
        self.flying_speed = flying_speed

    def fly(self, name, location):

        print("{0} : {1} 방향으로 날아갑니다. [속도 {2}]".format(name, location,
                                                      self.flying_speed))


# 공중 공격 유닛 클래스
class FlyableAttackUnit(AttackUnit, Flyable):  #다중 상속
    def __init__(self, name, hp, damage, flying_speed):
        AttackUnit.__init__(self, name, hp, 0, damage)  # 지상 speed 0
        Flyable.__init__(self, flying_speed)

    def move(self, location
             ):  # move 함수를 재정의 함으로써 비행 유닛을 따로 호출하지 않고, 동일하고 move함수로 부를 수 있게 함
        #print("[공중 유닛 이동]")
        self.fly(self.name, location)


# 레이스
class Wraith(FlyableAttackUnit):
    def __init__(self):
        FlyableAttackUnit.__init__(self, "레이스", 80, 20, 5)
        self.clocked = False  # 클로킹 모드 (해체 상태)

    def clocking(self):
        if self.clocked == True:  # 모드 해체
            print("{0} : 클로킹 모드 해체합니다.".format(self.name))
            self.clocekd = False
        else:
            print("{0} : 클로킹 모드 설정합니다.".format(self.name))
            self.clocekd = True


def game_start():
    print("[알람] 새로운 게임을 시작합니다.")


def game_over():
    print("Player : GG")
    print("[Player] 님이 퇴장하였습니다.")


# 실제 게임 진행

game_start()

# 마린 3명 생성
m1 = Marine()
m2 = Marine()
m3 = Marine()
# 탱크 2개 생성
t1 = Tank()
t2 = Tank()
# 레이스 1개 생성
w1 = Wraith()

#유닛 일괄 관리
attack_units = []
attack_units.append(m1)
attack_units.append(m2)
attack_units.append(m3)
attack_units.append(t1)
attack_units.append(t2)
attack_units.append(w1)

#전군 이동
for unit in attack_units:
  unit.move("1시")

# 탱크 시즈모드 개발 
Tank.seize_developed =True
print("[알람] 탱크 시즈 모드 개발이 완료되었습니다.")

# 공격 모드 준비 (마린 : 스팀팩, 탱크 : 시즈모드, 레이스 : 클로킹)
for unit in attack_units:
  if isinstance(unit, Marine): # isinstance : unit이라는 객체가 Marine이라는 class의 instance 즉 객체이냐? 
    unit.stimpack()
  elif isinstance(unit, Tank):
    unit.set_seize_mode()
  elif isinstance(unit, Wraith):
    unit.clocking()

# 전군 공격
for unit in attack_units:
  unit.attack("1시")

# 아군 피해
for unit in attack_units:
  unit.damaged(randint(5, 100)) # 랜덤으로 공격을 받음

# 게임 종료
game_over()
