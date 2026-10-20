# 리소스 정리 체크리스트

## 1. 생성 리소스 기록 (만들 때마다 바로 한 줄 추가)

| # | 리소스 | 이름 | ID | 생성일 | 삭제 확인 |
|---|---|---|---|---|---|
| 1 | VPC | `b3-1-vpc` | `vpc-07f1142c4fd787dde` | 2026-10-18 | [ ] |
| 2 | Subnet | `b3-1-subnet-public` | `subnet-0d9ef94b777f72943` | 2026-10-20 | [x] 삭제 |
| 3 | Internet Gateway | `b3-1-igw` | `igw-0d57e59b8c617f4e0` | 2026-10-20 | [ ] |
| 4 | Route Table | `b3-1-rt-public` | `rtb-03c65969cf2c394ad` | 2026-10-20 | [x] 삭제 |
| 5 | Security Group | `b3-1-sg-web` | `sg-0b70263b7d5833f46` | 2026-10-20 | [x] 삭제 |
| 6 | Key Pair | `b3-1-key` | — | 2026-10-20 | [x] AWS·내 PC 모두 삭제 |
| 7 | EC2 | `b3-1-ec2-web` | `i-04f3b8c675688f133` | 2026-10-20 | [x] 종료됨 |
| 8 | EBS (루트 볼륨) | — | `vol-0fab396aa4c25564a` | 2026-10-20 | [x] 자동 삭제 |
| 9 | IAM 사용자 | `b3-1-user` | — | | (평가 후 정리) |

태그 `Project=b3-1`은 VPC, Subnet, IGW, Route Table, SG, Key Pair, EC2에 달았다. **EBS 루트 볼륨에는 달지 않았으므로** 정리할 때 위 볼륨 ID로 확인한다(EC2 종료 시 함께 삭제되도록 설정됨).

## 2. 정리 순서와 확인

안에 들어 있는 것부터 지워야 바깥 리소스가 삭제된다.

- [ ] **스크린샷 01~12가 `docs/images/`에 모두 있는지 먼저 확인** (삭제 후에는 다시 찍을 수 없음)
- [x] 1. **EC2** Terminate → 상태 `Terminated` 확인
  - Terminated 상태는 약 1시간만 보이므로 **바로** 스크린샷 13을 찍는다
- [x] 2. **EBS** 볼륨 목록에 `vol-0fab396aa4c25564a`가 없는지 확인 (미사용 볼륨 포함 0개)
- [x] 3. **Elastic IP** 목록이 비어 있는지 확인 → 할당하지 않음. 쓰지 않았어도 연결 안 된 EIP는 과금되므로 **직접 확인함** ("이 리전에서 탄력적 IP 주소를 찾을 수 없음", 📸 13c)
- [x] 4. **Key Pair** `b3-1-key` 삭제 (로컬 `.pem` 파일도 삭제, `known_hosts` 기록 제거)
- [x] 5. **Security Group** `b3-1-sg-web` 삭제
- [x] 6. **Subnet** 삭제
- [x] 7. **Route Table** `b3-1-rt-public` 삭제
- [ ] 8. **Internet Gateway** VPC에서 Detach → 삭제
- [ ] 9. **VPC** `b3-1-vpc` 삭제

## 3. 만들지 않은 과금 리소스 (해당 없음 확인)

- [ ] NAT Gateway: 만들지 않음, 목록 0개 확인
- [ ] ELB/ALB: 만들지 않음, 목록 0개 확인
- [ ] RDS: 만들지 않음, 목록 0개 확인
- [ ] EBS 스냅샷: 만들지 않음, 목록 0개 확인

## 4. 최종 확인

- [ ] EC2 Global View에서 모든 리전의 인스턴스·VPC 확인 (기본 VPC 제외)
- [ ] (권장) Billing Dashboard에서 과금 항목 확인

## 5. 최종 기록

| 항목 | 내용 |
|---|---|
| 정리 일시 | `2026-__-__ __:__` (KST) |
| 리전 | `ap-northeast-2` |
| 남은 과금 리소스 | 없음 / ____ |
| 증빙 | [13a-ec2-terminated.png](images/13a-ec2-terminated.png), [13b-ebs-volumes-empty.png](images/13b-ebs-volumes-empty.png) 외 ([11단계 기록](steps/11-cleanup.md#4--실제-기록)) |
