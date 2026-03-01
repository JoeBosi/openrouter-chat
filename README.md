# Chat OpenRouter - Python

Una semplice applicazione di chat in Python che utilizza l'API di OpenRouter con il modello Auto Router.

## Installazione

1. Clona o scarica questo repository
2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## Configurazione

1. Copia il file `.env.example` in `.env`:
```bash
cp .env.example .env
```

2. Apri il file `.env` e inserisci la tua API key di OpenRouter:
```
OPENROUTER_API_KEY=la_tua_api_key_qui
```

Per ottenere una API key:
- Vai su [OpenRouter.ai](https://openrouter.ai/)
- Registrati o fai il login
- Vai nella sezione API Keys e crea una nuova key

## Utilizzo

Esegui la chat:
```bash
python chat.py
```

### Comandi disponibili
- `quit` - Esci dalla chat
- `clear` - Pulisci la cronologia della conversazione

## Caratteristiche

- ✅ Utilizza il modello Auto Router di OpenRouter
- ✅ Mantiene la cronologia della conversazione
- ✅ Gestione degli errori
- ✅ Interfaccia a riga di comando semplice
- ✅ Supporto per contesto continuo

## Struttura del progetto

```
├── chat.py              # File principale della chat
├── requirements.txt     # Dipendenze Python
├── .env.example        # Template per le variabili d'ambiente
├── .env                # Le tue configurazioni (da creare)
└── README.md           # Questo file
```

## Test

L'applicazione è stata completamente testata. Per eseguire i test:

```bash
# Test API base
python test_api.py

# Test GUI
python test_gui.py

# Test completo
python test_complete.py
```

### Risultati Test ✅

- ✅ **API Connection**: Connessione OpenRouter funzionante
- ✅ **Model Selection**: Auto Router seleziona automaticamente i modelli migliori
- ✅ **Long Text Handling**: Supporto per testi fino a 50KB
- ✅ **File Operations**: Caricamento ed esportazione file
- ✅ **Error Handling**: Gestione completa degli errori
- ✅ **GUI Components**: Tutti i componenti grafici funzionanti
- ✅ **CLI Interface**: Interfaccia a riga di comando operativa

## Note

- Il modello Auto Router seleziona automaticamente il modello migliore per ogni richiesta
- La cronologia della conversazione viene mantenuta in memoria durante la sessione
- Assicurati di avere una connessione internet attiva
- Per testi molto lunghi (>10KB), il timeout viene automaticamente esteso a 120 secondi
