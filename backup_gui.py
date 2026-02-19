"""
Backup GUI - Modern CustomTkinter interface (Srpski jezik)
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import os
from backup_engine import BackupEngine
from scheduler import BackupScheduler

SETTINGS_FILE = "podesavanja.json"


def ucitaj_podesavanja():
    """Ucitaj poslednja podesavanja iz fajla"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def sacuvaj_podesavanja(data: dict):
    """Sacuvaj podesavanja u fajl"""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Greska pri cuvanju podesavanja: {e}")


class BackupGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Alat za Backup Podataka")
        self.root.geometry("920x780")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.backup_engine = BackupEngine(progress_callback=self.azuriraj_progres)
        self.scheduler = BackupScheduler(self.backup_engine)
        self.backup_thread = None

        # Varijable
        self.izvorni_folder = ctk.StringVar()
        self.odredisni_folder = ctk.StringVar()
        self.ukljuci_ext = ctk.StringVar()
        self.iskljuci_ext = ctk.StringVar()
        self.raspored_ukljucen = ctk.BooleanVar(value=False)
        self.tip_rasporeda = ctk.StringVar(value="dnevno")
        self.vreme_rasporeda = ctk.StringVar(value="12:00")

        # Ucitaj poslednja podesavanja
        self.ucitaj_prethodna_podesavanja()

        self.kreiraj_widgete()
        self.provjeri_raspored()

    def ucitaj_prethodna_podesavanja(self):
        """Ucitaj podesavanja i popuni varijable"""
        p = ucitaj_podesavanja()
        if p.get("izvorni_folder"):
            self.izvorni_folder.set(p["izvorni_folder"])
        if p.get("odredisni_folder"):
            self.odredisni_folder.set(p["odredisni_folder"])
        if p.get("ukljuci_ext"):
            self.ukljuci_ext.set(p["ukljuci_ext"])
        if p.get("iskljuci_ext"):
            self.iskljuci_ext.set(p["iskljuci_ext"])
        if p.get("tip_rasporeda"):
            self.tip_rasporeda.set(p["tip_rasporeda"])
        if p.get("vreme_rasporeda"):
            self.vreme_rasporeda.set(p["vreme_rasporeda"])
        if p.get("raspored_ukljucen") is not None:
            self.raspored_ukljucen.set(p["raspored_ukljucen"])

    def sacuvaj_trenutna_podesavanja(self):
        """Sacuvaj trenutna podesavanja"""
        sacuvaj_podesavanja({
            "izvorni_folder": self.izvorni_folder.get(),
            "odredisni_folder": self.odredisni_folder.get(),
            "ukljuci_ext": self.ukljuci_ext.get(),
            "iskljuci_ext": self.iskljuci_ext.get(),
            "tip_rasporeda": self.tip_rasporeda.get(),
            "vreme_rasporeda": self.vreme_rasporeda.get(),
            "raspored_ukljucen": self.raspored_ukljucen.get(),
        })

    def kreiraj_widgete(self):
        """Kreiraj sve GUI komponente"""
        # Tabovi
        self.tabovi = ctk.CTkTabview(self.root)
        self.tabovi.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabovi.add("💾  Backup")
        self.tabovi.add("🔄  Restore")

        self.kreiraj_tab_backup(self.tabovi.tab("💾  Backup"))
        self.kreiraj_tab_restore(self.tabovi.tab("🔄  Restore"))

    # ─────────────────────────────────────────────
    #  TAB: BACKUP
    # ─────────────────────────────────────────────
    def kreiraj_tab_backup(self, tab):
        # Naslov
        ctk.CTkLabel(
            tab,
            text="Alat za Backup Podataka",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 16))

        # Izvorni folder
        okvir_izvor = ctk.CTkFrame(tab)
        okvir_izvor.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_izvor, text="Izvorni folder:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        red_izvor = ctk.CTkFrame(okvir_izvor)
        red_izvor.pack(fill="x", padx=10, pady=(0, 8))
        ctk.CTkEntry(red_izvor, textvariable=self.izvorni_folder).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(red_izvor, text="Pregledaj", command=self.odaberi_izvor, width=100).pack(side="left")

        # Odredisni folder
        okvir_odrediste = ctk.CTkFrame(tab)
        okvir_odrediste.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_odrediste, text="Odredišni folder:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        red_odrediste = ctk.CTkFrame(okvir_odrediste)
        red_odrediste.pack(fill="x", padx=10, pady=(0, 8))
        ctk.CTkEntry(red_odrediste, textvariable=self.odredisni_folder).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(red_odrediste, text="Pregledaj", command=self.odaberi_odrediste, width=100).pack(side="left")

        # Filteri
        okvir_filteri = ctk.CTkFrame(tab)
        okvir_filteri.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_filteri, text="Filteri fajlova:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))

        red_ukljuci = ctk.CTkFrame(okvir_filteri)
        red_ukljuci.pack(fill="x", padx=10, pady=3)
        ctk.CTkLabel(red_ukljuci, text="Uključi ekstenzije:", width=160).pack(side="left")
        ctk.CTkEntry(red_ukljuci, textvariable=self.ukljuci_ext, placeholder_text=".txt, .pdf, .docx").pack(side="left", fill="x", expand=True)

        red_iskljuci = ctk.CTkFrame(okvir_filteri)
        red_iskljuci.pack(fill="x", padx=10, pady=(3, 8))
        ctk.CTkLabel(red_iskljuci, text="Isključi ekstenzije:", width=160).pack(side="left")
        ctk.CTkEntry(red_iskljuci, textvariable=self.iskljuci_ext, placeholder_text=".tmp, .log").pack(side="left", fill="x", expand=True)

        # Raspored
        okvir_raspored = ctk.CTkFrame(tab)
        okvir_raspored.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_raspored, text="Automatsko zakazivanje:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))

        ctk.CTkCheckBox(
            okvir_raspored,
            text="Omogući automatski backup",
            variable=self.raspored_ukljucen,
            command=self.toggle_raspored
        ).pack(anchor="w", padx=10, pady=4)

        self.okvir_raspored_config = ctk.CTkFrame(okvir_raspored)
        self.okvir_raspored_config.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(self.okvir_raspored_config, text="Učestalost:", width=90).pack(side="left", padx=(0, 4))
        ctk.CTkRadioButton(self.okvir_raspored_config, text="Dnevno", variable=self.tip_rasporeda, value="dnevno").pack(side="left", padx=5)
        ctk.CTkRadioButton(self.okvir_raspored_config, text="Nedeljno", variable=self.tip_rasporeda, value="nedeljno").pack(side="left", padx=5)
        ctk.CTkRadioButton(self.okvir_raspored_config, text="Mesečno", variable=self.tip_rasporeda, value="mesecno").pack(side="left", padx=5)
        ctk.CTkLabel(self.okvir_raspored_config, text="Vreme:", width=55).pack(side="left", padx=(16, 4))
        ctk.CTkEntry(self.okvir_raspored_config, textvariable=self.vreme_rasporeda, width=80, placeholder_text="SS:MM").pack(side="left")

        # Sakrij config ako nije ukljucen
        if not self.raspored_ukljucen.get():
            self.okvir_raspored_config.pack_forget()

        # Progres
        okvir_progres = ctk.CTkFrame(tab)
        okvir_progres.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_progres, text="Napredak:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        self.traka_napretka = ctk.CTkProgressBar(okvir_progres)
        self.traka_napretka.pack(fill="x", padx=10, pady=4)
        self.traka_napretka.set(0)
        self.labela_napretka = ctk.CTkLabel(okvir_progres, text="Spreman za backup", font=ctk.CTkFont(size=12))
        self.labela_napretka.pack(padx=10, pady=(0, 8))

        # Dugmici
        okvir_dugmici = ctk.CTkFrame(tab)
        okvir_dugmici.pack(fill="x", pady=6)
        self.dugme_backup = ctk.CTkButton(
            okvir_dugmici, text="▶  Pokreni Backup",
            command=self.pokreni_backup,
            width=200, height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.dugme_backup.pack(side="left", padx=(10, 5))
        self.dugme_otkazivanje = ctk.CTkButton(
            okvir_dugmici, text="✖  Otkaži",
            command=self.otkazivanje_backup,
            width=150, height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#c0392b", hover_color="#922b21",
            state="disabled"
        )
        self.dugme_otkazivanje.pack(side="left", padx=5)

        # Log
        okvir_log = ctk.CTkFrame(tab)
        okvir_log.pack(fill="both", expand=True, pady=4)
        ctk.CTkLabel(okvir_log, text="Dnevnik aktivnosti:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        self.tekst_log = ctk.CTkTextbox(okvir_log, height=130)
        self.tekst_log.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    # ─────────────────────────────────────────────
    #  TAB: RESTORE
    # ─────────────────────────────────────────────
    def kreiraj_tab_restore(self, tab):
        ctk.CTkLabel(
            tab,
            text="Obnavljanje Podataka (Restore)",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(10, 16))

        # Folder backup-a (izvor za restore)
        okvir_backup_folder = ctk.CTkFrame(tab)
        okvir_backup_folder.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_backup_folder, text="Folder sa backup-om:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        red = ctk.CTkFrame(okvir_backup_folder)
        red.pack(fill="x", padx=10, pady=(0, 8))
        self.restore_izvor = ctk.StringVar()
        ctk.CTkEntry(red, textvariable=self.restore_izvor).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(red, text="Pregledaj", command=self.odaberi_restore_izvor, width=100).pack(side="left")

        # Folder za obnavljanje (odrediste)
        okvir_restore_odrediste = ctk.CTkFrame(tab)
        okvir_restore_odrediste.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_restore_odrediste, text="Obnovi u folder:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        red2 = ctk.CTkFrame(okvir_restore_odrediste)
        red2.pack(fill="x", padx=10, pady=(0, 8))
        self.restore_odrediste = ctk.StringVar()
        ctk.CTkEntry(red2, textvariable=self.restore_odrediste).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(red2, text="Pregledaj", command=self.odaberi_restore_odrediste, width=100).pack(side="left")

        # Opcije
        okvir_opcije = ctk.CTkFrame(tab)
        okvir_opcije.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_opcije, text="Opcije obnavljanja:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        self.prepisati_postojece = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            okvir_opcije,
            text="Prepiši postojeće fajlove",
            variable=self.prepisati_postojece
        ).pack(anchor="w", padx=10, pady=(0, 8))

        # Progres restore
        okvir_progres_r = ctk.CTkFrame(tab)
        okvir_progres_r.pack(fill="x", pady=4)
        ctk.CTkLabel(okvir_progres_r, text="Napredak:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        self.traka_restore = ctk.CTkProgressBar(okvir_progres_r)
        self.traka_restore.pack(fill="x", padx=10, pady=4)
        self.traka_restore.set(0)
        self.labela_restore = ctk.CTkLabel(okvir_progres_r, text="Spreman za obnavljanje", font=ctk.CTkFont(size=12))
        self.labela_restore.pack(padx=10, pady=(0, 8))

        # Dugme restore
        okvir_dugme_r = ctk.CTkFrame(tab)
        okvir_dugme_r.pack(fill="x", pady=6)
        self.dugme_restore = ctk.CTkButton(
            okvir_dugme_r, text="🔄  Pokreni Restore",
            command=self.pokreni_restore,
            width=200, height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1a7a4a", hover_color="#145c38"
        )
        self.dugme_restore.pack(side="left", padx=10)

        # Log restore
        okvir_log_r = ctk.CTkFrame(tab)
        okvir_log_r.pack(fill="both", expand=True, pady=4)
        ctk.CTkLabel(okvir_log_r, text="Dnevnik obnavljanja:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        self.tekst_log_restore = ctk.CTkTextbox(okvir_log_r, height=180)
        self.tekst_log_restore.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    # ─────────────────────────────────────────────
    #  BACKUP LOGIKA
    # ─────────────────────────────────────────────
    def toggle_raspored(self):
        if self.raspored_ukljucen.get():
            self.okvir_raspored_config.pack(fill="x", padx=10, pady=(0, 8))
        else:
            self.okvir_raspored_config.pack_forget()

    def odaberi_izvor(self):
        folder = filedialog.askdirectory(title="Izaberite izvorni folder")
        if folder:
            self.izvorni_folder.set(folder)

    def odaberi_odrediste(self):
        folder = filedialog.askdirectory(title="Izaberite odredišni folder")
        if folder:
            self.odredisni_folder.set(folder)

    def parsiraj_ekstenzije(self, tekst: str):
        if not tekst.strip():
            return []
        ext = [e.strip() for e in tekst.split(",") if e.strip()]
        return [e if e.startswith('.') else f'.{e}' for e in ext]

    def log(self, poruka: str):
        self.tekst_log.insert("end", f"{poruka}\n")
        self.tekst_log.see("end")

    def azuriraj_progres(self, trenutno: int, ukupno: int, ime_fajla: str):
        progres = trenutno / ukupno if ukupno > 0 else 0
        self.traka_napretka.set(progres)
        self.labela_napretka.configure(text=f"Kopiranje: {ime_fajla} ({trenutno}/{ukupno})")
        self.root.update_idletasks()

    def izvrsi_backup(self):
        try:
            izvor = self.izvorni_folder.get()
            odrediste = self.odredisni_folder.get()
            ukljuci = self.parsiraj_ekstenzije(self.ukljuci_ext.get())
            iskljuci = self.parsiraj_ekstenzije(self.iskljuci_ext.get())

            if not izvor or not odrediste:
                self.log("❌ Greška: Molimo izaberite izvorni i odredišni folder!")
                return

            self.sacuvaj_trenutna_podesavanja()

            self.log(f"🚀 Pokretanje backup-a: {izvor} → {odrediste}")
            if ukljuci:
                self.log(f"   Uključuje: {', '.join(ukljuci)}")
            if iskljuci:
                self.log(f"   Isključuje: {', '.join(iskljuci)}")

            rezultat = self.backup_engine.backup(
                source_dir=izvor,
                destination_dir=odrediste,
                include_extensions=ukljuci,
                exclude_extensions=iskljuci
            )

            if rezultat["success"]:
                self.log(f"✅ Backup završen uspješno!")
                self.log(f"   Kopirano fajlova: {rezultat['copied']}")
                self.log(f"   Preskočeno fajlova: {rezultat['skipped']}")
                self.log(f"   Vreme: {rezultat['timestamp']}")
                messagebox.showinfo("Uspjeh", f"Backup završen!\n\nKopirano: {rezultat['copied']} fajlova\nPreskočeno: {rezultat['skipped']} fajlova")
            else:
                self.log(f"❌ Backup nije uspeo: {rezultat['error']}")
                messagebox.showerror("Greška", f"Backup nije uspeo:\n{rezultat['error']}")

        except Exception as e:
            self.log(f"❌ Izuzetak: {e}")
            messagebox.showerror("Greška", str(e))
        finally:
            self.traka_napretka.set(0)
            self.labela_napretka.configure(text="Spreman za backup")
            self.dugme_backup.configure(state="normal")
            self.dugme_otkazivanje.configure(state="disabled")

    def pokreni_backup(self):
        self.dugme_backup.configure(state="disabled")
        self.dugme_otkazivanje.configure(state="normal")
        self.backup_thread = threading.Thread(target=self.izvrsi_backup, daemon=True)
        self.backup_thread.start()
        if self.raspored_ukljucen.get():
            self.postavi_raspored()

    def otkazivanje_backup(self):
        self.backup_engine.cancel()
        self.log("⚠️ Backup otkazan od strane korisnika")
        self.dugme_otkazivanje.configure(state="disabled")

    def postavi_raspored(self):
        self.scheduler.schedule_backup(
            schedule_type=self.tip_rasporeda.get(),
            time_str=self.vreme_rasporeda.get(),
            source_dir=self.izvorni_folder.get(),
            destination_dir=self.odredisni_folder.get(),
            include_extensions=self.parsiraj_ekstenzije(self.ukljuci_ext.get()),
            exclude_extensions=self.parsiraj_ekstenzije(self.iskljuci_ext.get())
        )
        self.log(f"⏰ Zakazan {self.tip_rasporeda.get()} backup u {self.vreme_rasporeda.get()}")

    def provjeri_raspored(self):
        self.scheduler.run_pending()
        self.root.after(1000, self.provjeri_raspored)

    # ─────────────────────────────────────────────
    #  RESTORE LOGIKA
    # ─────────────────────────────────────────────
    def odaberi_restore_izvor(self):
        folder = filedialog.askdirectory(title="Izaberite folder sa backup-om")
        if folder:
            self.restore_izvor.set(folder)

    def odaberi_restore_odrediste(self):
        folder = filedialog.askdirectory(title="Izaberite folder za obnavljanje")
        if folder:
            self.restore_odrediste.set(folder)

    def log_restore(self, poruka: str):
        self.tekst_log_restore.insert("end", f"{poruka}\n")
        self.tekst_log_restore.see("end")

    def azuriraj_progres_restore(self, trenutno: int, ukupno: int, ime_fajla: str):
        progres = trenutno / ukupno if ukupno > 0 else 0
        self.traka_restore.set(progres)
        self.labela_restore.configure(text=f"Obnavljanje: {ime_fajla} ({trenutno}/{ukupno})")
        self.root.update_idletasks()

    def izvrsi_restore(self):
        import shutil
        izvor = self.restore_izvor.get()
        odrediste = self.restore_odrediste.get()
        prepisati = self.prepisati_postojece.get()

        if not izvor or not odrediste:
            self.log_restore("❌ Greška: Molimo izaberite oba foldera!")
            return
        if not os.path.exists(izvor):
            self.log_restore("❌ Greška: Folder sa backup-om ne postoji!")
            return

        try:
            os.makedirs(odrediste, exist_ok=True)
        except Exception as e:
            self.log_restore(f"❌ Greška pri kreiranju odredišnog foldera: {e}")
            return

        # Prebroj fajlove
        ukupno = sum(len(fajlovi) for _, _, fajlovi in os.walk(izvor))
        if ukupno == 0:
            self.log_restore("❌ Nema fajlova u backup folderu!")
            self.dugme_restore.configure(state="normal")
            return

        kopirano = 0
        preskoceno = 0
        greske = []

        self.log_restore(f"🔄 Pokretanje restore-a: {izvor} → {odrediste}")
        self.log_restore(f"   Ukupno fajlova: {ukupno}")

        for root_dir, dirs, fajlovi in os.walk(izvor):
            for fajl in fajlovi:
                src_fajl = os.path.join(root_dir, fajl)
                rel_putanja = os.path.relpath(src_fajl, izvor)
                dest_fajl = os.path.join(odrediste, rel_putanja)

                os.makedirs(os.path.dirname(dest_fajl), exist_ok=True)

                if not prepisati and os.path.exists(dest_fajl):
                    preskoceno += 1
                    continue

                try:
                    shutil.copy2(src_fajl, dest_fajl)
                    kopirano += 1
                    self.azuriraj_progres_restore(kopirano + preskoceno, ukupno, fajl)
                except Exception as e:
                    greske.append(f"{fajl}: {e}")
                    preskoceno += 1

        self.traka_restore.set(0)
        self.labela_restore.configure(text="Spreman za obnavljanje")
        self.dugme_restore.configure(state="normal")

        self.log_restore(f"✅ Restore završen!")
        self.log_restore(f"   Obnovljeno fajlova: {kopirano}")
        self.log_restore(f"   Preskočeno: {preskoceno}")
        if greske:
            self.log_restore(f"   Greške ({len(greske)}):")
            for g in greske[:5]:
                self.log_restore(f"     • {g}")

        messagebox.showinfo("Restore završen", f"Obnavljanje završeno!\n\nObnovljeno: {kopirano} fajlova\nPreskočeno: {preskoceno} fajlova")

    def pokreni_restore(self):
        odrediste = self.restore_odrediste.get()
        if odrediste and os.path.exists(odrediste):
            potvrda = messagebox.askyesno(
                "Potvrda restore-a",
                f"Da li ste sigurni da želite da obnovite fajlove u:\n{odrediste}\n\nOvo može prepisati postojeće fajlove!"
            )
            if not potvrda:
                return

        self.dugme_restore.configure(state="disabled")
        threading.Thread(target=self.izvrsi_restore, daemon=True).start()

    def pokreni(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BackupGUI()
    app.pokreni()
