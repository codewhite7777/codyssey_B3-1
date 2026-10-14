# Codyssey B3-1: 내가 만든 웹사이트를 인터넷에 올려 누구나 쓰게 하기

AWS 서울 리전(`ap-northeast-2`)에 VPC를 직접 구성하고, EC2에 Nginx를 올려 외부에서 접속 가능한 웹 서비스를 만든 기록입니다.
모든 리소스는 **AWS 콘솔에서 직접** 만들었고, 실습 후 모두 삭제했습니다.

```
외부 사용자 → Internet Gateway → Route Table(0.0.0.0/0 → IGW) → Public Subnet → Security Group(80) → EC2 → Nginx
```

## 1. 제출물

| 산출물 | 위치 |
|---|---|
| 아키텍처 다이어그램 | [docs/architecture.png](docs/architecture.png) |
| 외부 접속 증빙 | 이 문서의 [3. 외부 접속 검증](#3-외부-접속-검증) |
| 트러블슈팅 보고서 | [docs/troubleshooting.md](docs/troubleshooting.md) |
| 리소스 정리 체크리스트 | [docs/cleanup-checklist.md](docs/cleanup-checklist.md) |
| (학습) 핵심 개념 정리 | [docs/concepts.md](docs/concepts.md) |
| (학습) 평가 항목 답변 | [docs/evaluation.md](docs/evaluation.md) |
| 적용한 IAM 정책 | [docs/iam-policy.json](docs/iam-policy.json) |

보너스 과제(HTTPS, Docker)는 수행하지 않았습니다.

## 2. 구성 요약

| 구분 | 설정 |
|---|---|
| 리전 | `ap-northeast-2` (서울) |
| VPC | `b3-1-vpc` / `10.0.0.0/16` |
| Public Subnet | `b3-1-subnet-public` / `10.0.1.0/24` / AZ: `ap-northeast-2_` / 퍼블릭 IPv4 자동 할당 ON |
| Internet Gateway | `b3-1-igw` / `b3-1-vpc`에 Attach |
| Route Table | `b3-1-rt-public` / `10.0.0.0/16 → local`, `0.0.0.0/0 → b3-1-igw` / 서브넷 연결 |
| Security Group | `b3-1-sg-web` / 인바운드 `80 ← 0.0.0.0/0`, `22 ← 내 IP/32` |
| EC2 | `b3-1-ec2-web` / t3.micro (크레딧 Standard) / Ubuntu ____ LTS / EBS 8GiB gp3 |
| Elastic IP | 할당하지 않음 (자동 퍼블릭 IP 사용) |
| 웹 서버 | Nginx (`/health` → `200 OK`, `OK`) |
| IAM | 사용자 `b3-1-user` / [docs/iam-policy.json](docs/iam-policy.json) 적용, AdministratorAccess 없음 |
| 태그 | 모든 리소스에 `Project=b3-1` |

## 3. 외부 접속 검증

- **선택한 방식: (B) `GET http://<퍼블릭IP>/health`**
- 접속 정보: `http://___.___.___.___/health` (실습 당시 퍼블릭 IP. 리소스 삭제 후에는 접속되지 않음)
- 확인 날짜: 2026-__-__

내 PC 터미널에서 실행했습니다.

```
$ curl -i http://___.___.___.___/health
HTTP/1.1 200 OK
...
OK
```

![외부 /health 호출](docs/images/10-external-health.png)

**B를 위해 구성한 것**
1. Nginx 설정(`/etc/nginx/sites-available/default`)의 `server {}` 안에 아래 블록을 추가
   ```nginx
   location = /health {
       default_type text/plain;
       return 200 "OK\n";
   }
   ```
2. `sudo nginx -t`로 문법 확인 후 `sudo systemctl reload nginx`
3. Security Group에서 80 포트를 `0.0.0.0/0`에 허용
4. 서브넷의 퍼블릭 IPv4 자동 할당을 켜서 EC2에 퍼블릭 IP 부여

## 4. 진행 과정과 증빙

| # | 단계 | 확인 내용 | 스크린샷 |
|---|---|---|---|
| 01 | IAM | 실습용 IAM 사용자, 최소 권한 정책, AdministratorAccess 없음 | [01](docs/images/01-iam-user-policy.png) |
| 02 | 네트워크 | VPC `10.0.0.0/16`, Subnet `10.0.1.0/24` | [02](docs/images/02-vpc-subnet.png) |
| 03 | 네트워크 | Route Table의 `0.0.0.0/0 → IGW` 경로와 서브넷 연결 | [03](docs/images/03-route-table.png) |
| 04 | 네트워크 | IGW가 VPC에 Attached | [04](docs/images/04-igw-attached.png) |
| 05 | 보안 | SG 인바운드 80(전체), 22(내 IP `/32`)만 존재 | [05](docs/images/05-security-group.png) |
| 06 | 컴퓨트 | EC2 Running, Public Subnet 배치, 퍼블릭 IP | [06](docs/images/06-ec2-instance.png) |
| 07 | 컴퓨트 | SSH 접속 성공 | [07](docs/images/07-ssh-login.png) |
| 08 | 네트워크 | 인스턴스에서 `curl -I https://example.com` 성공 (아웃바운드) | [08](docs/images/08-outbound-curl.png) |
| 09 | 웹 서버 | `systemctl status nginx` 실행 중, `curl -i http://localhost` 200 | [09](docs/images/09-localhost-200.png) |
| 10 | 검증 | 내 PC에서 `curl -i http://<퍼블릭IP>/health` 200 + `OK` | [10](docs/images/10-external-health.png) |
| 11 | 트러블슈팅 | 장애 재현 화면 | [11](docs/images/11-troubleshoot-before.png) |
| 12 | 트러블슈팅 | 조치 후 정상 화면 | [12](docs/images/12-troubleshoot-after.png) |
| 13 | 정리 | EC2 Terminated, 볼륨·VPC 삭제 확인 | [13](docs/images/13-cleanup.png) |

## 5. 평가 항목 ↔ 근거

| 평가 질문 | 근거 |
|---|---|
| VPC, Subnet, IGW, Route Table 구성 | 스크린샷 02~04, [다이어그램](docs/architecture.png) |
| SSH 접속, 웹 서버 실행 | 스크린샷 07, 09 |
| SG 최소 포트, SSH IP 제한 | 스크린샷 05 |
| 외부 접속 검증 (B) | 3장, 스크린샷 10 |
| 정리 5종 (EC2/EBS/EIP/IGW/VPC) | [정리 체크리스트](docs/cleanup-checklist.md), 스크린샷 13 |
| 개념 설명, 응용 질문 | [개념 정리](docs/concepts.md), [평가 답변](docs/evaluation.md) |

## 6. 리소스 추적 기준

- **태그**: 모든 리소스에 `Project=b3-1`
- **이름 규칙**: `b3-1-<리소스>-<용도>` (예: `b3-1-sg-web`)
- **체크리스트**: 리소스를 만들 때마다 [cleanup-checklist.md](docs/cleanup-checklist.md)에 바로 기록
- **확인**: 정리 후 EC2 Global View로 다른 리전에 남은 리소스가 없는지 확인

## 7. 보안 메모

- 루트 계정은 최초 설정(MFA, IAM 사용자 생성, 결제 알림)에만 사용했고, 실습은 IAM 사용자로만 진행했습니다.
- `.pem` 키와 AWS 자격 증명은 레포에 올리지 않았습니다(`.gitignore`).
- 스크린샷의 AWS 계정 ID와 내 IP 일부는 가렸습니다.
