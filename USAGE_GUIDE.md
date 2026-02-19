# 📚 Detaljno uputstvo za korišćenje

## 🎯 Brzi Start

### Windows korisnici:

1. **Instalacija:**
   - Dvoklik na `install.bat`
   - Sačekajte da se instaliraju svi paketi

2. **Pokretanje:**
   - Dvoklik na `run.bat`
   - Ili: Otvori Command Prompt i pokreni `python backup_gui.py`

### Linux/macOS korisnici:

```bash
# Instalacija
pip install -r requirements.txt

# Pokretanje
python3 backup_gui.py
```

## 🖥️ GUI Pregled

### Glavne Sekcije:

```
┌─────────────────────────────────────────┐
│     🗄️ Advanced Backup Tool           │
├─────────────────────────────────────────┤
│ Source Directory:                       │
│ [Path input field]        [Browse]      │
├─────────────────────────────────────────┤
│ Destination Directory:                  │
│ [Path input field]        [Browse]      │
├─────────────────────────────────────────┤
│ File Filters:                           │
│ Include: [.txt, .pdf, .docx]            │
│ Exclude: [.tmp, .log]                   │
├─────────────────────────────────────────┤
│ Scheduling:                             │
│ ☑ Enable Automatic Backup               │
│ ○ Daily  ○ Weekly  ○ Monthly            │
│ Time: [12:00]                           │
├─────────────────────────────────────────┤
│ Progress:                               │
│ [████████████████████░░░░] 80%          │
│ Backing up: document.pdf (40/50)        │
├─────────────────────────────────────────┤
│ [Start Backup]  [Cancel]                │
├─────────────────────────────────────────┤
│ Status Log:                             │
│ ✅ Backup completed successfully!       │
│    Files copied: 50                     │
│    Files skipped: 5                     │
└─────────────────────────────────────────┘
```

## 📖 Korak-po-Korak Primeri

### Primer 1: Osnovni Backup (Svi fajlovi)

**Cilj**: Backup kompletnog foldera sa dokumentima

**Koraci:**
1. Klikni **Browse** pored "Source Directory"
2. Izaberi folder: `C:\Users\YourName\Documents`
3. Klikni **Browse** pored "Destination Directory"
4. Izaberi folder: `D:\Backups\Documents_Backup`
5. Ostavi filtere **prazne** (biće backupovani svi fajlovi)
6. Klikni **Start Backup**

**Rezultat:**
- Svi fajlovi i podfolderi će biti kopirani
- Originalna struktura foldera će biti očuvana
- Status log će pokazati broj kopiranih fajlova

---

### Primer 2: Backup samo Office dokumenata

**Cilj**: Backup samo Word, Excel i PowerPoint fajlova

**Koraci:**
1. Source: `C:\Users\YourName\Work`
2. Destination: `D:\Backups\Office_Files`
3. **Include Extensions**: `.docx, .xlsx, .pptx, .doc, .xls, .ppt`
4. Exclude Extensions: (prazno)
5. Start Backup

**Rezultat:**
- Samo Office fajlovi će biti kopirani
- Svi drugi fajlovi (.txt, .pdf, slike, itd.) će biti preskočeni
- Status log: "✅ Backup completed! Copied: 234 files, Skipped: 1450 files"

---

### Primer 3: Backup medijskih fajlova (bez temp fajlova)

**Cilj**: Backup video i audio, ali bez temporary i cache fajlova

**Koraci:**
1. Source: `C:\Users\YourName\Media`
2. Destination: `E:\Media_Backup`
3. **Include Extensions**: `.mp4, .avi, .mkv, .mp3, .flac, .wav`
4. **Exclude Extensions**: `.tmp, .cache, .part`
5. Start Backup

**Rezultat:**
- Samo video i audio fajlovi će biti kopirani
- Temporary i incomplete download fajlovi će biti preskočeni

---

### Primer 4: Automatski Daily Backup u 2 AM

**Cilj**: Automatski backup svakog dana u 2:00 ujutru

**Koraci:**
1. Postavi Source i Destination
2. Postavi filtere (opciono)
3. Označi **"Enable Automatic Backup"**
4. Izaberi **Daily**
5. Upiši vreme: `02:00`
6. Klikni **Start Backup**

**Šta se dešava:**
- Prvi backup se izvršava odmah
- Zatim će se izvršavati automatski svaki dan u 2:00 AM
- **VAŽNO**: Aplikacija mora ostati pokrenuta!

**Pro tip**: Stavi aplikaciju u Windows Startup folder:
```
C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

---

### Primer 5: Weekly Backup (Ponedeljkom)

**Cilj**: Backup svake nedelje u ponedeljak u 10:00 AM

**Koraci:**
1. Postavi Source i Destination
2. Enable Automatic Backup
3. Izaberi **Weekly**
4. Vreme: `10:00`
5. Start Backup

**Rezultat:**
- Backup će se izvršavati svaki ponedeljak u 10:00
- Odlično za weekly reports ili project backups

---

### Primer 6: Monthly Backup (Prvi u mesecu)

**Cilj**: Backup 1. dana svakog meseca

**Koraci:**
1. Postavi Source i Destination
2. Enable Automatic Backup
3. Izaberi **Monthly**
4. Vreme: `09:00`
5. Start Backup

**Rezultat:**
- Backup će se izvršavati 1. dana svakog meseca u 9:00 AM
- Idealno za monthly archives

---

## 🎓 Napredne Tehnike

### Kombinovanje Filter Pravila

**Scenario**: Backup svih dokumenata OSIM starih .doc fajlova

**Rešenje:**
```
Include: .docx, .pdf, .txt, .xlsx
Exclude: (prazno)
```

**Scenario**: Backup svega OSIM log i temp fajlova

**Rešenje:**
```
Include: (prazno - znači sve)
Exclude: .log, .tmp, .cache, .bak, .old
```

### Multiple Source Backups

**Scenario**: Backup više foldera

**Rešenje**:
Ako želiš da backupuješ više foldera:

1. **Opcija A**: Napravi parent folder:
   ```
   C:\ToBackup\
   ├── Documents/
   ├── Pictures/
   └── Projects/
   ```
   Zatim backupuj `C:\ToBackup\`

2. **Opcija B**: Pokreni backup više puta sa različitim source/destination:
   - Run 1: Documents → Backup\Documents
   - Run 2: Pictures → Backup\Pictures
   - Run 3: Projects → Backup\Projects

### Incremental Backup Strategy

**Trenutna verzija radi "full backup"** - kopira sve fajlove svaki put.

**Za "pseudo-incremental" backup:**

1. Napravi destination folder sa datumom:
   ```
   Destination: D:\Backups\2026-02-19_Daily
   ```

2. Svaki dan promeni destination na novi datum:
   ```
   2026-02-20_Daily
   2026-02-21_Daily
   ...
   ```

3. Tako ćeš imati snapshot za svaki dan

**Pro tip**: Koristi scheduled backup sa različitim destination patterns.

---

## 🔍 Troubleshooting

### Problem: "No files match the filter criteria"

**Uzrok**: Filtri su previše strogi ili pogrešno uneseni

**Rešenje:**
1. Proveri da li extensions počinju sa tačkom: `.txt` ✅ ne `txt` ❌
2. Proveri da li source folder zaista sadrži te tipove fajlova
3. Privremeno obriši sve filtere i probaj ponovo

---

### Problem: GUI zamrzava

**Uzrok**: Threading nije pravilno postavljen (ne bi trebalo da se desi)

**Rešenje:**
1. Zatvori i ponovo pokreni aplikaciju
2. Proveri da li ima dovoljno RAM-a
3. Za velike backupe (10,000+ fajlova), povećaj RAM

---

### Problem: Scheduled backup se ne pokreće

**Uzrok**: Format vremena je pogrešan ili aplikacija nije pokrenuta

**Rešenje:**
1. Proveri format: `14:30` ✅ ne `2:30 PM` ❌
2. Proveri da li je aplikacija pokrenuta (mora biti!)
3. Gledaj status log za scheduler poruke

---

### Problem: Permission denied

**Uzrok**: Source ili destination folder zahteva admin prava

**Rešenje:**
1. Pokreni aplikaciju kao Administrator (desni klik → Run as administrator)
2. Ili izaberi folder koji ne zahteva admin prava

---

### Problem: Disk full

**Uzrok**: Destination disk nema dovoljno prostora

**Rešenje:**
1. Pre backupa proveri slobodan prostor
2. Koristi filtere da smanjiš broj fajlova
3. Izaberi drugi destination disk

---

## 💡 Best Practices

### 1. **Test prvo sa malim folderom**
   - Ne startuj odmah sa 100GB backup-om
   - Probaj prvo sa malim test folderom (100-200 MB)

### 2. **Koristi smislene destination paths**
   ```
   ❌ BAD: D:\New Folder\New Folder (1)\Backup
   ✅ GOOD: D:\Backups\Documents_2026-02-19
   ```

### 3. **Dokumentuj svoje filtere**
   - Napravi text file sa tvojim omiljenim filter kombinacijama
   ```
   # Office_Documents_Filter.txt
   Include: .docx, .xlsx, .pptx, .pdf
   Exclude: ~$, .tmp
   ```

### 4. **Scheduled Backup Tips**
   - Zakaži backup kada kompjuter radi, ali ti ne radiš
   - 2-3 AM je idealno vreme
   - Weekly backup: Nedeljom uveče ili ponedeljkom ujutru
   - Monthly backup: 1. u mesecu ujutru

### 5. **Verify Backup**
   - Nakon prvog backup-a, otvori destination folder
   - Proveri da li su svi fajlovi tu
   - Proveri da li su datumi očuvani

### 6. **Backup Strategy: 3-2-1 Rule**
   - **3** kopije podataka
   - **2** različita medija (HDD + USB ili Cloud)
   - **1** offsite backup (External drive ili cloud)

   **Primer:**
   - Original: `C:\Documents` (1)
   - Local backup: `D:\Backups` (2)
   - External: `E:\` (USB drive) (3) ✅

---

## 🛠️ Customization

### Promena Default Theme

Otvori `backup_gui.py` i pronađi:

```python
ctk.set_appearance_mode("dark")  # Promeni na "light" ili "system"
```

### Promena Window Veličine

```python
self.root.geometry("900x700")  # Promeni na željenu veličinu
```

### Dodavanje Custom Extensions

Možeš dodati bilo koje ekstenzije:
```
.psd, .ai        # Adobe fajlovi
.blend           # Blender fajlovi
.unitypackage    # Unity fajlovi
.dwg, .dxf       # CAD fajlovi
```

---

## 📊 Use Cases

### 1. **Developer Backup**
```
Source: C:\Projects\MyApp
Include: .py, .js, .jsx, .ts, .tsx, .json, .md
Exclude: node_modules, __pycache__, .git, dist, build
Schedule: Daily at 18:00 (after work)
```

### 2. **Photographer Backup**
```
Source: C:\Photos\2026
Include: .raw, .cr2, .nef, .jpg, .jpeg, .png
Exclude: .xmp, .aae
Schedule: Weekly on Sunday at 22:00
```

### 3. **Student Backup**
```
Source: C:\Users\Student\Schoolwork
Include: .docx, .pdf, .pptx, .xlsx
Exclude: .tmp, ~$
Schedule: Daily at 23:00
```

### 4. **Music Producer Backup**
```
Source: C:\Music\Projects
Include: .flp, .wav, .mp3, .flac, .mid
Exclude: .asd, .cache
Schedule: Daily at 03:00
```

---

## ❓ FAQ

**Q: Koliko prostora zauzima backup?**
A: Jednak original size-u fajlova. Ova aplikacija ne kompresuje.

**Q: Mogu li backupovati na Network Drive?**
A: Da! Samo izaberi network path kao destination (npr. `\\Server\Share\Backup`)

**Q: Šta se dešava ako se backup prekine?**
A: Klikni Cancel ili zatvori app. Već kopirani fajlovi ostaju, ali backup nije kompletan.

**Q: Mogu li backupovati otvorene fajlove?**
A: Windows može da blokira neke otvorene fajlove. Zatvori aplikacije pre backup-a.

**Q: Da li mogu da backup-ujem sistem fajlove?**
A: Ne preporučuje se. Koristi Windows System Image Backup za sistem.

**Q: Gde su scheduled backup logovi?**
A: U status log-u aplikacije. Za eksterne logs, pogledaj console output.

---

## 🎉 Zaključak

Sada si spreman da koristiš **Advanced Backup Tool** kao profesionalac!

**Zapamti:**
- ✅ Test sa malim folderom prvo
- ✅ Koristi smart filtere
- ✅ Schedule backup-e za non-work hours
- ✅ Verifikuj prvi backup
- ✅ Follow 3-2-1 backup rule

**Srećan Backup! 🚀**
