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
| `06a-ec2-launch-network.png` | 시작 설정: 네트워크(편집 후) | [x] |
| `06b-ec2-launch-storage-credit.png` | 시작 설정: 8GiB gp3, 크레딧 표준 | [x] |
| `06-ec2-instance.png` | 인스턴스 Running, 서브넷, 퍼블릭 IP, t3.micro | [x] |
| `06c-ec2-volume.png` | EBS 볼륨, 종료 시 삭제 예 | [x] |
| `07-ssh-login.png` | 내 PC 터미널의 SSH 접속 성공 화면 | [x] |
| `08-outbound-curl.png` | EC2 안에서 `curl -I https://example.com` | [x] |
| `09a-refused-before-nginx.png` | Nginx 설치 전 내 PC에서 refused | [x] |
| `09b-localhost-default.png` | 설치 직후 `curl -i http://localhost` 기본 페이지 | [x] |
| `09-localhost-200.png` | `systemctl status nginx` + `curl -i http://localhost/health` | [x] |
| `10-external-health.png` | **내 PC**에서 `curl -i http://<퍼블릭IP>/health` | [x] |
| `10b-external-browser.png` | 브라우저 `/health` → OK | [x] |
| `11-troubleshoot-mobile-chrome.png` | 트러블슈팅 요약: 휴대폰 Chrome timeout vs 삼성 인터넷 OK | [x] |
| `11a`~`11e` | 트러블슈팅 과정: Chrome 설정 켜짐·끔, timeout, 세부정보, 삼성 인터넷 OK | [x] |
| `13-ec2-terminate-confirm.png` | EC2 종료 확인 창 | [x] |
| `13a-ec2-terminated.png` | EC2 상태 종료됨 | [x] |
| `13b-ebs-volumes-empty.png` | EBS 볼륨 없음 | [x] |
| `13c-eip-empty.png` | 탄력적 IP 없음 (할당 안 했지만 과금 요인이라 확인) | [x] |
| `13d-keypair-delete.png` | 키 페어 삭제 메뉴 | [x] |
| `13e-keypair-empty.png` | 키 페어 없음 | [x] |
| `13f-pem-removed.png` | 내 PC `.pem` 삭제 | [x] |
| `13g-known-hosts.png` | `ssh-keygen -R`로 서버 지문 기록 제거 | [x] |
| `13h-sg-delete.png` | 보안 그룹 삭제 메뉴 | [x] |
| `13i-sg-deleted-banner.png` | 보안 그룹 삭제 완료 배너 | [x] |
| `13j-sg-list.png` | 보안 그룹 (2), default만 남음 | [x] |
| `13k0-subnet-menu.png` | 서브넷 선택과 삭제 메뉴 | [x] |
| `13k-subnet-delete.png` | 서브넷 삭제 확인 창 (RAM 조회 권한 안내) | [x] |
| `13l-subnet-deleted.png` | 서브넷 삭제 완료, 기본 서브넷 4개만 남음 | [x] |
| `13m0`~`13m2` | 라우팅 테이블: 오래된 화면, 삭제 막힘, 새로 고침 후 확인 창 | [x] |
| `13m-rt-deleted.png` | 라우팅 테이블 삭제 완료, 기본 2개만 남음 | [x] |
| `13n0-igw-detach-menu.png` | IGW 분리 메뉴 (삭제는 비활성) | [x] |
| `13n-igw-detached.png` | IGW Detached | [x] |
| `13o-igw-deleted.png` | 글로벌 검색: IGW ID 결과 없음 | [x] |
| `13p0-vpc-delete-menu.png` | VPC 삭제 메뉴 | [x] |
| `13p-vpc-deleted.png` | VPC 삭제 완료, 기본 VPC만 | [x] |
| `13q-global-view.png` | 글로벌 보기 리전 탐색기, 모두 0 | [x] |
| `13r-global-search.png` | 글로벌 검색, 기본 리소스와 종료된 인스턴스만 | [x] |
| `13s-search-b3-1.png` | `b3-1` 검색 결과 1개(종료된 인스턴스) | [x] |
| `keypair.svg`, `cleanup_order.svg` | 설명 그림: 키 페어 역할, 정리 순서 | [x] |

퍼블릭 IP는 EC2를 Stop/Start하면 바뀐다. IP가 보이는 06, 07, 10은 같은 날 한 번에 찍는다.

`focus/` 폴더: README 4장 "과정 따라보기"에서 쓰는 확대 이미지. 위 스크린샷의 핵심 부분만 잘라낸 것이다.
