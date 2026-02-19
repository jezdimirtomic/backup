# 🗄️ Advanced Backup Tool

Moderna Python GUI aplikacija za automatski backup podataka sa naprednim filterima i scheduling opcijama.

## ✨ Karakteristike

- **Moderni GUI** - CustomTkinter interfejs sa dark/light mode podrškom
- **Napredno filterisanje** - Include/Exclude ekstenzije (npr. `.txt`, `.pdf`, `.mp4`)
- **Real-time progres** - Progress bar koji pokazuje tačan status operacije
- **Automatsko zakazivanje** - Daily, Weekly, Monthly backup intervali
- **Multithreading** - GUI ostaje responzivan tokom backup operacija
- **Detaljni logovi** - Status log za praćenje svih operacija
- **Windows optimizovano** - Puna podrška za Windows file paths

## 📋 Zahtevi

- Python 3.11+
- Windows 10/11 (ili Linux/macOS za testiranje)

## 🚀 Instalacija

### 1. Klonirajte ili preuzmite projekat

```bash
cd /workspace
```

### 2. Instalirajte dependencies

```bash
pip install -r requirements.txt
```

Dependencies:
- `customtkinter` - Moderan GUI framework
- `schedule` - Scheduling biblioteka za automatske backup-e

## 💻 Pokretanje aplikacije

```bash
python backup_gui.py
```

## 📖 Uputstvo za korišćenje

### Osnovni Backup

1. **Izaberite Source Directory** - Kliknite "Browse" i odaberite folder koji želite da backupujete
2. **Izaberite Destination Directory** - Kliknite "Browse" i odaberite gde će backup biti sačuvan
3. **Podesite filtere** (opciono):
   - **Include Extensions**: Unesite ekstenzije koje želite da backupujete (npr. `.txt, .pdf, .docx`)
   - **Exclude Extensions**: Unesite ekstenzije koje želite da preskočite (npr. `.tmp, .log, .cache`)
4. **Kliknite "Start Backup"** - Backup će početi, sa live progress barom

### Primer filtera:

**Include samo dokumente:**
```
Include Extensions: .pdf, .docx, .txt, .xlsx
Exclude Extensions: (prazno)
```

**Exclude temporary fajlove:**
```
Include Extensions: (prazno - svi fajlovi)
Exclude Extensions: .tmp, .log, .cache, .bak
```

**Backup samo video fajlove:**
```
Include Extensions: .mp4, .avi, .mkv, .mov
Exclude Extensions: (prazno)
```

### Automatsko zakazivanje

1. **Označite "Enable Automatic Backup"**
2. **Izaberite frekvenciju:**
   - **Daily** - Svaki dan u isto vreme
   - **Weekly** - Jednom nedeljno (ponedeljkom)
   - **Monthly** - Jednom mesečno (1. u mesecu)
3. **Unesite vreme** u formatu `HH:MM` (24-časovni format)
   - Primer: `14:30` za 2:30 PM
   - Primer: `09:00` za 9:00 AM
4. **Kliknite "Start Backup"** - Backup će se prvo izvršiti odmah, a zatim automatski po rasporedu

## 🏗️ Struktura projekta

```
/workspace/
│
├── backup_gui.py          # Glavni GUI interfejs
├── backup_engine.py       # Core backup logika sa filterisanjem
├── scheduler.py           # Scheduling sistem
├── requirements.txt       # Python dependencies
└── README.md             # Dokumentacija
```

## 🔧 Tehničke Specifikacije

### BackupEngine (backup_engine.py)

- **Filtering logika**: Podržava include/exclude liste ekstenzija
- **Progress tracking**: Callback funkcija za real-time ažuriranje
- **Error handling**: Detaljno hvatanje i reporting grešaka
- **Preservation**: Koristi `shutil.copy2` za očuvanje metadata

### BackupGUI (backup_gui.py)

- **Framework**: CustomTkinter za moderan UI
- **Threading**: Backup operacije rade u background thread-u
- **Responsiveness**: GUI ostaje responzivan tokom backup-a
- **Logging**: Real-time status log sa emoji ikonama

### BackupScheduler (scheduler.py)

- **Daily**: Svaki dan u specifično vreme
- **Weekly**: Svaki ponedeljak (može se prilagoditi)
- **Monthly**: Prvi dan u mesecu
- **Non-blocking**: Scheduled jobs ne blokiraju GUI

## 🎨 UI Komponente

- **Source/Destination browsing** - File dialog za lak izbor foldera
- **Filter inputs** - Tekstualna polja za ekstenzije (comma-separated)
- **Schedule configuration** - Radio buttons za frequency + time picker
- **Progress bar** - Real-time vizualni progres
- **Status log** - Scrollable text area sa svim operacijama
- **Control buttons** - Start/Cancel sa disabled states

## ⚙️ Konfiguracija

### Promena default vrednosti

U `backup_gui.py`, možete izmeniti default-e:

```python
# Default schedule time
self.schedule_time = ctk.StringVar(value="12:00")  # Promenite na željeno vreme

# Default theme
ctk.set_appearance_mode("dark")  # Ili "light", "system"
```

### Promena window veličine

```python
self.root.geometry("900x700")  # Promenite na željenu širinu x visinu
```

## 🐛 Troubleshooting

### "No files match the filter criteria"
- Proverite da li su ekstenzije ispravno unesene (sa tačkom: `.txt` ne `txt`)
- Proverite da li source folder sadrži fajlove sa tim ekstenzijama

### GUI zamrzava tokom backup-a
- Ovo ne bi trebalo da se dešava zbog threading-a
- Ako se desi, proverite da li je backup_thread pravilno pokrenut

### Scheduled backup se ne izvršava
- Proverite format vremena (mora biti `HH:MM` u 24-časovnom formatu)
- Aplikacija mora da ostane pokrenuta da bi scheduled jobs radili
- Proverite status log za scheduler poruke

## 📝 Napomene

- **Backup tip**: Ovo je "full backup" - kopira sve fajlove svaki put
- **Differential backup nije podržan** - sve što matchuje filter se kopira
- **Overwrites**: Destinacija fajlova se overwrite-uje ako već postoje
- **Folder struktura**: Originalna folder struktura se čuva u destination-u

## 🔒 Sigurnost

- Aplikacija ne menja source fajlove (read-only operacija)
- Sve greške se loguju, ali backup nastavlja sa sledećim fajlovima
- Cancel dugme omogućava zaustavljanje operacije u bilo kom trenutku

## 🚀 Buduća poboljšanja

- [ ] Incremental backup (samo izmenjeni fajlovi)
- [ ] Backup compression (ZIP arhive)
- [ ] Email notifikacije nakon završenog backup-a
- [ ] Backup istorija i restore funkcionalnost
- [ ] Cloud storage integracija (Google Drive, Dropbox)
- [ ] Multi-source backup (više source foldera)

## 📄 Licenca

Open source projekat - slobodno koristite i modifikujte.

## 👨‍💻 Autor

Kreirao: The Virtuoso (Nxcode Platform)

---

**Uživajte u sigurnom backup-u! 🎉**
