# 8단계. Nginx와 `/health` 만들기

[← 단계 목록](../guide.md) · [이전: 7단계](./07-ssh.md) · [다음: 9단계 →](./09-verify.md)

> **한 줄 요약**: 서버에 웹 서버(Nginx)를 설치하고, `/health` 주소가 `OK`를 돌려주게 만든다.

## 1. 무엇을, 왜

| 항목 | 내용 |
|---|---|
| 무엇을 | Nginx 설치, `/health` 고정 응답 설정 |
| 왜 | 외부 접속 검증을 (B) `/health` 방식으로 하기 때문 |
| 어디서 | `ubuntu@...$` EC2 안 |

## 2. 할 일

**설치와 확인**

```bash
sudo apt update
sudo apt install -y nginx
systemctl status nginx --no-pager
curl -i http://localhost
```

| 명령 | 하는 일 |
|---|---|
| `sudo apt update` | 설치할 수 있는 패키지 목록 새로고침 |
| `sudo apt install -y nginx` | Nginx 설치. 설치 직후 80 포트에서 대기 |
| `systemctl status nginx` | 실행 중인지 확인 (`active (running)`) |
| `curl -i http://localhost` | 서버 안에서 요청. `HTTP/1.1 200 OK` |

**`/health` 추가**

```bash
sudo nano /etc/nginx/sites-available/default
```

`server {` 블록 안, `server_name _;` 줄 아래에 붙여넣고 저장(`Ctrl+O` → `Enter` → `Ctrl+X`):

```nginx
location = /health {
    default_type text/plain;
    return 200 "OK\n";
}
```

```bash
sudo nginx -t
sudo systemctl reload nginx
curl -i http://localhost/health
```

| 명령 | 하는 일 |
|---|---|
| `sudo nginx -t` | 설정 문법 검사. `syntax is ok`, `test is successful` |
| `sudo systemctl reload nginx` | 서버를 끄지 않고 바뀐 설정만 다시 읽음 |
| `curl -i http://localhost/health` | `/health` 응답 확인 |

## 3. 확인과 📸

| 확인할 것 | 📸 |
|---|---|
| `active (running)`, `HTTP/1.1 200 OK`, 마지막 줄 `OK` | `09-localhost-200.png` (`systemctl status`와 `curl`이 함께 보이게) |

## 4. ✍️ 실제 기록

**상태**: ⬜ 진행 전

| 항목 | 내용 |
|---|---|
| 한 날짜 | |
| 결과 | |
| 막힌 점 | |
| 내 말로 한 줄 | |

---

[← 단계 목록](../guide.md) · [이전: 7단계](./07-ssh.md) · [다음: 9단계 →](./09-verify.md)
