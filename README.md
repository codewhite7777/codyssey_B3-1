# B3-1 · 내가 만든 웹사이트를 인터넷에 올려 누구나 쓰게 하기

| 분야 | 구분 | 학습시간 | 필수/선택 |
|---|---|---|---|
| AI/SW 기초 | 클라우드와 AI API | 40시간 | 필수 |

> **AWS 서울 리전에 네트워크(VPC)를 직접 만들고, 서버(EC2)의 웹 서버(Nginx)를 외부에서 접속할 수 있게 한 뒤, 근거를 남기고 깨끗이 치우는 과제입니다.**
> AWS 콘솔에서 직접 구성 · 필수 요구사항만 (보너스 제외)

## 1. 한눈에 보기

![전체 흐름](docs/images/overview.svg)

**그림 읽는 법**: 왼쪽에서 오른쪽(①→⑤)이 **요청**, 오른쪽에서 왼쪽(⑤→⑨)이 **응답**입니다. 칸마다 그 지점에서 **무슨 처리를 하는지**, 맨 아랫줄은 그 지점이 **막히면 나오는 증상**입니다. 뒤 배경은 어디까지가 VPC, Subnet, SG 범위인지를 보여줍니다.

아래 표는 이 길을 **만드는 순서**입니다. 단계가 쌓이면서 외부 요청 결과가 바뀝니다.

| 단계 | 만드는 것 | 하는 일 | 이 단계 후 외부 요청 결과 |
|---|---|---|---|
| 1 | IAM 사용자, 정책 | 누가 AWS를 조작할 수 있는지 제한 | 서버 없음 |
| 2 | VPC, Subnet | 격리된 내 네트워크와 서버 구역. 서버에 퍼블릭 IP 자동 부여 | 서버 없음 |
| 3 | Internet Gateway | 인터넷과 연결되는 정문. 퍼블릭 ↔ 프라이빗 주소 변환 | 서버 없음 |
| 4 | Route Table | VPC 밖으로 가는 트래픽(응답)을 IGW로 보냄 | 서버 없음 |
| 5 | Security Group | 80은 누구나, 22는 내 IP만 들어오게 함 | 서버 없음 |
| 6 | EC2 | 길 끝에 놓인 서버 | **refused** (받을 프로그램 없음) |
| 7 | SSH 접속 | 내 PC에서 서버에 들어가 설정 | refused |
| 8 | Nginx, `/health` | 80에서 요청을 받아 `OK` 응답 | **200 OK** ✔ |
| 9 | 외부 검증 | 내 PC에서 전체 경로가 열렸음을 증명 | 200 OK (📸 증빙) |
| 10 | 트러블슈팅 | SG의 80을 잠시 빼서 고장을 재현 | **timeout** → 복구 후 200 OK |
| 11 | 리소스 정리 | 안쪽부터 삭제해 과금 요인 제거 | 응답 없음 |

> **refused**는 요청이 서버까지 **왔지만** 받을 프로그램이 없는 것(6단계), **timeout**은 서버까지 **오지 못한** 것(10단계)입니다. 그래서 장애가 나면 timeout은 바깥(라우팅, SG, 퍼블릭 IP)부터, refused는 서버 안(Nginx)부터 봅니다.

단계별 자세한 방법은 [실습 가이드](docs/guide.md)에 있습니다.

## 2. 외부 접속 검증

| 항목 | 내용 |
|---|---|
| 선택한 방식 | **(B) `GET http://<퍼블릭IP>/health`** |
| 접속 정보 | `http://52.79.204.114/health` (실습 당시 퍼블릭 IP. 리소스 정리 후에는 접속되지 않음) |
| 확인 일시 | 2026-10-20 10:31 (KST) |
| 결과 | `HTTP/1.1 200 OK`, 본문 `OK` |
| 증빙 | 📸 [10-external-health.png](docs/images/10-external-health.png) (내 PC 터미널), [10b-external-browser.png](docs/images/10b-external-browser.png) (브라우저) |

## 3. 과제 요구사항 확인

| 요구 | 어떻게 했나 | 근거 | 상태 |
|---|---|---|---|
| VPC, Public Subnet | `10.0.0.0/16`, `10.0.1.0/24`, 퍼블릭 IP 자동 할당, `0.0.0.0/0 → IGW` 테이블 연결 | 📸 02, 04 | ✅ |
| IGW를 VPC에 연결 | `b3-1-igw` Attached | 📸 03 | ✅ |
| Route Table `0.0.0.0/0 → IGW` | `b3-1-rt-public`을 서브넷에 연결 | 📸 04 | ✅ |
| 인스턴스 아웃바운드 | EC2에서 `curl -I https://example.com` → `HTTP/2 200` | 📸 08 | ✅ |
| EC2 1대, SSH 접속 | t3.micro, 내 IP에서 키로 접속 | 📸 06, 07 | ✅ |
| 웹 서버 실행, `curl localhost` 200 | Nginx `active (running)`, `curl -i http://localhost/health` → `200 OK` | 📸 09 | ✅ |
| SG 필요 포트만 | 80 ← `0.0.0.0/0`, 22 ← 내 IP `/32`, 전체 포트 규칙 없음 | 📸 05 | ✅ |
| IAM 최소 권한 | EC2 액션만, 생성·삭제는 서울 리전만, S3/RDS·관리자 권한 없음 | 📸 01, [iam-policy.json](docs/iam-policy.json) | ✅ |
| 외부 접속 검증 (B) | `/health` → 200 OK, `OK` | 📸 10, 위 2장 | ✅ |
| 아키텍처 다이어그램 | VPC, Subnet, IGW, Route Table, SG, EC2, 요청 흐름 | [architecture.png](docs/architecture.png) | ✅ |
| 트러블슈팅 보고서 | SG 80 제거 → timeout → 근거로 원인 확인 → 복구 | 📸 11, 12, [troubleshooting.md](docs/troubleshooting.md) | ⬜ |
| 리소스 정리 5종 | EC2, EBS, Elastic IP(할당 안 함), IGW, VPC | 📸 13, [cleanup-checklist.md](docs/cleanup-checklist.md) | ⬜ |
| 제약: 루트 미사용, 서울 리전, 프리 티어 | 루트는 IAM 사용자 생성까지만, t3.micro(크레딧 Standard), EIP·NAT·ALB 만들지 않음 | 📸 01, 06, 06b | ✅ |

## 4. 문서

| 문서 | 언제 보나 |
|---|---|
| [docs/guide.md](docs/guide.md) | **실습할 때**: 단계 목록과 진행 상태. 단계마다 할 일과 실제 기록(스크린샷) |
| [docs/design.md](docs/design.md) | 설계 이유, 요청·응답 왕복 |
| [docs/architecture.png](docs/architecture.png) | 제출물: 아키텍처 다이어그램 |
| [docs/troubleshooting.md](docs/troubleshooting.md) | 제출물: 트러블슈팅 보고서 |
| [docs/cleanup-checklist.md](docs/cleanup-checklist.md) | 제출물: 리소스 정리 체크리스트 |
| [docs/concepts.md](docs/concepts.md) | 개념 공부: VPC, 포트, SG, IAM 등 |
| [docs/evaluation.md](docs/evaluation.md) | 평가 준비: 질문별 답변 |
| [docs/images/](docs/images/README.md) | 스크린샷 01~13 목록 |
