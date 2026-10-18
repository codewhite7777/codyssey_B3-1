# 7단계. SSH 접속과 아웃바운드 확인

[← 단계 목록](../guide.md) · [이전: 6단계](./06-ec2.md) · [다음: 8단계 →](./08-nginx.md)

> **한 줄 요약**: 내 PC에서 서버에 접속하고, 서버에서 인터넷으로 나갈 수 있는지 확인한다.

## 1. 무엇을, 왜

| 항목 | 내용 |
|---|---|
| 무엇을 | SSH 접속, 서버에서 `curl https://example.com` |
| 왜 | 과제 요구: "SSH 접속 가능", "인스턴스에서 인터넷 아웃바운드 가능" |
| 어디서 | `$` 내 PC 터미널 → 접속 후 `ubuntu@...$` EC2 안 |

## 2. 할 일

내 PC 터미널에서:

```bash
chmod 400 ~/keys/b3-1-key.pem
ssh -i ~/keys/b3-1-key.pem ubuntu@<퍼블릭IP>
```

| 명령 | 하는 일 |
|---|---|
| `chmod 400` | 키 파일을 나만 읽게 함. 권한이 넓으면 ssh가 키를 거부함 |
| `ssh -i 키 ubuntu@IP` | 키로 서버에 접속. Ubuntu의 기본 사용자는 `ubuntu` |

처음 접속 때 `Are you sure you want to continue connecting?`이 나오면 `yes`.

접속한 EC2 안에서:

```bash
curl -I https://example.com
```

## 3. 확인과 📸

| 확인할 것 | 📸 |
|---|---|
| 프롬프트가 `ubuntu@ip-10-0-1-xx:~$`로 바뀜 | `07-ssh-login.png` |
| `curl -I` 첫 줄에 `HTTP/... 200` (서버 → 인터넷 길이 열림) | `08-outbound-curl.png` |

## 4. ✍️ 실제 기록

**상태**: ⬜ 진행 전

| 항목 | 내용 |
|---|---|
| 한 날짜 | |
| 결과 | |
| 막힌 점 | |

---

[← 단계 목록](../guide.md) · [이전: 6단계](./06-ec2.md) · [다음: 8단계 →](./08-nginx.md)
