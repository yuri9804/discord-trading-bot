# 🚀 GUIDA RAPIDA DEPLOYMENT - 5 MINUTI

## ✅ PREREQUISITI COMPLETATI
- ✓ Bot Discord creato
- ✓ Token copiato
- ✓ Bot invitato sul server
- ✓ ID canale: 1388574640666050692

## 📋 STEP 1: PREPARA I FILE

Hai già tutti i file pronti! Questi file:
```
discord_trading_bot/
├── bot.py              (codice principale)
├── requirements.txt    (dipendenze)
├── Procfile           (config Railway)
├── runtime.txt        (versione Python)
├── README.md          (documentazione)
└── .gitignore         (file da ignorare)
```

## 🌐 STEP 2: CARICA SU GITHUB

### Opzione A: Interfaccia Web GitHub
1. Vai su github.com
2. Clicca **"+"** in alto a destra → **"New repository"**
3. Nome: `discord-trading-bot` (o quello che vuoi)
4. **Pubblico** o **Privato** (entrambi ok)
5. Clicca **"Create repository"**

6. Nella pagina del repository:
   - Clicca **"uploading an existing file"**
   - Trascina TUTTI i file della cartella `discord_trading_bot`
   - Aggiungi messaggio: "Initial commit"
   - Clicca **"Commit changes"**

### Opzione B: Git da Terminale (se conosci Git)
```bash
cd discord_trading_bot
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/TUO_USERNAME/discord-trading-bot.git
git push -u origin main
```

## 🚂 STEP 3: DEPLOY SU RAILWAY

### 1. Crea Account Railway
- Vai su **https://railway.app**
- Clicca **"Login"** → **"Login with GitHub"**
- Autorizza Railway ad accedere ai tuoi repository

### 2. Nuovo Progetto
- Clicca **"New Project"**
- Seleziona **"Deploy from GitHub repo"**
- Cerca e seleziona il tuo repository `discord-trading-bot`
- Clicca sul repository per selezionarlo

### 3. Railway Inizia il Deploy Automatico
Railway legge il `Procfile` e installa tutto automaticamente!

### 4. Configura il Token (IMPORTANTE!)
Mentre Railway sta deployando:
1. Nel progetto Railway, clicca sulla **scheda del servizio**
2. Vai su **"Variables"**
3. Clicca **"+ New Variable"**
4. Aggiungi:
   - **Variable name:** `DISCORD_TOKEN`
   - **Value:** Incolla il tuo token Discord (quello NUOVO!)
5. Clicca **"Add"**

### 5. Riavvia il Servizio
- Torna alla scheda del servizio
- Clicca sui **3 puntini** (⋮) in alto a destra
- **"Restart"**

## 🎉 STEP 4: VERIFICA CHE FUNZIONI

### 1. Controlla i Logs
Su Railway:
- Vai sulla scheda del servizio
- Clicca **"Logs"**
- Dovresti vedere:
  ```
  Bot connesso come [nome bot]
  Canale target: 1388574640666050692
  Bot pronto! Tips verranno inviati ogni giorno alle 09:00 (Italy)
  ```

### 2. Testa su Discord
Nel tuo canale Discord, scrivi:
```
!help
```

Il bot dovrebbe rispondere con la lista comandi!

Poi prova:
```
!next
```

Per ricevere il primo tip immediatamente!

## ⏰ COMPORTAMENTO DEL BOT

- **Invio automatico:** Ogni giorno alle 9:00 AM (ora italiana)
- **Primo tip:** Domani mattina alle 9:00 (oppure usa `!next` per riceverlo subito)
- **Progresso:** Salvato automaticamente, anche se Railway riavvia il bot

## 🔧 COMANDI UTILI

Sul tuo Discord:
- `!next` → Tip successivo subito
- `!random` → Tip casuale
- `!progress` → Vedi progresso (es. 15/100 completati)
- `!help` → Lista comandi

Solo admin:
- `!pause` → Metti in pausa invio automatico
- `!resume` → Riattiva invio automatico
- `!reset` → Ricomincia da tip #1

## ❗ IMPORTANTE - SICUREZZA TOKEN

**DOPO aver configurato Railway, RESETTA il token:**

1. Vai su Discord Developer Portal
2. Sezione "Bot"
3. Clicca **"Reset Token"**
4. Copia il NUOVO token
5. Su Railway → Variables → Modifica `DISCORD_TOKEN` con il nuovo
6. Restart del servizio

Questo perché hai condiviso il token nella chat!

## 📊 RAILWAY - LIMITI GRATIS

Piano gratuito Railway:
- ✅ **500 ore/mese** di runtime (17 ore/giorno, più che sufficienti)
- ✅ **100 GB bandwidth**
- ✅ Riavvii automatici
- ✅ HTTPS e logs inclusi

Per un bot Discord semplice come questo, **il piano gratis è perfetto**!

## 🆘 PROBLEMI COMUNI

### Bot non risponde
1. Verifica logs Railway per errori
2. Controlla che il token sia corretto
3. Assicurati che il bot abbia permessi nel canale

### Bot offline
1. Controlla che Railway non abbia superato le 500 ore
2. Verifica che il servizio sia "running" su Railway
3. Riavvia il servizio

### Tips non arrivano alle 9:00
1. Controlla i logs all'orario previsto
2. Il bot potrebbe essere in pausa (`!resume` per riattivare)
3. Verifica che CHANNEL_ID sia corretto nel codice

## ✨ FATTO!

Il tuo bot è ora LIVE 24/7 su Railway, completamente gratis!

**Ogni giorno alle 9:00 AM**, il bot invierà automaticamente un nuovo tip di trading alla tua community Discord! 🎉

---

**Tempo totale:** ~5-10 minuti
**Costo:** €0 (Railway gratis)
**Manutenzione:** Zero, tutto automatico!
