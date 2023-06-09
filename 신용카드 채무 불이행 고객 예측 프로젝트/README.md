## 신용카드 채무 불이행 고객 예측 프로젝트

기간 : 2023.03.13 ~ 2023.03.15
팀원 : 이진서, 윤혜림, 김종현

- 문제 : 신용카드 대금 채무 불이행으로 인한 손실
- 해결 방안 :
    - 고객 프로필 정보 확인 및 파생변수 생성 및 검증
    - 고객 프로필 정보 (나이, 결혼 여부 등), 이용한도에 따른 채무 불이행률 탐색
    - ML알고리즘 활용 (XGBoost, LightGBM)활용하여 채무 불이행 고객 예측
    
### [데이터로 생성할 수 있는 파생변수 생각해보기]

- **신용카드 채무 불이행하는 고객을 예측할 때 만들 수 있는 파생변수**
    - **고객의 총 신용 한도 대비 청구금액 비율**
        - 신용 한도 대비 청구금액 비율은 고객이 자신의 신용 한도를 얼마나 근접하여 사용하고 있는지를 나타낼 수 있음. 신용한도에 근접하여 사용할수록 연체할 확률이 높다고 판단.
    - **고객의 지난 달 대비 이번 달 청구금액 증감률**
        - 지난 달 대비 이번 달 청구금액 증감률은 고객의 지출 패턴을 파악할 수 있다. 예를 들어, 이전 달보다 급격한 증가가 있을 경우 급한 상황에서 대출을 받아서 지불한 경우일 가능성이 있음. 이러한 경우 채무 불이행 가능성이 높아짐.
    - **결제 지연 기간(PAY_0 ~ PAY_6)의 평균**
        - 결제 지연 기간은 신용도를 나타내는 지표. 결제 지연이 길어질수록 채무 불이행 가능성이 높아짐.
    - **고객의 연령대**
        - 고객의 연령대는 연령대에 따라 채무 불이행 가능성이 달라질 수 있다.
    - **고객의 결혼 여부**
        - 마지막으로 결혼 여부도 채무 불이행 가능성에 영향을 미칠 수 있음. 결혼한 고객은 가족의 지출까지 고려해야 하기 때문에 채무 불이행 가능성이 높아질 수 있다.
- **세울 수 있는 가설**
    1. 신용한도 내에 청구되는 금액이 많은 고객일수록 채무 불이행할 확률이 높을까?
    2. 청구금액의 증감율이 크다. -> 급격한 소비는 default할 가능성이 높다?
    3. 결제지연 기간이 길어지면 길어질 수록 연체할 확률이 높을 수 있다는 가정
    4. 고객의 연령이 낮을 수록 채무를 불이행할 확률이 높다는 가정
