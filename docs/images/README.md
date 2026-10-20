# 스크린샷 목록

실습하면서 아래 이름으로 저장한다. 계정 ID와 내 IP 일부는 가리되, 내 IP 뒤의 `/32`는 보이게 남긴다.

| 파일 | 찍을 화면 | 상태 |
|---|---|---|
| `00a-region-seoul.png` | (준비) 리전을 서울로 선택 | [x] |
| `00b-mfa-device-type.png` | (준비) MFA 유형: 인증 관리자 앱 | [x] |
| `00c-mfa-setup.png` | (준비) QR 스캔 후 코드 입력 (QR 가림) | [x] |
| `00d-iam-policy-create.png` | (준비) IAM 정책 목록 → 정책 생성 | [x] |
| `00e-iam-policy-json.png` | (준비) 정책 JSON 붙여넣기 | [x] |
| `00f-iam-policy-review.png` | (준비) 정책 검토: EC2만, 서울 조건 | [x] |
| `00g-iam-users-list.png` | (준비) IAM 사용자 목록 → 사용자 생성 | [x] |
| `00h-iam-user-details.png` | (준비) 사용자 세부 정보 | [x] |
| `00i-iam-user-permissions.png` | (준비) 직접 정책 연결: b3-1-policy | [x] |
| `00j-iam-user-review.png` | (준비) 검토 및 생성 | [x] |
| `00k-iam-user-created.png` | (준비) 생성 완료 (로그인 URL 가림) | [x] |
| `00l-iam-user-created-list.png` | (준비) IAM 사용자 목록에 b3-1-user | [x] |
| `00m-iam-policy-summary.png` | (준비) 정책 요약: EC2 하나, 서울 조건 | [x] |
| `01-iam-user-policy.png` | IAM 사용자와 연결된 정책 (AdministratorAccess 없음) | [x] |
| `02a-vpc-create.png` | VPC 생성 입력 (VPC만, `10.0.0.0/16`, 태그 2개) | [x] |
| `02b-vpc-created.png` | VPC 생성 결과 (VPC ID, Available) | [x] |
| `02c-subnet-create.png` | 서브넷 생성 입력 | [x] |
| `02d-subnet-public-ip.png` | 퍼블릭 IPv4 자동 할당 활성화 | [x] |
| `02-vpc-subnet.png` | 서브넷 상세: CIDR·AZ·VPC·퍼블릭 IP 자동 할당 예 | [x] |
| `03-igw-attached.png` | IGW 상태 Attached, VPC ID | [x] |
| `04-route-table.png` | 경로(`0.0.0.0/0 → igw-`) + 서브넷 연결 탭 | [x] |
| `05-security-group.png` | 인바운드 규칙 2개 (80 전체, 22 내 IP/32) | [x] |
| `06-ec2-instance.png` | 인스턴스 Running, 서브넷, 퍼블릭 IP, t3.micro | [ ] |
| `07-ssh-login.png` | 내 PC 터미널의 SSH 접속 성공 화면 | [ ] |
| `08-outbound-curl.png` | EC2 안에서 `curl -I https://example.com` | [ ] |
| `09-localhost-200.png` | `systemctl status nginx` + `curl -i http://localhost` | [ ] |
| `10-external-health.png` | **내 PC**에서 `curl -i http://<퍼블릭IP>/health` | [ ] |
| `11-troubleshoot-before.png` | 장애 상황 (timeout, SG 규칙) | [ ] |
| `12-troubleshoot-after.png` | 조치 후 정상 응답 | [ ] |
| `13-cleanup.png` | EC2 Terminated, 볼륨 0개, VPC 목록 | [ ] |

퍼블릭 IP는 EC2를 Stop/Start하면 바뀐다. IP가 보이는 06, 07, 10은 같은 날 한 번에 찍는다.
