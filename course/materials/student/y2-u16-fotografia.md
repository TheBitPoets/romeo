# Secondo anno 16. Fotografia REST

## Obiettivo

In questa unità imparerai a ricevere JPEG con media type corretto.

## Che cosa sai già

Conosci REST, TestClient, JSON, byte JPEG e CameraService mock.

## Modello mentale

Una foto REST è una risorsa binaria: la response contiene byte JPEG invece di JSON. Status e Content-Type dicono al client se e come interpretarla. `create_app(camera=mock)` passa alla app una camera prevedibile; questa iniezione evita hardware reale durante il test.

## Esempio minimo commentato

```python
with TestClient(create_app(camera=MockCameraService())) as client:
    response = client.get("/api/camera/photo")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
```

Solo dopo questi controlli usiamo `response.content` come JPEG.

## Prova guidata

1. Confronta una response JSON e una JPEG.
2. Individua dove il mock viene passato alla app.
3. Richiedi la foto e controlla lo status.
4. Controlla Content-Type e marker JPEG.
5. Simula camera indisponibile e verifica una risposta d'errore.

## Esercizio base

Valida status, media type e contenuto della foto mock.

## Esercizio intermedio

Salva i byte soltanto dopo la validazione e verifica che il file non sia vuoto.

## Mini-sfida

Definisci il comportamento REST per camera non disponibile, motivando status e body d'errore.

## Consegna valutata

Completa `download_photo` nello starter senza rinominare le funzioni. Rispetta parametri, valore restituito e cleanup descritti nella docstring: TheBitLab importerà le funzioni e le proverà con input diversi. Obiettivo: ricevere JPEG con media type corretto.

## Errori tipici

- Chiamare `.json()` su una foto.
- Accettare qualsiasi contenuto con status 200.
- Usare la camera reale nei test automatici.

## Autoverifica

- So distinguere response JSON e binaria?
- Controllo il Content-Type?
- Il test è ripetibile senza hardware?

## Accessibilità

L'esito della foto è descritto anche con testo, dimensione e status; nessuno deve essere ripreso per completare il laboratorio.

## Parole nuove

| Termine | Significato in questa lezione |
| --- | --- |
| `Content-Type` | header che descrive il formato del body |
| `iniezione` | passaggio esplicito di un collaboratore alla app |
| `binario` | dati composti da byte, non testo JSON |
