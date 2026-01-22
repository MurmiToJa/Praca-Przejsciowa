# 🔬 Praca Przejsciowa - Network Security Testing App

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-Educational-orange.svg)

**Środowisko badawcze do analizy zabezpieczeń sieciowych**

*Praca Przejściowa - Projekt z zakresu cyberbezpieczeństwa*

[Funkcje](#-funkcje) • [Instalacja](#-instalacja) • [Użycie](#-użycie) • [Dokumentacja](#-dokumentacja-techniczna)

</div>


## 📖 O Projekcie

Network Security Testing App to  platforma webowa do przeprowadzania kontrolowanych testów penetracyjnych i analizy odporności systemów sieciowych na różne typy ataków DDoS. Projekt został stworzony w ramach **Pracy Przejściowej** z zakresu cyberbezpieczeństwa.

### 🎯 Cele Projektu

- Demonstracja różnych technik ataków sieciowych w środowisku edukacyjnym
- Analiza wpływu ataków DDoS na infrastrukturę sieciową
- Badanie skuteczności mechanizmów obronnych
- Edukacja w zakresie cyberbezpieczeństwa i etycznego hackingu

### 🔬 Zakres Badań

Projekt umożliwia testowanie następujących scenariuszy:
- Ataki warstwy aplikacji (HTTP Flood)
- Ataki warstwy transportowej (SYN Flood)
- Kombinowane ataki wielowektorowe
- Analiza zachowania systemów pod obciążeniem

---

## ✨ Funkcje

### 🎨 Interfejs Webowy

- **UI** - Intuicyjny interfejs
- **Panel kontrolny** - Łatwa konfiguracja parametrów ataku (IP, port, wątki)
- **Monitoring w czasie rzeczywistym** - Status aktywnych ataków na żywo
- **System logowania** - Krótkie logi

### 🛠️ Typy Ataków

#### 1. **HTTP Flood (Socket)**
Podstawowy atak HTTP wykorzystujący natywne sockety Pythona do wysyłania masowych żądań GET.

**Charakterystyka:**
- Wykorzystuje standardową bibliotekę `socket`
- Niskie zużycie zasobów
- Wysoka częstotliwość żądań

#### 2. **HTTP Flood (Scapy)**
Zaawansowany atak HTTP z wykorzystaniem biblioteki Scapy do tworzenia niestandardowych pakietów TCP/IP.

**Charakterystyka:**
- Pełna kontrola nad pakietami
- Możliwość spoofingu IP
- Manipulacja nagłówkami TCP

#### 3. **Combined Attack**
Kompleksowy atak łączący wiele wektorów: GET, POST i SYN packets.

**Charakterystyka:**
- Żądania GET i POST przez `requests`
- Pakiety SYN przez Scapy
- Maksymalne obciążenie celu

#### 4. **SYN Flood**
Klasyczny atak SYN Flood wykorzystujący niekompletny TCP handshake.

**Charakterystyka:**
- Wyczerpanie zasobów połączeń
- Atakuje warstwę transportową
- Trudny do filtrowania

---

## 🚀 Instalacja

### Wymagania Systemowe

- **Docker** 20.10+ i **Docker Compose** 1.29+ (zalecane)
- **LUB** Python 3.8+ z pip
- System operacyjny: Windows, Linux, macOS
- Minimum 2GB RAM
- Połączenie sieciowe

### Metoda 1: Docker (Zalecana) 🐳

Docker zapewnia tutaj środowisko z wszystkimi zależnościami.

```bash
# 1. Klonujemy repozytorium
git clone https://github.com/MurmiToJa/Praca-Przejsciowa.git
cd network-security-lab

# 2. Budujemy i odpalamy kontener
docker-compose up --build

# 3. Otwieramy przeglądarkę
# Przejdź do: http://localhost:5000
```

**Zatrzymanie:**
```bash
docker-compose down
```

**Restart:**
```bash
docker-compose restart
```

### Metoda 2: Instalacja Lokalna 🐍

#### Windows

```powershell
# 1. Klonujemy repozytorium
git clone https://github.com/MurmiToJa/Praca-Przejsciowa.git
cd network-security-lab

# 2. Tworzymy środowisko wirtualne
python -m venv venv
.\venv\Scripts\activate

# 3. Instalujemy zależności
pip install -r requirements.txt

# 4. Instalujemy Npcap (wymagane dla Scapy)
# Pobieramy z: https://npcap.com/#download
# Instalujemy z opcją "WinPcap API-compatible Mode"

# 5. Odpalamy aplikację (jako Administrator!)
python app.py
```

#### Linux/macOS

```bash
# 1. Klonujemy repozytorium
git clone https://github.com/MurmiToJa/Praca-Przejsciowa.git
cd network-security-lab

# 2. Tworzymy środowisko wirtualne
python3 -m venv venv
source venv/bin/activate

# 3. Instalujemy zależności systemowe (Linux)
sudo apt-get update
sudo apt-get install tcpdump libpcap-dev

# 4. Instalujemy zależności Python
pip install -r requirements.txt

# 5. Odpalamy aplikację (z sudo dla Scapy)
sudo python3 app.py
```

---

## 💻 Użycie

### Krok po kroku

1. **Uruchamiamy aplikację** zgodnie z instrukcją instalacji
2. **Otwieramy przeglądarkę** i przejdź do `http://localhost:5000`
3. **Konfigurujemy parametry ataku:**
   - **Docelowy adres IP**: Wprowadź IP celu (np. `192.168.1.100`)
   - **Port**: Ustaw port docelowy (domyślnie `80`)
   - **Liczba wątków**: Wybierz intensywność (1-100, domyślnie `10`)
4. **Wybieramy typ ataku** i kliknij przycisk **"Uruchom"**
5. **Monitorig statusu** w panelu statusu i logach
6. **Zatrzymujemy atak** klikając przycisk **"Zatrzymaj"**

### Przykładowe Scenariusze Testowe

---

## 🏗️ Dokumentacja Techniczna

### Architektura Systemu

```
┌─────────────────────────────────────────┐
│         Interfejs Webowy (HTML/CSS/JS)  │
│         http://localhost:5000           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Flask REST API (Python)         │
│   - /start_attack (POST)                │
│   - /stop_attack (POST)                 │
│   - /status (GET)                       │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│      Moduły Ataków (Python)             │
│   - http_flood.py                       │
│   - scapy_http.py                       │
│   - combined_attack.py                  │
│   - syn_flood.py                        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Sieć / Cel Ataku                │
└─────────────────────────────────────────┘
```

### Struktura Projektu

```
network-security-lab/
├── 📄 app.py                    # Główna aplikacja Flask z API
├── 📁 attacks/                  # Moduły ataków
│   ├── http_flood.py           # Atak HTTP przez socket
│   ├── scapy_http.py           # Atak HTTP przez Scapy
│   ├── combined_attack.py      # Atak kombinowany
│   └── syn_flood.py            # Atak SYN Flood
├── 📁 templates/                # Szablony HTML
│   └── index.html              # Główny interfejs
├── 📁 static/                   # Zasoby statyczne
│   ├── style.css               # Style CSS
│   └── script.js               # Logika JavaScript
├── 🐳 Dockerfile                # Konfiguracja obrazu Docker
├── 🐳 docker-compose.yml        # Orkiestracja kontenerów
├── 📋 requirements.txt          # Zależności Python
├── 📖 README.md                 # Dokumentacja
└── 🚫 .dockerignore             # Wykluczenia Docker
```

### Technologie

| Warstwa | Technologia | Wersja | Zastosowanie |
|---------|-------------|--------|--------------|
| **Backend** | Python | 3.11+ | Logika aplikacji |
| **Framework** | Flask | 3.0.0 | Serwer HTTP i API |
| **Networking** | Scapy | 2.5.0 | Manipulacja pakietami |
| **HTTP Client** | Requests | 2.31.0 | Żądania HTTP |
| **Frontend** | HTML5/CSS3/JS | - | Interfejs użytkownika |
| **Konteneryzacja** | Docker | 20.10+ | Izolacja środowiska |

### API Endpoints

#### `POST /start_attack`
Uruchamia wybrany typ ataku.

**Request Body:**
```json
{
  "attack_type": "http_flood",
  "target_ip": "192.168.1.100",
  "port": 80,
  "threads": 10
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Attack http_flood started on 192.168.1.100:80"
}
```

#### `POST /stop_attack`
Zatrzymuje aktywny atak.

**Request Body:**
```json
{
  "attack_type": "http_flood"
}
```

#### `GET /status`
Pobiera status aktywnych ataków.

**Response:**
```json
{
  "active_attacks": ["http_flood", "syn_flood"]
}
```

---

## 🐛 Rozwiązywanie Problemów

### Problem: Scapy nie działa na Windows

**Rozwiązanie:**
1. Zainstaluj [Npcap](https://npcap.com/#download)
2. Podczas instalacji zaznacz "Install Npcap in WinPcap API-compatible Mode"
3. Uruchom aplikację jako Administrator

### Problem: "Permission denied" na Linux

**Rozwiązanie:**
```bash
# Uruchom z sudo
sudo python3 app.py

# LUB nadaj uprawnienia CAP_NET_RAW
sudo setcap cap_net_raw=eip $(which python3)
```

### Problem: Docker nie może wysyłać pakietów

**Rozwiązanie:**
Upewnij się, że `docker-compose.yml` zawiera:
```yaml
cap_add:
  - NET_ADMIN
  - NET_RAW
privileged: true
```

---

## 📚 Bibliografia i Zasoby

### Materiały Edukacyjne

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [RFC 793 - TCP Protocol](https://tools.ietf.org/html/rfc793)


---

<div align="center">



</div>
