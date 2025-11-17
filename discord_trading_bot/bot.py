import discord
from discord.ext import commands, tasks
import os
import json
from datetime import datetime, time
import pytz

# Configurazione Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ID del canale dove inviare i tips
CHANNEL_ID = 1388574640666050692

# Fuso orario italiano
ITALY_TZ = pytz.timezone('Europe/Rome')

# Database tips (verrà caricato da file JSON)
tips_data = {
    "current_tip": 0,
    "tips": []
}

# 100 Trading Tips
TRADING_TIPS = [
    # SETTIMANA 1: Fondamenti del Trading (1-7)
    "**Tip #1 - Cos'è il Trading**\n\nIl trading è l'acquisto e la vendita di strumenti finanziari (forex, azioni, oro, ecc.) con l'obiettivo di generare profitti dalle variazioni di prezzo. Non è un gioco d'azzardo: richiede strategia, disciplina e gestione del rischio.",
    
    "**Tip #2 - Capitale di Rischio**\n\nOpera SOLO con denaro che puoi permetterti di perdere. Mai usare soldi necessari per vivere, pagare bollette o emergenze. Il trading comporta rischi reali e puoi perdere il tuo investimento.",
    
    "**Tip #3 - Demo Account Prima**\n\nPrima di investire denaro reale, fai pratica con un account demo per almeno 2-3 mesi. Impara a usare la piattaforma, testa le strategie e comprendi le dinamiche del mercato senza rischiare capitale.",
    
    "**Tip #4 - Timeframe e Stili**\n\nEsistono diversi stili di trading: scalping (minuti), day trading (ore), swing trading (giorni), position trading (settimane/mesi). Scegli quello che si adatta al tuo tempo disponibile e alla tua personalità.",
    
    "**Tip #5 - Leva Finanziaria**\n\nLa leva amplifica sia i guadagni che le perdite. Una leva 1:100 significa che con 100€ puoi controllare 10.000€. Usa leve basse all'inizio (max 1:10) per limitare i rischi.",
    
    "**Tip #6 - Spread e Commissioni**\n\nLo spread è la differenza tra prezzo di acquisto (ask) e vendita (bid). È il costo principale nel forex. Broker diversi hanno spread diversi: confrontali prima di scegliere. Spread bassi = costi minori.",
    
    "**Tip #7 - Orari di Mercato**\n\nIl forex è aperto 24/5. Le sessioni principali sono: Tokyo (2-11), Londra (9-18), New York (14-23, ora italiana). I momenti di maggior volatilità sono quando si sovrappongono (es. Londra-New York 14-18).",
    
    # SETTIMANA 2: Risk Management Base (8-14)
    "**Tip #8 - La Regola d'Oro**\n\nMai rischiare più del 1-2% del tuo capitale totale per singolo trade. Se hai 1000€, rischia max 10-20€ per trade. Questo ti permette di sopravvivere a serie di perdite consecutive.",
    
    "**Tip #9 - Stop Loss Obbligatorio**\n\nOGNI trade deve avere uno Stop Loss impostato PRIMA di entrare. È il punto dove chiudi automaticamente in perdita per limitare i danni. Mai fare trading senza Stop Loss, MAI.",
    
    "**Tip #10 - Take Profit**\n\nCome lo Stop Loss, imposta sempre un Take Profit: il livello dove vuoi chiudere in guadagno. Questo ti aiuta a prendere profitti senza avidità e a seguire il tuo piano di trading.",
    
    "**Tip #11 - Risk/Reward Ratio**\n\nIl rapporto rischio/rendimento indica quanto guadagni vs quanto rischi. Un R:R di 1:2 significa che rischi 10€ per guadagnarne 20. Cerca sempre R:R minimo 1:2, meglio 1:3.",
    
    "**Tip #12 - Position Sizing**\n\nCalcola sempre la dimensione della posizione (lot size) in base al tuo Stop Loss e al capitale che vuoi rischiare. Usa calcolatori online per non sbagliare i calcoli.",
    
    "**Tip #13 - Diversificazione**\n\nNon mettere tutti i soldi su un solo asset o su un solo trade. Diversifica tra coppie diverse (EUR/USD, GOLD, GBP/JPY) per ridurre il rischio complessivo del portafoglio.",
    
    "**Tip #14 - Trailing Stop**\n\nQuando un trade va in profitto, puoi usare un Trailing Stop: uno Stop Loss che si muove con il prezzo per proteggere i guadagni. Se il prezzo inverte, chiudi con profitto invece di tornare in perdita.",
    
    # SETTIMANA 3: Analisi Tecnica Base (15-21)
    "**Tip #15 - Supporti e Resistenze**\n\nSupporto: livello dove il prezzo tende a rimbalzare verso l'alto. Resistenza: livello dove il prezzo tende a rimbalzare verso il basso. Sono le fondamenta dell'analisi tecnica.",
    
    "**Tip #16 - Trendline**\n\nCollega almeno 2 minimi crescenti per una trendline rialzista, o 2 massimi decrescenti per una ribassista. Il prezzo tende a rispettare queste linee: rotture sono segnali importanti.",
    
    "**Tip #17 - Trend è Tuo Amico**\n\n\"The trend is your friend\" - fare trading nella direzione del trend aumenta le probabilità di successo. Identifica il trend principale e cerca entrate nella sua direzione.",
    
    "**Tip #18 - Candele Giapponesi**\n\nLe candele mostrano apertura, chiusura, massimo e minimo. Verde/bianca = rialzo, rossa/nera = ribasso. Impara i pattern base: doji, hammer, engulfing, shooting star.",
    
    "**Tip #19 - Medie Mobili (MA)**\n\nLe Moving Average smoothano il prezzo. MA50 e MA200 sono le più usate. Quando il prezzo è sopra la MA = uptrend, sotto = downtrend. L'incrocio MA50/MA200 è un segnale potente.",
    
    "**Tip #20 - RSI (Relative Strength Index)**\n\nL'RSI misura la forza del movimento. Valori: 0-100. Sopra 70 = ipercomprato (possibile discesa), sotto 30 = ipervenduto (possibile salita). Attenzione: può rimanere estremo in trend forti.",
    
    "**Tip #21 - MACD**\n\nIl MACD mostra momentum e direzione. È composto da 2 linee e un istogramma. Quando la linea MACD incrocia sopra la Signal line = segnale rialzista, sotto = ribassista.",
    
    # SETTIMANA 4: Pattern e Strategie (22-28)
    "**Tip #22 - Breakout Trading**\n\nUn breakout avviene quando il prezzo rompe un supporto/resistenza importante con volume. È un segnale forte di continuazione. Attendi conferma per evitare falsi breakout.",
    
    "**Tip #23 - Pullback Strategy**\n\nDopo un breakout, il prezzo spesso ritorna (pullback) a testare il livello rotto prima di continuare. Questa è un'ottima opportunità di entrata a rischio ridotto.",
    
    "**Tip #24 - Double Top/Bottom**\n\nDouble Top: due massimi allo stesso livello = pattern ribassista. Double Bottom: due minimi allo stesso livello = pattern rialzista. Conferma con rottura del neckline.",
    
    "**Tip #25 - Head & Shoulders**\n\nPattern di inversione: tre picchi, quello centrale più alto. La rottura della neckline conferma l'inversione trend. Inverse H&S è la versione rialzista.",
    
    "**Tip #26 - Triangoli**\n\nTriangoli ascendenti (rialzisti), discendenti (ribassisti), simmetrici (continuazione). Il prezzo si comprime tra le trendlines fino al breakout. Volume deve aumentare alla rottura.",
    
    "**Tip #27 - Flag e Pennant**\n\nPattern di continuazione dopo un movimento forte. La consolidazione (flag/pennant) è seguita da continuazione nella direzione originale. Ottimi per entry durante trend forti.",
    
    "**Tip #28 - Volume Analysis**\n\nIl volume conferma i movimenti. Breakout con alto volume = più affidabile. Movimento senza volume = debole. Volume crescente in trend = forza, volume in diminuzione = possibile inversione.",
    
    # SETTIMANA 5: Indicatori Avanzati (29-35)
    "**Tip #29 - Bollinger Bands**\n\nLe bande misurano la volatilità. Il prezzo si muove dentro le bande nel 95% dei casi. Quando tocca la banda superiore = possibile ipercomprato, banda inferiore = ipervenduto.",
    
    "**Tip #30 - Fibonacci Retracement**\n\nLivelli chiave: 38.2%, 50%, 61.8%. Dopo un movimento, il prezzo spesso ritraccia a questi livelli prima di continuare. Usali per identificare zone di supporto/resistenza dinamiche.",
    
    "**Tip #31 - Stocastico**\n\nOscillatore che mostra momentum. Due linee (%K e %D) che oscillano 0-100. Sopra 80 = ipercomprato, sotto 20 = ipervenduto. Incroci delle linee danno segnali di entrata/uscita.",
    
    "**Tip #32 - ATR (Average True Range)**\n\nL'ATR misura la volatilità media. Più è alto, più il mercato è volatile. Usalo per impostare Stop Loss appropriati: in alta volatilità usa Stop più larghi.",
    
    "**Tip #33 - Parabolic SAR**\n\nPunti sopra/sotto le candele. Quando sono sotto = trend rialzista, sopra = ribassista. Il cambio di posizione dei punti segnala possibili inversioni di trend.",
    
    "**Tip #34 - Ichimoku Cloud**\n\nSistema completo con cloud, tenkan, kijun. Prezzo sopra cloud = rialzo forte, sotto = ribasso forte. Cloud fornisce supporto/resistenza dinamica. Complesso ma molto potente.",
    
    "**Tip #35 - Volume Profile**\n\nMostra dove è stato scambiato più volume a determinati livelli di prezzo. Il POC (Point of Control) è il livello con più volume = zona importante di supporto/resistenza.",
    
    # SETTIMANA 6: Psicologia del Trading (36-42)
    "**Tip #36 - Controllo Emotivo**\n\nLe emozioni sono il peggior nemico del trader. Paura e avidità portano a decisioni sbagliate. Segui sempre il tuo piano di trading, non le emozioni del momento.",
    
    "**Tip #37 - Accetta le Perdite**\n\nLe perdite sono PARTE del trading. Anche i trader migliori perdono 40-50% dei trade. L'importante è che i guadagni siano maggiori delle perdite. Non cercare la perfezione.",
    
    "**Tip #38 - No Revenge Trading**\n\nDopo una perdita, mai cercare subito vendetta aprendo trade impulsivi per recuperare. Questo porta a perdite maggiori. Fai una pausa, analizza l'errore, torna calmo.",
    
    "**Tip #39 - Overtrading**\n\nFare troppi trade (overtrading) per noia o ansia aumenta commissioni e rischi. Qualità > quantità. Aspetta i setup migliori, non forzare le entrate.",
    
    "**Tip #40 - FOMO (Fear Of Missing Out)**\n\nVedere un movimento forte e voler entrare per paura di perdere l'opportunità porta a entrate nel momento peggiore. Le opportunità tornano sempre, non inseguire il mercato.",
    
    "**Tip #41 - Confirmation Bias**\n\nCercare solo informazioni che confermano la tua idea è pericoloso. Analizza sempre anche gli scenari contrari alla tua posizione. Sii obiettivo, non emotivo.",
    
    "**Tip #42 - Disciplina e Routine**\n\nCrea una routine giornaliera: analisi pre-market, review dei trade, studio. La disciplina distingue i trader profittevoli da quelli che perdono. Trading è un business, trattalo come tale.",
    
    # SETTIMANA 7: Money Management Avanzato (43-49)
    "**Tip #43 - Kelly Criterion**\n\nFormula matematica per calcolare la size ottimale: (Win Rate * Avg Win - Avg Loss) / Avg Win. Usa una frazione del risultato (es. 25%) per essere conservativo.",
    
    "**Tip #44 - Drawdown Management**\n\nIl drawdown è la perdita dal picco massimo. Se il tuo capitale scende del 20%, devi guadagnare 25% per recuperare. Limita il drawdown massimo al 20% del capitale.",
    
    "**Tip #45 - Scaling In/Out**\n\nEntra in posizione gradualmente (3 lotti invece di 1 grande) per ridurre il rischio. Esci gradualmente per massimizzare profitti: chiudi 50% al primo TP, lascia correre il resto.",
    
    "**Tip #46 - Correlazione Tra Asset**\n\nAlcune coppie sono correlate (EUR/USD e GBP/USD si muovono simili). Aprire trade su coppie correlate moltiplica il rischio senza diversificare. Attento alle correlazioni nascoste.",
    
    "**Tip #47 - Compounding**\n\nReinvestire i profitti aumenta esponenzialmente i guadagni nel tempo. Il 2% mensile composto = 26.8% annuo. Ma compounding funziona anche al contrario con le perdite: proteggi il capitale!",
    
    "**Tip #48 - Swap e Overnight**\n\nTenere posizioni aperte oltre le 00:00 (ora server) comporta costi/guadagni di swap (interessi). Coppie con carry trade positivo pagano swap positivo, altre negativo. Controlla prima di fare swing trading.",
    
    "**Tip #49 - Margin Call**\n\nSe le perdite erodono troppo il margine disponibile, il broker chiude automaticamente le posizioni (margin call). Usa sempre Stop Loss per evitarlo e non sfruttare mai il margine al 100%.",
    
    # SETTIMANA 8: Trading Plan e Strategia (50-56)
    "**Tip #50 - Trading Plan Scritto**\n\nOgni trader deve avere un piano scritto: strategia, risk management, obiettivi, regole. Senza piano stai giocando d'azzardo. Il piano ti guida nelle decisioni e mantiene disciplina.",
    
    "**Tip #51 - Backtesting**\n\nTesta la tua strategia su dati storici prima di usarla con soldi veri. Quanto avrebbe guadagnato/perso negli ultimi 2-3 anni? Il backtesting rivela punti deboli e valida le strategie.",
    
    "**Tip #52 - Forward Testing**\n\nDopo il backtesting, testa la strategia in demo per 2-3 mesi in condizioni reali di mercato. Solo se funziona in forward testing, passa al conto reale con capitale ridotto.",
    
    "**Tip #53 - Trading Journal**\n\nRegistra OGNI trade: entry, exit, motivo, emozioni, risultato. Rivedi il journal settimanalmente. Imparerai dai tuoi errori e migliorerai costantemente. Il journal è oro puro.",
    
    "**Tip #54 - Win Rate vs Profit Factor**\n\nWin Rate = % trade vincenti. Profit Factor = guadagni totali / perdite totali. Puoi essere profittevole con 40% win rate se i guadagni sono molto maggiori delle perdite (R:R alto).",
    
    "**Tip #55 - Expectancy**\n\nL'expectancy indica quanto guadagni in media per trade. Formula: (Win Rate × Avg Win) - (Loss Rate × Avg Loss). Se positiva, la strategia è profittevole nel lungo periodo.",
    
    "**Tip #56 - Adatta la Strategia**\n\nUna strategia che funziona in trend potrebbe fallire in range. Una che funziona in alta volatilità fallisce in bassa. Impara a riconoscere il contesto di mercato e adatta l'approccio.",
    
    # SETTIMANA 9: Analisi Fondamentale (57-63)
    "**Tip #57 - News Trading**\n\nEventi economici (NFP, decisioni banche centrali, PIL) muovono fortemente i mercati. Controlla il calendario economico. I principianti dovrebbero evitare di fare trading durante news ad alto impatto.",
    
    "**Tip #58 - Tassi di Interesse**\n\nI tassi di interesse delle banche centrali influenzano le valute. Tassi più alti = valuta più forte (attrae investimenti). Le decisioni di FED, BCE, BoE sono cruciali per forex.",
    
    "**Tip #59 - Inflazione (CPI)**\n\nL'inflazione misura l'aumento dei prezzi. Alta inflazione porta le banche centrali ad alzare i tassi. I dati CPI (Consumer Price Index) sono tra i più importanti per forex.",
    
    "**Tip #60 - NFP (Non-Farm Payrolls)**\n\nIl report occupazionale USA esce il primo venerdì del mese. Mostra i nuovi posti di lavoro creati. È uno degli eventi più volatili: il prezzo può muoversi di 100+ pips in minuti.",
    
    "**Tip #61 - PMI e GDP**\n\nPMI (Purchasing Managers Index) misura la salute manifatturiera. GDP (Gross Domestic Product) misura la crescita economica. Valori alti = economia forte = valuta forte.",
    
    "**Tip #62 - Geopolitica**\n\nGuerre, elezioni, crisi politiche muovono i mercati. Brexit, guerre commerciali USA-Cina, conflitti in Medio Oriente hanno impatto forte su forex e oro. Seguire le news globali è importante.",
    
    "**Tip #63 - Risk On / Risk Off**\n\nIn periodi \"risk on\" (ottimismo), investitori comprano asset rischiosi (azioni, valute emergenti). In \"risk off\" (paura), comprano asset rifugio (USD, JPY, oro). Riconosci il sentiment di mercato.",
    
    # SETTIMANA 10: Trading Specifico Forex (64-70)
    "**Tip #64 - Majors vs Minors**\n\nMajors: coppie con USD (EUR/USD, GBP/USD, USD/JPY) - più liquidità, spread bassi. Minors: senza USD (EUR/GBP, AUD/NZD) - meno liquide, spread più alti. Inizia con le majors.",
    
    "**Tip #65 - EUR/USD Caratteristiche**\n\nLa coppia più scambiata al mondo. Più liquida, spread bassissimo. Influenzata da FED e BCE. Buona per principianti. Movimenti meno estremi rispetto ad altre coppie.",
    
    "**Tip #66 - GBP/USD (Cable)**\n\nVolatile, movimenti ampi. Influenzata da BoE (Bank of England) e notizie UK. Attenzione durante sessione di Londra. Spread più ampi di EUR/USD. Richiede Stop Loss più larghi.",
    
    "**Tip #67 - USD/JPY**\n\nInfluenzata da avversione al rischio (JPY è valuta rifugio). In periodi di paura, JPY si rafforza. Correlata al Nikkei e Treasury USA. Movimenti smooth, buona per trend following.",
    
    "**Tip #68 - Commodity Currencies**\n\nAUD, NZD, CAD sono legate a materie prime. AUD/USD correlato a prezzi oro/ferro. USD/CAD correlato inversamente al petrolio. Segui i prezzi delle commodity per trading migliore.",
    
    "**Tip #69 - Exotic Pairs**\n\nCoppie con valute emergenti (USD/TRY, EUR/ZAR). Altamente volatili, spread enormi, bassa liquidità. Sconsigliato per principianti. Rischio molto alto ma anche opportunità.",
    
    "**Tip #70 - Carry Trade**\n\nStrategia che sfrutta la differenza di tassi d'interesse tra valute. Compri valuta ad alto tasso, vendi a basso tasso. Guadagni lo swap positivo. Funziona in mercati stabili, pericoloso in alta volatilità.",
    
    # SETTIMANA 11: Gold Trading (71-77)
    "**Tip #71 - Gold (XAU/USD) Basics**\n\nL'oro è quotato in USD per oncia. Asset rifugio: sale in periodi di crisi, incertezza, alta inflazione. Correlazione negativa con USD: dollaro debole = oro forte (solitamente).",
    
    "**Tip #72 - Volatilità Gold**\n\nL'oro è molto più volatile del forex. Movimenti di $20-50 al giorno sono normali. Usa Stop Loss più ampi ma position sizing ridotto per compensare la volatilità.",
    
    "**Tip #73 - Gold e Tassi Reali**\n\nL'oro è influenzato dai tassi d'interesse reali (tasso nominale - inflazione). Tassi reali negativi = oro sale. Segui le decisioni FED e i dati inflazione per tradare oro.",
    
    "**Tip #74 - Gold e DXY**\n\nDXY (Dollar Index) misura la forza del dollaro vs un paniere di valute. Correlazione inversa con oro: DXY sale = oro scende (di solito). Monitora DXY per trading oro migliore.",
    
    "**Tip #75 - Orari Migliori Gold**\n\nGold è più attivo durante sessione USA (14-23 ora italiana) e overlap Londra-NY (14-18). Movimenti forti durante apertura NYSE (15:30). Evita ore asiatiche se cerchi volatilità.",
    
    "**Tip #76 - Gold e Geopolitica**\n\nGuerre, tensioni, crisi sanitarie spingono gli investitori verso l'oro (bene rifugio). COVID-19, guerre in Ucraina/Medio Oriente hanno portato oro a massimi storici. News geopolitiche = opportunità gold.",
    
    "**Tip #77 - Gold Range vs Trend**\n\nL'oro alterna fasi di trend forte a fasi di consolidamento (range). Identifica il contesto: in trend usa breakout/trend following, in range usa supporti/resistenze e mean reversion.",
    
    # SETTIMANA 12: Strumenti e Piattaforme (78-84)
    "**Tip #78 - MetaTrader 4/5**\n\nLe piattaforme più usate per forex/CFD. MT4 è semplice e stabile, MT5 più avanzata con più timeframe e indicatori. Impara a usarle bene: template, indicatori custom, alert.",
    
    "**Tip #79 - TradingView**\n\nLa migliore piattaforma per analisi grafica. Grafici puliti, tantissimi indicatori, community, Pine Script per indicatori custom. Usala per analisi, poi esegui su MT4/MT5.",
    
    "**Tip #80 - VPS per Trading**\n\nUn VPS (Virtual Private Server) tiene la piattaforma sempre online 24/7. Essenziale per EA (Expert Advisors), copy trading, o se hai connessione instabile. Costo: €10-30/mese.",
    
    "**Tip #81 - Scelta del Broker**\n\nScegli broker regolamentati (CySEC, FCA, ASIC). Verifica: spread, commissioni, velocità esecuzione, supporto. Leggi recensioni reali. Evita broker con bonus troppo alti (spesso truffa).",
    
    "**Tip #82 - ECN vs Market Maker**\n\nECN broker: spread variabile, commissioni, esecuzione diretta al mercato. Market Maker: spread fisso, nessuna commissione, broker controparte. ECN è migliore per trader seri.",
    
    "**Tip #83 - Slippage**\n\nLo slippage è quando il tuo ordine viene eseguito a prezzo diverso da quello richiesto. Succede in alta volatilità (news) o bassa liquidità. Usa ordini limit per controllare il prezzo.",
    
    "**Tip #84 - Copy Trading**\n\nCopiare altri trader può essere utile per imparare, ma non è soluzione magica. Molti \"guru\" falliscono. Se copi, studia la strategia del trader, il suo drawdown, e usa capitale ridotto inizialmente.",
    
    # SETTIMANA 13: Errori Comuni (85-91)
    "**Tip #85 - Errore: No Stop Loss**\n\nIl più grave. \"Spero che risalga\" mentre la perdita cresce. Risultato: blown account. SEMPRE Stop Loss, SEMPRE. Nessuna eccezione. È la differenza tra trader e gambler.",
    
    "**Tip #86 - Errore: Overleverage**\n\nUsare leva 1:500 con tutto il margine per \"guadagnare veloce\". Bastano pochi pips contro e sei liquidato. Leva alta = account bruciato velocemente. Usa max 1:20, meglio 1:10.",
    
    "**Tip #87 - Errore: Trading News Senza Esperienza**\n\nEntrare durante NFP o FED senza esperienza è suicidio. Spread si allarga, slippage enorme, movimenti violenti. Aspetta 30 minuti dopo la news prima di entrare.",
    
    "**Tip #88 - Errore: Martingala**\n\nRaddoppiare la size dopo ogni perdita per recuperare. Sembra funzionare finché non arriva una serie di 5-6 perdite consecutive: account azzerato. MAI usare martingala.",
    
    "**Tip #89 - Errore: Cambiare Strategia Spesso**\n\nProvare una strategia per 1 settimana, poi cambiarla. Risultato: nessuna strategia viene testata abbastanza. Scegli una strategia e seguila per almeno 3 mesi prima di giudicare.",
    
    "**Tip #90 - Errore: Trading per Noia**\n\nAprire trade perché non succede niente, per \"fare qualcosa\". Il mercato non paga lo stipendio orario. Meglio 0 trade che 1 trade forzato. Aspetta i setup migliori.",
    
    "**Tip #91 - Errore: Ignorare le Commissioni**\n\nSpread, swap, commissioni sembrano piccoli ma si accumulano. Fare 10 trade al giorno su EUR/USD con 2 pip spread = 20 pip persi solo in spread. Conta i costi reali.",
    
    # SETTIMANA 14: Mindset Vincente (92-98)
    "**Tip #92 - Pazienza è Profitto**\n\nI trader migliori fanno pochi trade di qualità, non tanti trade a caso. Aspettare il setup perfetto è più profittevole che fare 10 trade mediocri. Pazienza = denaro.",
    
    "**Tip #93 - Focus sul Processo**\n\nNon fissarti sul P&L (profitto/perdita). Concentrati sul processo: seguire il piano, gestire il rischio, migliorare l'analisi. I profitti sono CONSEGUENZA del processo corretto.",
    
    "**Tip #94 - Formazione Continua**\n\nIl mercato evolve, tu devi evolvere. Leggi libri, segui trader esperti, analizza i tuoi trade. Chi smette di imparare, smette di guadagnare. Dedica 30 min/giorno allo studio.",
    
    "**Tip #95 - Aspettative Realistiche**\n\nTrading non è \"diventa milionario in 1 mese\". Profitti realistici: 2-5% mensile è eccellente. 10% è straordinario. Chi promette 50-100% mensile mente o si sta bruciando l'account.",
    
    "**Tip #96 - Gestire i Periodi di Perdita**\n\nAnche i migliori trader hanno settimane/mesi negativi. È normale. Non andare in panico. Rivedi il piano, riduci temporaneamente il rischio, riprendi quando torni in forma mentale.",
    
    "**Tip #97 - Ogni Trade è Indipendente**\n\nHai fatto 5 trade vincenti? Il prossimo può essere perdente. Hai perso 3 trade? Il prossimo può essere vincente. Ogni trade è una nuova storia. Non lasciare che i risultati passati influenzino il presente.",
    
    "**Tip #98 - Trading è Maratona**\n\nNon sprint. Costruire capitale richiede tempo, pazienza, disciplina. Non cercare colpi da 1000%, proteggi il capitale e cresci costantemente. In 2-3 anni con 3% mensile raddoppi l'account.",
    
    # ULTIMI 2 TIPS: Call to Action (99-100)
    "**Tip #99 - La Regola 90/90/90**\n\nStatistica dura ma reale: 90% dei trader perde 90% del capitale nei primi 90 giorni. Perché? No piano, no risk management, emozioni. Tu puoi essere nel 10% che sopravvive: studia, pratica, disciplina.",
    
    "**Tip #100 - Il Tuo Viaggio Inizia Ora**\n\n🎓 Hai completato i 100 tips! Ora conosci le basi del trading. Ma la teoria è solo l'inizio. Pratica su demo, crea il tuo piano, studia il mercato ogni giorno. Il successo richiede tempo e dedizione.\n\n💎 Vuoi approfondire? Scopri i nostri servizi NovaQore FX: segnali gold, copytrading, indicatori professionali e supporto della community.\n\n🚀 Ricorda: il mercato è sempre lì. Non avere fretta. Costruisci le fondamenta solide e i profitti arriveranno.\n\n**Welcome to the Nova Family! 🌟**"
]

def load_progress():
    """Carica il progresso dal file JSON"""
    try:
        if os.path.exists('tips_progress.json'):
            with open('tips_progress.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('current_tip', 0)
    except Exception as e:
        print(f"Errore caricamento progresso: {e}")
    return 0

def save_progress(tip_number):
    """Salva il progresso nel file JSON"""
    try:
        with open('tips_progress.json', 'w', encoding='utf-8') as f:
            json.dump({'current_tip': tip_number}, f)
    except Exception as e:
        print(f"Errore salvataggio progresso: {e}")

@bot.event
async def on_ready():
    print(f'Bot connesso come {bot.user}')
    print(f'Canale target: {CHANNEL_ID}')
    
    # Carica il progresso salvato
    current = load_progress()
    print(f'Progresso caricato: Tip #{current}')
    
    # Avvia il task di invio giornaliero
    if not daily_tip.is_running():
        daily_tip.start()
    
    print('Bot pronto! Tips verranno inviati ogni giorno alle 09:00 (Italy)')

@tasks.loop(time=time(hour=7, minute=0))  # 9:00 AM ora italiana = 7:00 UTC
async def daily_tip():
    """Invia un tip al giorno automaticamente"""
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Errore: Canale {CHANNEL_ID} non trovato!")
        return
    
    # Carica progresso
    current_tip = load_progress()
    
    # Se abbiamo finito tutti i tips, ricomincia
    if current_tip >= len(TRADING_TIPS):
        current_tip = 0
        await channel.send("🔄 **Abbiamo completato tutti i 100 tips! Ricominciamo dal primo!**")
    
    # Invia il tip
    tip_message = TRADING_TIPS[current_tip]
    
    # Crea un embed bello per il tip
    embed = discord.Embed(
        title=f"📊 Trading Tip of the Day",
        description=tip_message,
        color=0x00ff00,
        timestamp=datetime.now(ITALY_TZ)
    )
    embed.set_footer(text="NovaQore FX • Tips giornalieri per trader", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    
    await channel.send(embed=embed)
    
    # Salva progresso
    current_tip += 1
    save_progress(current_tip)
    
    print(f"✅ Tip #{current_tip} inviato con successo!")

# COMANDI MANUALI
@bot.command(name='next')
async def next_tip(ctx):
    """Invia il prossimo tip manualmente"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    current_tip = load_progress()
    
    if current_tip >= len(TRADING_TIPS):
        await ctx.send("✅ Hai già ricevuto tutti i 100 tips! Aspetta il reset automatico.")
        return
    
    tip_message = TRADING_TIPS[current_tip]
    
    embed = discord.Embed(
        title=f"📊 Trading Tip #{current_tip + 1}",
        description=tip_message,
        color=0x00ff00,
        timestamp=datetime.now(ITALY_TZ)
    )
    embed.set_footer(text="NovaQore FX • Tip manuale")
    
    await ctx.send(embed=embed)
    
    current_tip += 1
    save_progress(current_tip)

@bot.command(name='random')
async def random_tip(ctx):
    """Invia un tip casuale"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    import random
    tip = random.choice(TRADING_TIPS)
    
    embed = discord.Embed(
        title="🎲 Random Trading Tip",
        description=tip,
        color=0xffaa00,
        timestamp=datetime.now(ITALY_TZ)
    )
    embed.set_footer(text="NovaQore FX • Tip casuale")
    
    await ctx.send(embed=embed)

@bot.command(name='progress')
async def show_progress(ctx):
    """Mostra il progresso dei tips"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    current_tip = load_progress()
    total_tips = len(TRADING_TIPS)
    percentage = (current_tip / total_tips) * 100
    
    embed = discord.Embed(
        title="📈 Progresso Tips",
        description=f"**Tips completati:** {current_tip}/{total_tips}\n**Percentuale:** {percentage:.1f}%\n\n{'█' * int(percentage/5)}{' ' * (20-int(percentage/5))} {percentage:.1f}%",
        color=0x0099ff
    )
    
    await ctx.send(embed=embed)

@bot.command(name='reset')
@commands.has_permissions(administrator=True)
async def reset_progress(ctx):
    """Reset del progresso (solo admin)"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    save_progress(0)
    await ctx.send("🔄 **Progresso resettato!** Il prossimo tip sarà il #1.")

@bot.command(name='pause')
@commands.has_permissions(administrator=True)
async def pause_tips(ctx):
    """Mette in pausa l'invio automatico"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    if daily_tip.is_running():
        daily_tip.cancel()
        await ctx.send("⏸️ **Tips in pausa.** Usa `!resume` per riattivare.")
    else:
        await ctx.send("ℹ️ I tips sono già in pausa.")

@bot.command(name='resume')
@commands.has_permissions(administrator=True)
async def resume_tips(ctx):
    """Riprende l'invio automatico"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    if not daily_tip.is_running():
        daily_tip.start()
        await ctx.send("▶️ **Tips riattivati!** Prossimo invio: domani alle 09:00.")
    else:
        await ctx.send("ℹ️ I tips sono già attivi.")

@bot.command(name='help')
async def help_command(ctx):
    """Mostra tutti i comandi disponibili"""
    if ctx.channel.id != CHANNEL_ID:
        return
    
    embed = discord.Embed(
        title="🤖 Comandi Bot Trading Tips",
        description="Ecco tutti i comandi disponibili:",
        color=0x9b59b6
    )
    
    embed.add_field(
        name="📚 Comandi Pubblici",
        value="`!next` - Ricevi il prossimo tip\n`!random` - Ricevi un tip casuale\n`!progress` - Vedi il tuo progresso\n`!help` - Questo messaggio",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Comandi Admin",
        value="`!reset` - Reset progresso\n`!pause` - Pausa invio automatico\n`!resume` - Riprendi invio automatico",
        inline=False
    )
    
    embed.set_footer(text="NovaQore FX Trading Bot")
    
    await ctx.send(embed=embed)

# Avvia il bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN', 'MTQ0MDA2OTkwMjM2MTgyMTIyNA.G9eObd.69yT7PhahWnwicUc_h78wbKJ0nvb8c5jo286TE')
    bot.run(TOKEN)
