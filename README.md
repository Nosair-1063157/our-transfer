# our-transfer

Ik heb de applicatie Our Transfer ontwikkeld als een opdracht om opdracht 4 en 5 samen te voegen in 1 programma

Voor de implementatie van de symmetrisch encryptie heb ik gekozen voor AES-256 (Advanced Encryption Standard) via Fernet in de cryptography library

AES is wereldweid het standaard voor symmetetrisch encryptie en word gebruikt door grote organisaties en overheden, met een 256 bit sleutel is brute forcen bijna onmogelijk met de rekenkracht dat we hebben 

De sleutel wordt eenmalig gegenereerd met Fernet.generate.key en deze sleutel word lokaal opgeslagen, bij het starten van de applicatie wordt er gecontroleerd of dit bestand bestaat, zo ja wordt de bestaande sleutel gebruikt, zoniet of is de sleutel ermee getampert wordt er een automatisch sleutel gecreëerd

Het applicatie is ook Kerckhoffs Principe vriendelijk 
dat betekent dat de versleutelingssysteem veilig is, zelfs als alles openbaar is moet de sleutel zelf altijd geheim blijven
de keys worden alleen maar gegenereerd ook wanneer er geen bestaand geldige sleutel is


## Cybersecurity opdracht 4

Bestanden uploaden en versleutelen voor opslag
Delen via geëncrypteerde links met tijdelijke toegang
Implementatie van symmetrische (AES) en asymmetrische encryptie (RSA)
Checksum verificatie (SHA-256) voor bestandsintegriteit

## Cybersecurity opdracht 5 

Tekst versleutelen en ontsleutelen met symmetrische (AES) en asymmetrische (RSA) encryptie


## Installatiehandleiding

1. **Maak een venv aan**:

   ```bash
   python -m venv venv

   ```

2. **Venv activeren**:

   *Windows*
   ```bash
   venv/Scripts/activate
   ```
   *MacOS/ Linux*
    ```bash
   source venv/bin/activate
   ```
   *Windows met Bash*
    ```bash
   source venv/Scripts/activate
   ```

3. **Installeer afhankelijkheden**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Start de ontwikkelingsserver**:

   ```bash
   python app.py
   ```

5.  **Wij bevelen Python verise 3.13 aan**:
   ```bash
   python --version
   ```