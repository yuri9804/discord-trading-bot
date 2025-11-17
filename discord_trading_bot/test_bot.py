#!/usr/bin/env python3
"""
Test rapido per verificare che il bot funzioni prima del deployment
"""

import sys

print("🧪 Test Bot Discord Trading Tips\n")
print("=" * 50)

# Test 1: Import delle librerie
print("\n1️⃣ Test import librerie...")
try:
    import discord
    from discord.ext import commands, tasks
    import pytz
    print("✅ Tutte le librerie importate correttamente!")
except ImportError as e:
    print(f"❌ Errore import: {e}")
    print("\n💡 Installa le dipendenze con:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

# Test 2: Verifica configurazione
print("\n2️⃣ Test configurazione...")
try:
    from bot import TRADING_TIPS, CHANNEL_ID, ITALY_TZ
    print(f"✅ CHANNEL_ID configurato: {CHANNEL_ID}")
    print(f"✅ Fuso orario: {ITALY_TZ}")
    print(f"✅ Tips caricati: {len(TRADING_TIPS)} tips")
except Exception as e:
    print(f"❌ Errore configurazione: {e}")
    sys.exit(1)

# Test 3: Verifica tips
print("\n3️⃣ Test contenuto tips...")
if len(TRADING_TIPS) != 100:
    print(f"⚠️ Attenzione: Trovati {len(TRADING_TIPS)} tips invece di 100")
else:
    print("✅ Tutti i 100 tips sono presenti!")

# Mostra primi 3 tips come esempio
print("\n📝 Preview primi 3 tips:")
for i in range(min(3, len(TRADING_TIPS))):
    tip_preview = TRADING_TIPS[i][:100] + "..." if len(TRADING_TIPS[i]) > 100 else TRADING_TIPS[i]
    print(f"\n   Tip #{i+1}:")
    print(f"   {tip_preview}")

# Test 4: Verifica token
print("\n4️⃣ Test token Discord...")
import os
token = os.getenv('DISCORD_TOKEN')
if not token or token == 'your_token_here':
    print("⚠️ Token non configurato!")
    print("💡 Configura DISCORD_TOKEN su Railway prima del deployment")
else:
    print("✅ Token presente (controlla che sia valido su Discord)")

print("\n" + "=" * 50)
print("✨ Test completato!")
print("\n📋 Prossimi passi:")
print("   1. Carica i file su GitHub")
print("   2. Deploy su Railway")
print("   3. Configura DISCORD_TOKEN su Railway")
print("   4. Verifica i logs su Railway")
print("\n🚀 Il tuo bot è pronto per il deployment!")
