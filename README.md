# Codyssey B3-1: AWS 퍼블릭 웹 서비스

이 저장소는 과제에서 요구하는 서울 리전의 최소 AWS 경로를 정의합니다.

`External user → Internet Gateway → Public Subnet → Security Group → EC2 → Nginx`

## 구현 내용

- `infra/template.yaml`: VPC 1개, 퍼블릭 서브넷, IGW, 라우팅 테이블, 제한된 SG, EC2/Nginx 서버 1개를 구성하는 CloudFormation 스택입니다.
- `iam/cloudformation-deployer-policy.json`: 전용 배포 IAM 자격 증명을 위한 최소 권한 시작 정책입니다. `AdministratorAccess`, S3 또는 RDS 권한은 부여하지 않습니다.
- `scripts/deploy.sh`: 입력값을 검증하고 `ap-northeast-2`에만 배포합니다.
- `scripts/integration_test.py`: 읽기 전용 스택/리소스 확인과 외부 `GET /health` 확인을 수행합니다.
- `scripts/cleanup.sh`: 명시적인 확인을 받은 뒤 스택을 삭제하고 완료될 때까지 기다립니다.
- `scripts/generate_architecture.py`: 아키텍처 PNG를 재현 가능한 방식으로 생성합니다.
- `tests/test_template.py`: 로컬 구조 및 보안 검사를 수행합니다.

EC2 키 페어는 서울 리전에 이미 존재해야 합니다. 키 페어 이름과 학습자의 공인 `/32`(또는 의도적으로 좁힌 CIDR)를 배포 스크립트에 전달하세요. 프라이빗 키는 절대 커밋하지 마세요.

```sh
python3 -m pip install -r requirements-test.txt
pytest -q
bash -n scripts/deploy.sh scripts/cleanup.sh
./scripts/deploy.sh codyssey-web <key-name> <your-public-ip>/32
python3 scripts/integration_test.py codyssey-web
./scripts/cleanup.sh codyssey-web --confirm
```

## 증거 상태

| Artifact | Status |
| --- | --- |
| `docs/architecture.png` | 로컬 설계 산출물 사용 가능 |
| 로컬 단위/정적 테스트 | 구현 중 4개 통과; 체크아웃 변경 후 다시 실행 필요 |
| Live external `/health` response | Pending; 라이브 배포를 수행했다고 주장하지 않음 |
| Live AWS screenshots | Pending |
| Cleanup confirmation | 권한 있는 non-root 배포가 이루어질 때까지 Pending |

이 작업에서 확인된 AWS 자격 증명은 root 사용자를 가리킵니다. 과제에서는 root 액세스를 명시적으로 금지하므로 AWS 스택을 생성하거나 삭제하지 않았습니다. `iam/cloudformation-deployer-policy.json`의 정책을 사용하는 전용 IAM 사용자 또는 역할을 준비한 뒤, `docs/evidence/live/`에 라이브 증거를 수집하세요.

## 제출 문서

- [아키텍처](docs/architecture.png)
- [트러블슈팅 보고서](docs/troubleshooting.md)
- [정리 체크리스트](docs/cleanup-checklist.md)
- [증거 규칙](docs/evidence/README.md)

다이어그램과 문서는 로컬 산출물과 실제 AWS 증거를 구분합니다. 타임스탬프가 포함된 라이브 캡처가 추가되기 전까지는 외부 요청이 성공했다고 주장하지 않습니다.
