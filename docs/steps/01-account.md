# 1단계. 계정 준비

[← 단계 목록](../guide.md) · [다음: 2단계 →](./02-vpc-subnet.md)

> **한 줄 요약**: 실습을 시작하기 전에 계정을 안전하게 만들고, 실수로 돈이 나가는 것을 막고, 실습에 쓸 최소 권한 사용자를 만든다.

## 1. 무엇을, 왜

| 작업 | 하는 일 | 왜 필요한가 |
|---|---|---|
| ① 리전 서울 | 앞으로 만드는 리소스가 모두 서울 데이터센터에 생김 | 과제 제약이 "모든 리소스는 서울 리전". 리전이 섞이면 정리할 때 놓쳐서 과금됨 |
| ② MFA | 로그인할 때 비밀번호에 더해 휴대폰 앱의 6자리 코드를 요구 | 루트는 모든 권한을 가진 계정이라 비밀번호만 유출돼도 계정 전체를 잃음 |
| ③ 제로 지출 예산 | 1센트라도 비용이 생기면 이메일로 알림 | 프리 티어를 넘거나 정리를 잊은 리소스를 바로 알아챔 |
| ④ IAM 정책 | 실습에 필요한 EC2 작업만 허용하는 권한 묶음 | 과제 요구: 최소 권한, 관리자 권한 금지 |
| ⑤ IAM 사용자 | 위 정책만 가진 실습 전용 로그인 | 과제 제약: 루트 대신 IAM 사용자로 작업 |

**어디서**: 🖱️ AWS 콘솔, **루트 계정**으로 로그인한 상태 (루트로 하는 작업은 이번이 마지막)

## 2. 할 일

#### ① 리전 바꾸기

오른쪽 위 리전 이름 클릭 → **아시아 태평양(서울) ap-northeast-2**

#### ② MFA 등록

1. 오른쪽 위 계정 이름 → **보안 자격 증명** → **MFA 디바이스 할당**
2. 디바이스 이름 입력 → **인증 관리자 앱** 선택 → Next
3. 휴대폰 인증 앱으로 QR 스캔 → 연속된 코드 2개 입력 → **MFA 추가**

> 창을 새로고침하면 QR이 새로 바뀝니다. 그때는 앱의 예전 항목을 지우고 새 QR을 다시 스캔합니다.

#### ③ 제로 지출 예산

검색창 `Budgets` → **예산 생성** → **템플릿 사용(단순화)** → **제로 지출 예산** → 이메일 입력 → 생성

#### ④ IAM 정책 만들기

1. 검색창 `IAM` → 왼쪽 **정책** → **정책 생성** → **JSON** 탭
2. 기존 내용을 지우고 아래 내용을 붙여넣기 (코드 블록 오른쪽 위 복사 버튼 사용) → **다음**
3. 이름 `b3-1-policy` → **정책 생성**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "B31ReadOnlyAllRegions",
      "Effect": "Allow",
      "Action": ["ec2:Describe*", "ec2:Get*"],
      "Resource": "*"
    },
    {
      "Sid": "B31Ec2VpcSeoulOnly",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateVpc", "ec2:DeleteVpc", "ec2:ModifyVpcAttribute",
        "ec2:CreateSubnet", "ec2:DeleteSubnet", "ec2:ModifySubnetAttribute",
        "ec2:CreateInternetGateway", "ec2:AttachInternetGateway",
        "ec2:DetachInternetGateway", "ec2:DeleteInternetGateway",
        "ec2:CreateRouteTable", "ec2:DeleteRouteTable",
        "ec2:CreateRoute", "ec2:DeleteRoute",
        "ec2:AssociateRouteTable", "ec2:DisassociateRouteTable",
        "ec2:CreateSecurityGroup", "ec2:DeleteSecurityGroup",
        "ec2:AuthorizeSecurityGroupIngress", "ec2:RevokeSecurityGroupIngress",
        "ec2:CreateKeyPair", "ec2:DeleteKeyPair",
        "ec2:RunInstances", "ec2:TerminateInstances",
        "ec2:StartInstances", "ec2:StopInstances",
        "ec2:ModifyInstanceCreditSpecification",
        "ec2:CreateTags", "ec2:DeleteVolume"
      ],
      "Resource": "*",
      "Condition": { "StringEquals": { "aws:RequestedRegion": "ap-northeast-2" } }
    }
  ]
}
```

| 정책 부분 | 허용 범위 | 이유 |
|---|---|---|
| 조회 (`Describe*`, `Get*`) | 모든 리전 | 콘솔 화면 표시, 정리 때 다른 리전까지 확인 |
| 만들기·지우기·연결 | **서울 리전만** | 실습에 필요한 작업만, 다른 리전에 실수로 만드는 것도 막음 |
| S3, RDS, IAM 등 다른 서비스, 관리자 권한 | **없음** | 과제 요구: EC2/VPC/SG 범위로 제한 |

#### ⑤ IAM 사용자 만들기

1. 왼쪽 **사용자** → **사용자 생성** → 이름 `b3-1-user`
2. **AWS Management Console에 대한 사용자 액세스 권한 제공** 체크 → **IAM에서 사용자 생성**
3. **사용자 지정 암호** 입력, **"다음 로그인 시 새 암호 생성" 체크 해제** → 다음
4. **직접 정책 연결** → `b3-1-policy` 체크 → 다음
5. 태그 `Project` = `b3-1` → **사용자 생성**
6. 완료 화면의 **콘솔 로그인 URL**을 메모 (`.csv` 파일은 레포에 넣지 않음)

#### ⑥ 📸 01 찍기

아래 3장 참고. **루트로 로그인한 상태에서** 찍습니다.

#### ⑦ 갈아타기

로그아웃 → 메모한 URL로 `b3-1-user` 로그인 → 리전이 서울인지 확인

## 3. 확인과 📸

| 확인할 것 | 📸 |
|---|---|
| 오른쪽 위 리전이 "아시아 태평양(서울)" | `00a-region-seoul.png` |
| MFA 유형으로 인증 관리자 앱 선택 | `00b-mfa-device-type.png` |
| QR 스캔 후 코드 2개 입력 (QR은 가림) | `00c-mfa-setup.png` |
| `b3-1-user`의 **권한** 탭에 `b3-1-policy` **하나만** 연결됨 | `01-iam-user-policy.png` |

> 01은 **루트로 로그인한 지금** 찍어야 합니다. `b3-1-user`에게는 IAM 화면을 볼 권한이 없습니다.

## 4. ✍️ 실제 기록

**상태**: 🟡 진행 중 (①~⑥ 완료, ⑦ 로그인 전환 남음) · **날짜**: 2026-10-18

### 4-1. 한 일 한눈에 보기

| 작업 | 실제로 한 일 | 이것이 하는 일 | 확인한 결과 | 📸 |
|---|---|---|---|---|
| ① 리전 | 콘솔 리전을 **서울**로 선택 | 앞으로 만드는 리소스가 생길 위치를 고정 | 오른쪽 위 "아시아 태평양(서울)" | 00a |
| ② MFA | 루트 계정에 인증 앱 등록 (`codyssey_project`) | 로그인할 때 비밀번호 + 휴대폰 6자리 코드를 요구 | 등록 완료 | 00b, 00c |
| ③ 결제 알림 | **제로 지출 예산** 생성 | 1센트라도 비용이 생기면 이메일로 알림 | 생성 완료 | — |
| ④ IAM 정책 | `b3-1-policy` 생성 | "무엇을 할 수 있는지" 적은 **권한 목록**. EC2 작업만, 만들기·지우기는 서울만 | JSON 검사 보안·오류·경고 0, 요약에 서비스는 **EC2 하나** | 00d, 00e, 00f, 00m |
| ⑤ IAM 사용자 | `b3-1-user` 생성, 정책 직접 연결 | 위 권한만 들고 로그인하는 **실습 전용 계정** | 콘솔 접근 O, 암호 재설정 필요 "아니요", 태그 없음 | 00g~00l |
| ⑥ 증빙 | 사용자 **권한 탭** 확인 | 사용자에게 정책이 하나만 붙었는지 확인 | `b3-1-policy` 하나 (고객 관리형, 직접), AdministratorAccess 없음 | **01** |
| ⑦ 전환 | 로그아웃 후 `b3-1-user`로 로그인 | 이후 작업을 루트가 아닌 최소 권한 사용자로 함 | 스크린샷 생략. 2단계부터 모든 사진의 오른쪽 위 사용자 이름(`b3-1-user`)이 증빙 | — |

### 4-2. 1단계로 갖춰진 것

- **계정 보호**: 루트는 MFA 없이는 로그인할 수 없음
- **과금 감시**: 비용이 생기면 바로 알림이 옴
- **최소 권한 작업 환경**: 앞으로의 작업은 EC2 권한만 가진 `b3-1-user`로 함. S3, RDS, IAM, 관리자 권한은 없음

→ 과제 요구 **"루트 계정 사용 금지, IAM 최소 권한, AdministratorAccess 금지, 프리 티어 범위"**의 준비가 끝남

> **왜 정책에 EC2 하나만 보이나?** AWS에서 VPC, Subnet, Internet Gateway, Route Table, Security Group, 키 페어는 모두 **EC2 서비스의 API**(`ec2:CreateVpc`, `ec2:CreateSubnet` …)로 만듭니다. 그래서 이 과제에 필요한 권한이 EC2 한 줄로 묶여 보이고, 다른 서비스는 하나도 없습니다. 이것이 최소 권한의 근거입니다.

### 4-3. 막힌 점과 해결

| 항목 | 내용 |
|---|---|
| 증상 | MFA 등록 때 `Authentication code for device is not valid` |
| 원인 | 페이지를 새로고침해 QR(비밀키)이 새로 바뀌었는데, 앱에는 이전 QR로 만든 항목이 남아 있어 그 코드를 입력함 |
| 해결 | 앱의 기존 AWS 항목을 지우고 새 QR을 다시 스캔 → 연속된 코드 2개 입력 |
| 배운 점 | MFA 화면을 새로 열 때마다 QR을 다시 스캔해야 함 |

### 4-4. 내 말로 한 줄

(작성 예정)

### 4-5. 스크린샷

> 계정 ID, 로그인 URL, ARN은 가렸습니다. 2단계부터는 **12자리 계정 ID만** 가리고, 로그인한 사용자 이름은 보이게 둡니다.

**① 리전을 서울로 선택**

![리전 서울](../images/00a-region-seoul.png)

**② MFA 유형: 인증 관리자 앱**

![MFA 유형](../images/00b-mfa-device-type.png)

**② QR 스캔 후 연속 코드 2개 입력** (QR은 비밀키라 가림)

![MFA 설정](../images/00c-mfa-setup.png)

**④ IAM → 정책 → 정책 생성**

![정책 생성](../images/00d-iam-policy-create.png)

**④ JSON 탭에 정책 붙여넣기** (보안·오류·경고 0)

![정책 JSON](../images/00e-iam-policy-json.png)

**④ 검토**: 이름 `b3-1-policy`, 허용 서비스 EC2 하나, 조건은 서울 리전

![정책 검토](../images/00f-iam-policy-review.png)

**④ 생성된 정책 요약**: EC2 하나, `aws:RequestedRegion = ap-northeast-2`

![정책 요약](../images/00m-iam-policy-summary.png)

**⑤ IAM 사용자 목록** (처음 0명) → 사용자 생성

![IAM 사용자 목록](../images/00g-iam-users-list.png)

**⑤ 사용자 세부 정보**: 이름, 콘솔 접근, 사용자 지정 암호, 재설정 체크 해제

![사용자 세부 정보](../images/00h-iam-user-details.png)

**⑤ 권한 설정**: 직접 정책 연결 → `b3-1-policy`만 선택

![권한 설정](../images/00i-iam-user-permissions.png)

**⑤ 검토**: 암호 재설정 필요 "아니요", 권한은 `b3-1-policy` 하나

![검토 및 생성](../images/00j-iam-user-review.png)

**⑤ 생성 완료** (콘솔 로그인 URL은 계정 ID가 들어 있어 가림)

![생성 완료](../images/00k-iam-user-created.png)

**⑤ 사용자 목록에 `b3-1-user` 1명**

![사용자 목록](../images/00l-iam-user-created-list.png)

**⑥ 📸 01: `b3-1-user` 권한 탭** (정책은 `b3-1-policy` 하나, AdministratorAccess 없음)

![사용자 권한](../images/01-iam-user-policy.png)

---

[← 단계 목록](../guide.md) · [다음: 2단계 →](./02-vpc-subnet.md)
