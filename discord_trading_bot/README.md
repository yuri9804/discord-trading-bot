# 🤖 NovaQore FX Trading Tips Bot

Bot Discord che invia automaticamente **100 tips sul trading** (forex, gold, risk management, psicologia) uno al giorno alle 9:00 AM.

## ✨ Funzionalità

### 📅 Invio Automatico
- **1 tip al giorno** alle 9:00 AM (ora italiana)
- **100 tips totali** che coprono tutte le basi del trading
- Ripartenza automatica dopo aver completato tutti i tips
- Sistema di salvataggio progresso (riprende da dove ha lasciato anche dopo riavvii)

### 🎮 Comandi Disponibili

**Comandi Pubblici:**
- `!next` - Ricevi il prossimo tip immediatamente (invece di aspettare)
- `!random` - Ricevi un tip casuale tra i 100
- `!progress` - Visualizza quanti tips hai già ricevuto (con barra progresso)
- `!help` - Lista di tutti i comandi

**Comandi Admin:**
- `!reset` - Resetta il progresso a 0 (ricomincia dal tip #1)
- `!pause` - Mette in pausa l'invio automatico giornaliero
- `!resume` - Riprende l'invio automatico

## 📚 Contenuto Tips

I 100 tips coprono:
- **Settimana 1-2:** Fondamenti del trading e risk management base
- **Settimana 3-4:** Analisi tecnica (supporti, resistenze, pattern, candele)
- **Settimana 5:** Indicatori avanzati (RSI, MACD, Bollinger, Fibonacci)
- **Settimana 6:** Psicologia del trading (emozioni, disciplina, FOMO)
- **Settimana 7-8:** Money management avanzato e trading plan
- **Settimana 9:** Analisi fondamentale (news, tassi, inflazione)
- **Settimana 10-11:** Trading specifico forex e gold
- **Settimana 12:** Strumenti e piattaforme (MT4/5, TradingView, VPS)
- **Settimana 13-14:** Errori comuni e mindset vincente

## 🚀 Deployment su Railway (GRATIS)

### 1. Crea Account Railway
- Vai su [railway.app](https://railway.app)
- Registrati con GitHub (gratis)

### 2. Deploy del Bot

**Opzione A: Deploy da GitHub (consigliato)**
1. Carica questi file su un tuo repository GitHub
2. Su Railway: "New Project" → "Deploy from GitHub repo"
3. Seleziona il repository
4. Railway farà tutto automaticamente

**Opzione B: Deploy diretto**
1. Su Railway: "New Project" → "Empty Project"
2. Clicca "+ New" → "GitHub Repo" (collega il repo)
3. Oppure usa Railway CLI (vedi sotto)

### 3. Configura le Variabili d'Ambiente

Su Railway, nel tuo progetto:
1. Vai su **"Variables"**
2. Aggiungi variabile:
   - **Key:** `DISCORD_TOKEN`
   - **Value:** Il tuo token Discord (quello NUOVO dopo il reset!)
3. Clicca "Add"

### 4. Verifica Deployment

- Il bot si avvierà automaticamente
- Controlla i logs su Railway per vedere se è online
- Dovresti vedere: `Bot connesso come [nome bot]`

## 🔧 Configurazione Avanzata

### Cambiare Orario Invio

Nel file `bot.py`, modifica questa riga:

```python
@tasks.loop(time=time(hour=7, minute=0))  # 9:00 AM ora italiana = 7:00 UTC
```

Esempi:
- `hour=6, minute=0` → 8:00 AM Italia
- `hour=9, minute=30` → 11:30 AM Italia
- `hour=16, minute=0` → 18:00 PM Italia

**Nota:** Railway usa fuso UTC, quindi sottrai 2 ore dall'orario italiano desiderato.

### Cambiare Canale Discord

Nel file `bot.py`, modifica:

```python
CHANNEL_ID = 1388574640666050692
```

Sostituisci con l'ID del tuo canale.

## 🐛 Troubleshooting

### Bot non invia tips
1. Verifica che il token sia corretto su Railway
2. Controlla che il bot abbia permessi "Send Messages" nel canale
3. Verifica che CHANNEL_ID sia corretto

### Bot offline
1. Controlla i logs su Railway per errori
2. Verifica che il piano Railway sia attivo (500 ore gratis/mese)
3. Riavvia il servizio su Railway

### Tips non salvano progresso
- Normal, Railway ha filesystem effimero. Il progresso si resetta se il container si riavvia.
- Per persistenza: aggiungi Railway PostgreSQL (più complesso, non necessario per uso base)

## 📊 Personalizzazione Tips

Per modificare i tips, edita l'array `TRADING_TIPS` nel file `bot.py`:

```python
TRADING_TIPS = [
    "**Tip #1 - Titolo**\n\nIl tuo contenuto qui...",
    "**Tip #2 - Altro Titolo**\n\nAltro contenuto...",
    # ... ecc
]
```

## 💡 Note Importanti

- Il bot **NON richiede** server dedicato o VPS
- Railway offre **500 ore gratis/mese** (più che sufficienti per un bot 24/7)
- Il bot si riavvia automaticamente se crasha
- I tips sono in **Italiano** e specifici per forex/gold trading

## 🔐 Sicurezza

- **MAI** condividere il token Discord pubblicamente
- Il token è salvato come variabile d'ambiente su Railway (sicuro)
- Se il token viene esposto, resettalo SUBITO dal Discord Developer Portal

## 📞 Supporto

Se hai problemi:
1. Controlla i logs su Railway
2. Verifica che Discord Developer Portal abbia i permessi corretti
3. Testa prima in locale con `python bot.py` (richiede Python installato)

---

**Creato per NovaQore FX** 🌟

Bot pronto all'uso per educare la community sui fondamenti del trading!
