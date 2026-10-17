# 3단계. Internet Gateway 연결하기

[← 단계 목록](../guide.md) · [이전: 2단계](./02-vpc-subnet.md) · [다음: 4단계 →](./04-route-table.md)

> **한 줄 요약**: VPC에 인터넷과 연결되는 정문(Internet Gateway)을 단다.

## 1. 무엇을, 왜

| 항목 | 내용 |
|---|---|
| 무엇을 | Internet Gateway `b3-1-igw`를 만들어 `b3-1-vpc`에 연결 |
| 왜 | IGW가 없으면 퍼블릭 IP가 있어도 VPC가 인터넷과 연결되지 않음. 퍼블릭 ↔ 프라이빗 주소 변환도 IGW가 함 |
| 어디서 | 🖱️ AWS 콘솔 → **VPC** 서비스 → 인터넷 게이트웨이 |

## 2. 할 일

1. **인터넷 게이트웨이 생성** → 이름 `b3-1-igw`, 태그 `Project=b3-1`
2. **작업** → **VPC에 연결** → `b3-1-vpc`
3. [cleanup-checklist.md](../cleanup-checklist.md)에 IGW ID 기록

## 3. 확인과 📸

| 확인할 것 | 📸 |
|---|---|
| 상태 `Attached`, VPC ID가 `b3-1-vpc`의 ID와 같음 | `03-igw-attached.png` |

## 4. ✍️ 실제 기록

**상태**: ⬜ 진행 전

| 항목 | 내용 |
|---|---|
| 한 날짜 | |
| 결과 | |
| 막힌 점 | |
| 내 말로 한 줄 | |

---

[← 단계 목록](../guide.md) · [이전: 2단계](./02-vpc-subnet.md) · [다음: 4단계 →](./04-route-table.md)
