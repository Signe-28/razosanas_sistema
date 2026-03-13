import sqlite3 as db
import tkinter as tk
from tkinter import Scrollbar
from tkinter import messagebox
from tkinter import ttk

#---------------------------------------------------------------
# ADMINISTRATORAM :
# Kods: 123456789

# 1. līmeņa lietotāja var pievienot un rediģēt produktus, izejvielas un tehniku, bet tikai apskatīties brīdinājumus
# 2. līmeņa lietotājs var tikai apskatīties produktus, izejvielas, tehniku un brīdinājumus
# Administrators var redzēt produktus, izejvielas un tehniku, un var rediģēt brīdinājumus un lietotāju lomas
#---------------------------------------------------------------


# - 1. ievada lietotājvārdu un paroli ja tādi ir 
# - 1.5. Ja nav sava profila, tad spiež uz pogas "jauns lietotājs"
# - 2. Ja sakrīt ar datubāzi pieeja sistēmai, ja nesakrīt tad nev pieeja sistēmai
# - 3. informācija salikta tabulās un tabulu sānā poga pievienoit jaunu un rediģēt
# - 4. Ja vēlas izveidot jaunu, tad aizved uz jaunu lapu
# - 5. Ja vēlas rediģēt, tad uzspiežu uz tā kuru vēlas rediģēt un informāciju atver jaunā lapā

# - 1. Ievada izejvielas
# - 2. Var mainīt izejvielu daudzumu
# - 2.5. Kad izejvielas ir zem konkrēta skaita, tad izmet brīdinājumu, ka maz izejvielas palikušas
# - 3. saražotās produkcijas uzskaite (Kurā noliktavā atrodas)
# - 4. 1. līmenis var rediģēt un pievienot informāciju
# - 5. 2. līmenis var tikai apskatīt informāciju
# - 6. Pievienot administratora logu
# - 8. Lietotāju e-pasts
# - 9. Produkcijas kvalitāte, ja zema tad brīdinājums
# - 10. Dzēst lietotāja profilu
# - 11. Brīdinājumi par problēmām
# - 12. Tabula par iekārtām




### IZVEIDO DATUBĀZES

conn = db.connect("sistema.db")
cursor = conn.cursor()

# Izveido autorizācijas tabulu
cursor.execute( """ 
CREATE TABLE IF NOT EXISTS "autorizacija" (
    lietotaja_ID INTEGER PRIMARY KEY,
    parole TEXT,
    loma TEXT,
    epasts TEXT
) """)


# Izveido produkta inventerizācijas tabulu
cursor.execute( """
CREATE TABLE IF NOT EXISTS "produkta_inventerizacija" (
    produkta_ID INTEGER PRIMARY KEY,
    produkta_nosaukums TEXT,
    daudzums INTEGER,
    noliktava TEXT,
    kvalitate TEXT
) """ )

# Izveido rezerves daļu inventerizācijas tabulu
cursor.execute( """
CREATE TABLE IF NOT EXISTS "izejvielu_inventerizacija" (
    izejvielas_ID INTEGER PRIMARY KEY, 
    izejviela TEXT,
    daudzums INTEGER
) """)

# Izveido brīdinājumu tabulu
cursor.execute("""
CREATE TABLE IF NOT EXISTS "bridinajumi" (
    bridinajums TEXT,
    nr INTEGER PRIMARY KEY
)   """)

# Izveido tehnikas tabulu
cursor.execute("""
CREATE TABLE IF NOT EXISTS "tehnikas_inventerizacija" (
    tehnikas_ID INTEGER PRIMARY KEY,
    tehnikas_nosaukums TEXT, 
    iegades_datums TEXT,
    kludas TEXT
)   """)

conn.commit()

### FUNKCIJAS 

# Notīra ekrānu
def clear_screen():
    
    for element in screen.winfo_children():
        element.destroy()


def autorizacija():

    # Autorizācijas info
    lietotaja_ID = int(ievade_lietotaja_ID.get())
    parole = str(ievade_parole.get().strip())
    
    if (lietotaja_ID is not None and parole is not None):
        cursor.execute("SELECT parole FROM autorizacija WHERE lietotaja_ID=?", (lietotaja_ID,))
        db_parole = cursor.fetchone()
        if (db_parole is not None and parole == db_parole[0]):
            cursor.execute("SELECT loma FROM autorizacija WHERE lietotaja_ID=?", (lietotaja_ID,))
            db_loma = cursor.fetchone()
            if (db_loma[0] == "lvl 1"):
                galvenais_logs_1()
            elif (db_loma[0] == "lvl 2"):
                galvenais_logs_2()
        else:
            messagebox.showwarning("Kļūda", "Nepareizs lietotājvārds un/vai parole")
    else: 
        messagebox.showwarning("Kļūda", "Nav ievadīta parole!")
    

def autorizacijas_ievade():
    clear_screen()
    
    # ievades lauciņi autorizācijai
    tk.Label(screen, text="Lietotāja ID").pack(padx=5, pady=10)
    global ievade_lietotaja_ID
    ievade_lietotaja_ID = tk.Entry(screen)
    ievade_lietotaja_ID.pack(pady=10)

    tk.Label(screen, text="Parole").pack(padx=5, pady=10)
    global ievade_parole
    ievade_parole = tk.Entry(screen)
    ievade_parole.pack(pady=10)
    
    tk.Button(screen, text="Pievienoties", command=autorizacija).pack(padx=5, pady=10)
    tk.Button(screen, text="Jauns lietotājs", command=jauna_lietotaja_ievade).pack(padx=5, pady=10)
    tk.Button(screen, text="Administrators", command=administrators_ievade).pack(padx=5, pady=10)


def administratora_parbaude():
    
    administratora_kods = str(ievade_administratora_kods.get())
    if (administratora_kods == "123456789") :
        administrators()
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs kods!")


def administrators_ievade():
    clear_screen()
    
    tk.Label(screen, text="Administratora kods").pack(padx=5, pady=10)
    global ievade_administratora_kods
    ievade_administratora_kods = tk.Entry(screen)
    ievade_administratora_kods.pack(pady=10)
    
    tk.Button(screen, text="Ievadīt", command=administratora_parbaude).pack(pady=10)
    tk.Button(screen, text="Atpakaļ", command=autorizacijas_ievade).pack(pady=10)


def jauns_lietotajs():

    jauns_lietotaja_ID = int(ievade_jauns_lietotaja_ID.get())
    jauns_parole = str(ievade_jauns_parole.get().replace(" ", ""))
    loma = izvele.get()
    epasts = str(ievade_jauns_epasts.get())
    
    if (jauns_lietotaja_ID is not None and jauns_parole is not None):
        cursor.execute("SELECT COUNT(*) FROM autorizacija WHERE lietotaja_ID=?", (jauns_lietotaja_ID,)) 
        db_lietotaja_ID = cursor.fetchone()[0]
        if (db_lietotaja_ID == 0):
            cursor.execute("INSERT INTO autorizacija(lietotaja_ID, parole, loma, epasts) VALUES(?, ?, ?, ?)", (jauns_lietotaja_ID, jauns_parole, loma, epasts))
            conn.commit()
            if (loma == "lvl 1"):
                galvenais_logs_1()
            elif (loma == "lvl 2"):
                galvenais_logs_2()
        else:
            messagebox.showwarning("Kļūda", "tāds lietotājvārds jau pastāv")
    else :
        messagebox.showwarning("Kļūda", "Nav ievadīta parole!")


def jauna_lietotaja_ievade():
    clear_screen()

    # ievades lauciņi jaunam lietotajam
    tk.Label(screen, text="Jaunais lietotāja ID (tikai cipari)").pack(pady=10)
    global ievade_jauns_lietotaja_ID
    ievade_jauns_lietotaja_ID = tk.Entry(screen)
    ievade_jauns_lietotaja_ID.pack(pady=10)

    tk.Label(screen, text="Parole").pack(pady=10)
    global ievade_jauns_parole
    ievade_jauns_parole = tk.Entry(screen)
    ievade_jauns_parole.pack(pady=10)
    
    tk.Label(screen, text="E-pasts").pack(pady=10)
    global ievade_jauns_epasts
    ievade_jauns_epasts = tk.Entry(screen)
    ievade_jauns_epasts.pack(pady=10)
    
    tk.Label(screen, text="Piekļuves līmenis").pack(pady=10)
    global izvele
    lomas = ["lvl 1", "lvl 2"]
    izvele = tk.StringVar(screen)
    izvele.set(lomas[1])
    dropdown = tk.OptionMenu(screen, izvele, *lomas)
    dropdown.pack(pady=10)
    
    tk.Button(screen, text="Izveidot profilu", command=jauns_lietotajs).pack(padx=10, pady=20)
    tk.Button(screen, text="Atpakaļ", command=autorizacijas_ievade).pack(padx=10, pady=50)


def produkta_inventerizacija():
    
    # produkta inventerizācija
    try:
        produkta_ID = int(ievade_produkta_ID.get())
        produkta_nosaukums = str(ievade_produkta_nosaukums.get())
        daudzums = int(ievade_daudzums.get())
        noliktava = izvele_noliktava.get()
        kvalitate = izvele_kvalitate.get()
    except ValueError:
        messagebox.showwarning("Kļūda!", "Lūdzu ievadi korektas skaitliskas vērtības!")
        return
    
    if (kvalitate == "Zema"):
        messagebox.showinfo("Uzmanību!", "Preces kvalitāte is zema!")
    
    cursor.execute("INSERT INTO produkta_inventerizacija(produkta_ID, produkta_nosaukums, daudzums, noliktava, kvalitate) VALUES(?, ?, ?, ?, ?)", (produkta_ID, produkta_nosaukums, daudzums, noliktava, kvalitate))
    conn.commit()
    if (daudzums < 10):
        messagebox.showinfo("Uzmanību!", "Mazs produkta daudzums noliktavā!")
    galvenais_logs_1()


def produkta_inventerizacija_ievade():
    clear_screen()
    
    # Ievades lauciņi produkta inventerizācijai
    tk.Label(screen, text="produkta ID (Tikai cipari)").pack(pady=5)
    global ievade_produkta_ID
    ievade_produkta_ID = tk.Entry(screen)
    ievade_produkta_ID.pack(pady=5)

    tk.Label(screen, text="produkta nosaukums").pack(pady=5)
    global ievade_produkta_nosaukums
    ievade_produkta_nosaukums = tk.Entry(screen)
    ievade_produkta_nosaukums.pack(pady=5)
    
    tk.Label(screen, text="produkta daudzums").pack(pady=5)
    global ievade_daudzums
    ievade_daudzums = tk.Entry(screen)
    ievade_daudzums.pack(pady=5)
    
    tk.Label(screen, text="Noliktava").pack(pady=10)
    global izvele_noliktava
    noliktava = ["Noliktava nr 1", "Noliktava nr 2", "Noliktava nr 3"]
    izvele_noliktava = tk.StringVar(screen)
    izvele_noliktava.set(noliktava[0])
    dropdown = tk.OptionMenu(screen, izvele_noliktava, *noliktava)
    dropdown.pack(pady=10)
    
    tk.Label(screen, text="Produkta kvalitāte").pack(pady=10)
    global izvele_kvalitate
    kvalitate = ["Augsta", "Vidēja", "Zema"]
    izvele_kvalitate = tk.StringVar(screen)
    izvele_kvalitate.set(kvalitate[0])
    dropdown = tk.OptionMenu(screen, izvele_kvalitate, *kvalitate)
    dropdown.pack(pady=10)

    # poga datu ievadīšanai
    tk.Button(screen, text="Ievadīt", command=produkta_inventerizacija).pack(pady=5)
    tk.Button(screen, text="Atpakaļ", command=galvenais_logs_1).pack(pady=40)



def produkta_redigesana():
    
    try:
        produkta_ID = int(jauns_ievade_produkta_ID.get())
        jauns_sarazotais_daudzums = int(jauns_ievade_sarazotais_daudzums.get())
        jauns_pardotais_daudzums = int(jauns_ievade_pardotais_daudzums.get())
        kvalitate = izvele_kvalitate.get()
    except ValueError:
        messagebox.showwarning("Kļūda!", "Lūdzu, ievadi korektas skaitliskas vērtības!")
        return

    cursor.execute("SELECT COUNT(*) FROM produkta_inventerizacija WHERE produkta_ID=?", (produkta_ID,)) 
    db_produkta_ID = cursor.fetchone()[0]
    if (db_produkta_ID != 0):
        if (kvalitate is not None):
            cursor.execute("UPDATE produkta_inventerizacija SET kvalitate=? WHERE produkta_ID=?", (kvalitate, produkta_ID))
            conn.commit()
            if (kvalitate == "Zema"):
                messagebox.showwarning("Uzmanību!", "Preces kvalitāte is zema!")
        if (jauns_sarazotais_daudzums is not None):
            cursor.execute("SELECT daudzums FROM produkta_inventerizacija WHERE produkta_ID=?", (produkta_ID,)) 
            db_daudzums = cursor.fetchone()[0]
            db_daudzums = db_daudzums + jauns_sarazotais_daudzums
            cursor.execute("UPDATE produkta_inventerizacija SET daudzums=? WHERE produkta_ID=?", (db_daudzums, produkta_ID))
            conn.commit()
        if (jauns_pardotais_daudzums is not None):
            cursor.execute("SELECT daudzums FROM produkta_inventerizacija WHERE produkta_ID=?", (produkta_ID,)) 
            db_daudzums = cursor.fetchone()[0]
            db_daudzums = db_daudzums - jauns_pardotais_daudzums
            if (db_daudzums >= 0):
                cursor.execute("UPDATE produkta_inventerizacija SET daudzums=? WHERE produkta_ID=?", (db_daudzums, produkta_ID))
                conn.commit()
                if (db_daudzums < 10):
                    messagebox.showinfo("Uzmanību!", "Mazs produkta daudzums noliktavā!")
                galvenais_logs_1()
            else:
                messagebox.showwarning("Kļūda!", "Nepietiekams produkta daudzums!")
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs produkta ID!")


def produkta_dzesana():
    
    produkta_ID = int(jauns_ievade_produkta_ID.get())
    cursor.execute("SELECT COUNT(*) FROM produkta_inventerizacija WHERE produkta_ID=?", (produkta_ID,))
    db_produkta_ID = cursor.fetchone()[0]
    if (db_produkta_ID != 0):
        cursor.execute("DELETE FROM produkta_inventerizacija WHERE produkta_ID=?", (produkta_ID,))
        conn.commit()
        galvenais_logs_1()
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs produkta ID!")


def produkta_redigesana_ievade():
    clear_screen()
    
    tk.Label(screen, text="produkta ID (Tikai cipari)").pack(pady=5)
    global jauns_ievade_produkta_ID
    jauns_ievade_produkta_ID = tk.Entry(screen)
    jauns_ievade_produkta_ID.pack(pady=5)

    tk.Label(screen, text="Saražotais produkta daudzums (Obligāti jāaizpilda)").pack(pady=5)
    global jauns_ievade_sarazotais_daudzums
    jauns_ievade_sarazotais_daudzums = tk.Entry(screen)
    jauns_ievade_sarazotais_daudzums.pack(pady=5)
    
    tk.Label(screen, text="Pārdotais produkta daudzums (Obligāti jāaizpilda)").pack(pady=5)
    global jauns_ievade_pardotais_daudzums
    jauns_ievade_pardotais_daudzums = tk.Entry(screen)
    jauns_ievade_pardotais_daudzums.pack(pady=5)
    
    tk.Label(screen, text="Produkta kvalitāte").pack(pady=10)
    global izvele_kvalitate
    kvalitate = ["Augsta", "Vidēja", "Zema"]
    izvele_kvalitate = tk.StringVar(screen)
    izvele_kvalitate.set(kvalitate[0])
    dropdown = tk.OptionMenu(screen, izvele_kvalitate, *kvalitate)
    dropdown.pack(pady=10)

    
    tk.Button(screen, text="Ievadīt izmaiņas", command=produkta_redigesana).pack(pady=5)
    tk.Button(screen, text="Dzēst produktu", command=produkta_dzesana).pack(pady=20)
    tk.Button(screen, text="Atpakaļ", command=galvenais_logs_1).pack(pady=20)
   
   
def izejvielu_inventerizacija():
    
    # Izejvielu inventerizācija
    try:
        izejvielas_ID = int(ievade_izejvielas_ID.get())
        izejviela = str(ievade_izejviela.get())
        daudzums = int(ievade_izejvielas_daudzums.get())
    except ValueError:
        messagebox.showwarning("Kļūda!", "Lūdzu, ievadi korektas skaitliskas vērtības!")
        return
    
    cursor.execute("INSERT INTO izejvielu_inventerizacija(izejvielas_ID, izejviela, daudzums) VALUES(?, ?, ?)", (izejvielas_ID, izejviela, daudzums))
    conn.commit()
    if (daudzums < 10):
        messagebox.showinfo("Uzmanību!", "Mazs produkta daudzums noliktavā!")
    galvenais_logs_1()
    

def izejvielu_inventerizacija_ievade():
    clear_screen()
    
    # Ievades lauciņi rezerves daļu inventerizācijai
    tk.Label(screen, text="Izejvielas ID (Tikai cipari)").pack(pady=5)
    global ievade_izejvielas_ID
    ievade_izejvielas_ID = tk.Entry(screen)
    ievade_izejvielas_ID.pack(pady=5)
    
    tk.Label(screen, text="Izejvielas nosaukums").pack(pady=5)
    global ievade_izejviela
    ievade_izejviela = tk.Entry(screen)
    ievade_izejviela.pack(pady=5)

    tk.Label(screen, text="Izejvielas daudzums").pack(pady=5)
    global ievade_izejvielas_daudzums
    ievade_izejvielas_daudzums = tk.Entry(screen)
    ievade_izejvielas_daudzums.pack(pady=5)

    # poga datu ievadīšanai
    tk.Button(screen, text="Ievadīt", command=izejvielu_inventerizacija).pack(pady=5)
    tk.Button(screen, text="Atpakaļ", command=galvenais_logs_1).pack(pady=40)


def izejvielu_redigesana():
    try:
        izejvielas_ID = int(ievade_izejvielas_ID.get())
        jauns_piegadatais_daudzums = int(jauns_ievade_piegadatais_daudzums.get())
        jauns_izmantotais_daudzums = int(jauns_ievade_izmantotais_daudzums.get())
    except ValueError:
        messagebox.showerror("Kļūda!", "Lūdzu, ievadi korektas skairliskas vērtības!")
    
    cursor.execute("SELECT COUNT(*) FROM izejvielu_inventerizacija WHERE izejvielas_ID=?", (izejvielas_ID,)) 
    db_izejvielas_ID = cursor.fetchone()[0]
    if (db_izejvielas_ID != 0):  
        if (jauns_piegadatais_daudzums is not None):
            cursor.execute("SELECT daudzums FROM izejvielu_inventerizacija WHERE izejvielas_ID=?", (izejvielas_ID,)) 
            db_daudzums = cursor.fetchone()[0]
            db_daudzums = db_daudzums + jauns_piegadatais_daudzums
            cursor.execute("UPDATE izejvielu_inventerizacija SET daudzums=? WHERE izejvielas_ID=?", (db_daudzums, izejvielas_ID))
            conn.commit()
        if (jauns_izmantotais_daudzums is not None):
            cursor.execute("SELECT daudzums FROM izejvielu_inventerizacija WHERE izejvielas_ID=?", (izejvielas_ID,)) 
            db_daudzums = cursor.fetchone()[0]
            db_daudzums = db_daudzums - jauns_izmantotais_daudzums
            if (db_daudzums >= 0):
                cursor.execute("UPDATE izejvielu_inventerizacija SET daudzums=? WHERE izejvielas_ID=?", (db_daudzums, izejvielas_ID))
                conn.commit()
                if (db_daudzums < 10):
                    messagebox.showinfo("Uzmanību!", "Mazs produkta daudzums noliktavā!")
                galvenais_logs_1()
            else:
                messagebox.showwarning("Kļūda!", "Nepietiekams izejvielas daudzums!")
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs izejvielas ID!")
    
    
def izejvielu_dzesana():
    
    izejvielas_ID = int(ievade_izejvielas_ID.get())
    cursor.execute("SELECT COUNT(*) FROM izejvielu_inventerizacija WHERE izejvielas_ID=?", (izejvielas_ID,))
    db_izejvielas_ID = cursor.fetchone()[0]
    if (db_izejvielas_ID !=0):
        cursor.execute("DELETE FROM izejvielu_inventerizacija WHERE izejvielas_ID=?", (izejvielas_ID,))
        conn.commit()
        galvenais_logs_1()
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs izejvielas ID!")


def izejvielu_redigesana_ievade():
    clear_screen()
    
    tk.Label(screen, text="Izejvielas ID (Tikai cipari)").pack(pady=5)
    global ievade_izejvielas_ID
    ievade_izejvielas_ID = tk.Entry(screen)
    ievade_izejvielas_ID.pack(pady=5)
    
    tk.Label(screen, text="Piegādātais izejvielu daudzums (Obligāti jāaizpilda)").pack(pady=5)
    global jauns_ievade_piegadatais_daudzums
    jauns_ievade_piegadatais_daudzums = tk.Entry(screen)
    jauns_ievade_piegadatais_daudzums.pack(pady=5)

    tk.Label(screen, text="Izmantotais izejvielu daudzums (Obligāti jāaizpilda)").pack(pady=5)
    global jauns_ievade_izmantotais_daudzums
    jauns_ievade_izmantotais_daudzums = tk.Entry(screen)
    jauns_ievade_izmantotais_daudzums.pack(pady=5)
    
    tk.Button(screen, text="Ievadīt izmaiņas", command=izejvielu_redigesana).pack(pady=5)
    tk.Button(screen, text="Dzēst izejvielu", command=izejvielu_dzesana).pack(pady=20)
    tk.Button(screen, text="Atpakaļ", command=galvenais_logs_1).pack(pady=20)


def tehnikas_inventerizacija():
    try:
        tehnikas_ID = int(ievade_tehnikas_ID.get())
        tehnikas_nosaukums = str(ievade_tehnikas_nosaukums.get())
        tehnikas_iegades_datums = str(ievade_tehnikas_iegades_datums.get())
        tehnikas_kludas = str(ievade_tehnikas_kludas.get())
    except ValueError:
        messagebox.showerror("Kļūda!", "Nepareizs datu formāts!")
    if (tehnikas_ID is not None and tehnikas_nosaukums is not None and tehnikas_iegades_datums is not None and tehnikas_kludas is not None):
        cursor.execute("INSERT INTO tehnikas_inventerizacija(tehnikas_ID, tehnikas_nosaukums, iegades_datums, kludas) VALUES=(?, ?, ?, ?)", (tehnikas_ID, tehnikas_nosaukums, tehnikas_iegades_datums, tehnikas_kludas))
        galvenais_logs_1()


def tehnikas_inventerizacija_ievade():
    clear_screen()
    
    tk.Label(screen, text="Tehnikas ID (tikai cipari)").pack(pady=5)
    global ievade_tehnikas_ID
    ievade_tehnikas_ID = tk.Entry(screen)
    ievade_tehnikas_ID.pack(pady=5)
    
    tk.Label(screen, text="Tehnikas nosaukums").pack(pady=5)
    global ievade_tehnikas_nosaukums
    ievade_tehnikas_nosaukums = tk.Entry(screen)
    ievade_tehnikas_nosaukums.pack(pady=5)
    
    tk.Label(screen, text="Tehnikas iegādes datums").pack(pady=5)
    global ievade_tehnikas_iegades_datums
    ievade_tehnikas_iegades_datums = tk.Entry(screen)
    ievade_tehnikas_iegades_datums.pack(pady=5)
    
    tk.Label(screen, text="Tehnikas iepriekšējās kļūdas").pack(pady=5)
    global ievade_tehnikas_kludas
    ievade_tehnikas_kludas = tk.Entry(screen)
    ievade_tehnikas_kludas.pack(pady=5)
    
    tk.Button(screen, text="Ievadīt", command=tehnikas_inventerizacija).pack(pady=5)
    tk.Button(screen, text="Atpakaļ", command=galvenais_logs_1).pack(pady=5)


def dzest_lietotaju():
    lietotaja_ID = int(ievade_administrators_lietotaja_ID.get())
    cursor.execute("SELECT COUNT(*) FROM autorizacija WHERE lietotaja_ID=?", (lietotaja_ID,))
    db_lietotaja_ID = cursor.fetchone()[0]
    if (db_lietotaja_ID !=0):
        cursor.execute("DELETE FROM autorizacija WHERE lietotaja_ID=?", (lietotaja_ID,))
        conn.commit()
        administrators()
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs lietotāja ID!")
    

def rediget_lomas():
    
    loma = izvele.get()
    administrators_lietotaja_ID = int(ievade_administrators_lietotaja_ID.get())
    cursor.execute("SELECT COUNT(*) FROM autorizacija WHERE lietotaja_ID=?", (administrators_lietotaja_ID,))
    db_administrators_lietotaja_ID = cursor.fetchone()[0]
    if (db_administrators_lietotaja_ID != 0):
        cursor.execute("UPDATE autorizacija SET loma=? WHERE lietotaja_ID=?", (loma, administrators_lietotaja_ID))
        conn.commit()
        administrators()
    else:
        messagebox.showerror("Kļūda!", "Tāds lietotāja ID neeksistē!")


def rediget_lomas_ievade():
    clear_screen()
    
    ## AUTORIZĀCIJAS TABULAS IZVEIDOŠANA
    # Iegūst datus no datubāzes
    cursor.execute("SELECT lietotaja_ID, loma, epasts FROM autorizacija")
    rows_admin = cursor.fetchall()
    
    tabula_admin = ttk.Treeview(screen, columns=("lietotaja_ID", "loma", "epasts"), show="headings")
    
    tabula_admin.heading("lietotaja_ID", text="Lietotāja ID")
    tabula_admin.heading("loma", text="Lietotāja loma")
    tabula_admin.heading("epasts", text="Lietotāja e-pasts")


    # Ievieto datus tabulā
    for row in rows_admin:
        tabula_admin.insert("", "end", values=row)
    
    tabula_admin.pack(padx=15, pady=10)
    
    tk.Label(screen, text="Lietotāja ID (Tikai cipari)").pack(pady=5)
    global ievade_administrators_lietotaja_ID
    ievade_administrators_lietotaja_ID = tk.Entry(screen)
    ievade_administrators_lietotaja_ID.pack(pady=5)
    
    tk.Label(screen, text="Jaunais piekļuves līmenis").pack(pady=5)
    global izvele
    lomas = ["lvl 1", "lvl 2"]
    izvele = tk.StringVar(screen)
    izvele.set(lomas[1])
    dropdown = tk.OptionMenu(screen, izvele, *lomas)
    dropdown.pack(pady=10)
    
    tk.Button(screen, text="Ievadīt", command=rediget_lomas).pack(pady=10)
    tk.Button(screen, text="Dzēst lietotāju", command=dzest_lietotaju).pack(pady=10)
    tk.Button(screen, text="Atpakaļ", command=administrators).pack(pady=10)


def bridinajums():
    bridinajums = ievade_bridinajums.get()
    numurs = int(ievade_bridinajuma_numurs.get())
    cursor.execute("INSERT INTO bridinajumi(bridinajums, nr) VALUES(?, ?)", (bridinajums, numurs))
    administrators()
    

def bridinajumu_dzesana():
    bridinajums = int(ievade_bridinajuma_numurs.get())
    cursor.execute("SELECT COUNT(*) FROM bridinajumi WHERE nr=?", (bridinajums,))
    db_bridinajums = cursor.fetchone()[0]
    if (db_bridinajums != 0):
        cursor.execute("DELETE FROM bridinajumi WHERE nr=?", (bridinajums,))
        conn.commit()
        administrators()
    else:
        messagebox.showwarning("Kļūda!", "Nepareizs numurs!")


def bridinajumu_ievade():
    clear_screen()
    
    tk.Label(screen, text="Brīdinājuma teksts").pack(pady=5)
    global ievade_bridinajums
    ievade_bridinajums = tk.Entry(screen)
    ievade_bridinajums.pack(pady=5)
    
    tk.Label(screen, text="Brīdinājuma numurs").pack(pady=5)
    global ievade_bridinajuma_numurs
    ievade_bridinajuma_numurs = tk.Entry(screen)
    ievade_bridinajuma_numurs.pack(pady=5)
    
    tk.Button(screen, text="Ievadīt", command=bridinajums).pack(pady=10)
    tk.Button(screen, text="Dzēst brīdinājumu", command=bridinajumu_dzesana).pack(pady=10)
    tk.Button(screen, text="Atpakaļ", command=administrators).pack(pady=10)



def galvenais_logs_1():
    clear_screen()

    ## SCROLLBAR
    main_frame = tk.Frame(screen, bg='silver') # fona krāsa
    main_frame.pack(expand=True, fill="both") # pack() izmanto, lai logā ievietotu main_frame ; rāmis aizņem visu pieejamo vietu vecāklogā
    canvas = tk.Canvas(main_frame, bg='silver') # fona krāsa
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview) # vertikāls scrollbar, kas saistīts ar canvas
    scrollable_frame = tk.Frame(canvas, bg='silver') # fona krāsa
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) # kad mainās frame izmērs (piem. daudz preču katalogā)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n") # "n" - north (augšā)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y") # scrollbar labajā pusē vertikāli
    canvas.configure(yscrollcommand=scrollbar.set) # saista canvas ritināšanu ar scrollbar pozīciju

    ## PRODUKTA TABULAS IZVEIDOŠANA
    # Iegūst datus no datubāzes
    cursor.execute("SELECT produkta_ID, produkta_nosaukums, daudzums, noliktava, kvalitate FROM produkta_inventerizacija")
    rows_produkts = cursor.fetchall()
    
    tabula_produkts = ttk.Treeview(scrollable_frame, columns=("produkta_ID", "produkta_nosaukums", "daudzums", "noliktava", "kvalitate"), show="headings")
    
    tabula_produkts.heading("produkta_ID", text="Produkta ID")
    tabula_produkts.heading("produkta_nosaukums", text="Produkta nosaukums")
    tabula_produkts.heading("daudzums", text="Produkta daudzums")
    tabula_produkts.heading("noliktava", text="Noliktava")
    tabula_produkts.heading("kvalitate", text="Produkta kvalitāte")

    # Ievieto datus tabulā
    for row in rows_produkts:
        tabula_produkts.insert("", "end", values=row)
    
    tabula_produkts.pack(padx=15, pady=10)
    
    tk.Button(scrollable_frame, text="Pievienot jaunu produktu", command=produkta_inventerizacija_ievade).pack(pady=5)
    tk.Button(scrollable_frame, text="Rediģēt produktu daudzumu", command=produkta_redigesana_ievade).pack(pady=5)
    
    ## IZEJVIELU TABULAS IZVEIDOŠANA
    # Iegūst datus no datubāzes
    cursor.execute("SELECT izejvielas_ID, izejviela, daudzums FROM izejvielu_inventerizacija")
    rows_izejvielas = cursor.fetchall()
    
    tabula_izejvielas = ttk.Treeview(scrollable_frame, columns=("izejvielas_ID", "izejviela", "daudzums"), show="headings")
    
    tabula_izejvielas.heading("izejvielas_ID", text="Izejvielas ID")
    tabula_izejvielas.heading("izejviela", text="Izejvielas nosaukums")
    tabula_izejvielas.heading("daudzums", text="Izejvielas daudzums")
  
    # Ievieto datus tabulā
    for row in rows_izejvielas:
        tabula_izejvielas.insert("", "end", values=row)
    
    tabula_izejvielas.pack(padx=15, pady=10)
    
    tk.Button(scrollable_frame, text="Pievienot jaunu izejvielu", command=izejvielu_inventerizacija_ievade).pack(pady=5)
    tk.Button(scrollable_frame, text="Rediģēt izejvielu daudzumu", command=izejvielu_redigesana_ievade).pack(pady=5)
    
    # TEHNIKAS INVENTERIZĀCIJA
    
    cursor.execute("SELECT tehnikas_ID, tehnikas_nosaukums, iegades_datums, kludas FROM tehnikas_inventerizacija")
    rows_tehnika = cursor.fetchall()
    
    tabula_tehnika = ttk.Treeview(scrollable_frame, columns=("tehnikas_ID", "tehnikas_nosaukums", "iegades_datums", "kludas"), show="headings")
    
    tabula_tehnika.heading("tehnikas_ID", text="Tehnikas ID")
    tabula_tehnika.heading("tehnikas_nosaukums", text="Tehnikas nosaukums")
    tabula_tehnika.heading("iegades_datums", text="Tehnikas iegādes datums")
    tabula_tehnika.heading("kludas", text="Tehnikas iepriekšējās kļūdas")

    # Ievieto datus tabulā
    for row in rows_tehnika:
        tabula_tehnika.insert("", "end", values=row)
    
    tabula_tehnika.pack(padx=15, pady=10)
    
    tk.Button(scrollable_frame, text="Pievienot jaunu tehniku", command=tehnikas_inventerizacija_ievade).pack(pady=5)
    
    # BRĪDINĀJUMI
    
    cursor.execute("SELECT bridinajums FROM bridinajumi")
    rows_bridinajumi = cursor.fetchall()
    tabula_izejvielas = ttk.Treeview(scrollable_frame, columns=("izejvielas_ID", "izejviela", "daudzums"), show="headings")
    tabula_bridinajumi = ttk.Treeview(scrollable_frame, columns=("bridinajums"), show="headings")
    
    tabula_bridinajumi.heading("bridinajums", text="Brīdinājumi")
    tabula_bridinajumi.column("bridinajums", width=1000)
  
    # Ievieto datus tabulā
    for row in rows_bridinajumi:
        tabula_bridinajumi.insert("", "end", values=row)
    
    tabula_bridinajumi.pack(padx=15, pady=10)
    
    tk.Button(scrollable_frame, text="Izrakstīties", command=autorizacijas_ievade).pack(pady=40)


def galvenais_logs_2():
    clear_screen()
    
     ## SCROLLBAR
    main_frame = tk.Frame(screen, bg='silver') # fona krāsa
    main_frame.pack(expand=True, fill="both") # pack() izmanto, lai logā ievietotu main_frame ; rāmis aizņem visu pieejamo vietu vecāklogā
    canvas = tk.Canvas(main_frame, bg='silver') # fona krāsa
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview) # vertikāls scrollbar, kas saistīts ar canvas
    scrollable_frame = tk.Frame(canvas, bg='silver') # fona krāsa
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) # kad mainās frame izmērs (piem. daudz preču katalogā)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n") # "n" - north (augšā)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y") # scrollbar labajā pusē vertikāli
    canvas.configure(yscrollcommand=scrollbar.set) # saista canvas ritināšanu ar scrollbar pozīciju

    ## PRODUKTA TABULAS IZVEIDOŠANA
    # Iegūst datus no datubāzes
    cursor.execute("SELECT produkta_ID, produkta_nosaukums, daudzums, noliktava, kvalitate FROM produkta_inventerizacija")
    rows_produkts = cursor.fetchall()
    
    tabula_produkts = ttk.Treeview(scrollable_frame, columns=("produkta_ID", "produkta_nosaukums", "daudzums", "noliktava", "kvalitate"), show="headings")
    
    tabula_produkts.heading("produkta_ID", text="Produkta ID")
    tabula_produkts.heading("produkta_nosaukums", text="Produkta nosaukums")
    tabula_produkts.heading("daudzums", text="Produkta daudzums")
    tabula_produkts.heading("noliktava", text="Noliktava")
    tabula_produkts.heading("kvalitate", text="Produkta kvalitāte")

    # Ievieto datus tabulā
    for row in rows_produkts:
        tabula_produkts.insert("", "end", values=row)
    
    tabula_produkts.pack(padx=15, pady=10)
    
    ## IZEJVIELU TABULAS IZVEIDOŠANA

    cursor.execute("SELECT izejvielas_ID, izejviela, daudzums FROM izejvielu_inventerizacija")
    rows_izejvielas = cursor.fetchall()
    
    tabula_izejvielas = ttk.Treeview(scrollable_frame, columns=("izejvielas_ID", "izejviela", "daudzums"), show="headings")
    
    tabula_izejvielas.heading("izejvielas_ID", text="Izejvielas ID")
    tabula_izejvielas.heading("izejviela", text="Izejvielas nosaukums")
    tabula_izejvielas.heading("daudzums", text="Izejvielas daudzums")
  
    # Ievieto datus tabulā
    for row in rows_izejvielas:
        tabula_izejvielas.insert("", "end", values=row)
    
    tabula_izejvielas.pack(padx=15, pady=10)
    
    cursor.execute("SELECT tehnikas_ID, tehnikas_nosaukums, iegades_datums, kludas FROM tehnikas_inventerizacija")
    rows_tehnika = cursor.fetchall()
    
    tabula_tehnika = ttk.Treeview(scrollable_frame, columns=("tehnikas_ID", "tehnikas_nosaukums", "iegades_datums", "kludas"), show="headings")
    
    tabula_tehnika.heading("tehnikas_ID", text="Tehnikas ID")
    tabula_tehnika.heading("tehnikas_nosaukums", text="Tehnikas nosaukums")
    tabula_tehnika.heading("iegades_datums", text="Tehnikas iegādes datums")
    tabula_tehnika.heading("kludas", text="Tehnikas iepriekšējās kļūdas")

    # Ievieto datus tabulā
    for row in rows_tehnika:
        tabula_tehnika.insert("", "end", values=row)
    
    tabula_tehnika.pack(padx=15, pady=10)
    
    ## BRĪDINĀJUMI
    
    cursor.execute("SELECT bridinajums FROM bridinajumi")
    rows_bridinajumi = cursor.fetchall()
    tabula_bridinajumi = ttk.Treeview(scrollable_frame, columns=("bridinajums"), show="headings")
    
    tabula_bridinajumi.heading("bridinajums", text="Brīdinājumi")
    tabula_bridinajumi.column("bridinajums", width=1000)
  
    # Ievieto datus tabulā
    for row in rows_bridinajumi:
        tabula_bridinajumi.insert("", "end", values=row)
    
    tabula_bridinajumi.pack(padx=15, pady=10)
    
    tk.Button(scrollable_frame, text="Izrakstīties", command=autorizacijas_ievade).pack(pady=10)
    
    
def administrators():
    clear_screen()
    
    ## SCROLLBAR
    main_frame = tk.Frame(screen, bg='silver') # fona krāsa
    main_frame.pack(expand=True, fill="both") # pack() izmanto, lai logā ievietotu main_frame ; rāmis aizņem visu pieejamo vietu vecāklogā
    canvas = tk.Canvas(main_frame, bg='silver') # fona krāsa
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview) # vertikāls scrollbar, kas saistīts ar canvas
    scrollable_frame = tk.Frame(canvas, bg='silver') # fona krāsa
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) # kad mainās frame izmērs (piem. daudz preču katalogā)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n") # "n" - north (augšā)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y") # scrollbar labajā pusē vertikāli
    canvas.configure(yscrollcommand=scrollbar.set) # saista canvas ritināšanu ar scrollbar pozīciju
    
    ## PRODUKTA TABULAS IZVEIDOŠANA
    # Iegūst datus no datubāzes
    cursor.execute("SELECT produkta_ID, produkta_nosaukums, daudzums, noliktava, kvalitate FROM produkta_inventerizacija")
    rows_produkts = cursor.fetchall()
    
    tabula_produkts = ttk.Treeview(scrollable_frame, columns=("produkta_ID", "produkta_nosaukums", "daudzums", "noliktava", "kvalitate"), show="headings")
    
    tabula_produkts.heading("produkta_ID", text="Produkta ID")
    tabula_produkts.heading("produkta_nosaukums", text="Produkta nosaukums")
    tabula_produkts.heading("daudzums", text="Produkta daudzums")
    tabula_produkts.heading("noliktava", text="Noliktava")
    tabula_produkts.heading("kvalitate", text="Produkta kvalitāte")

    # Ievieto datus tabulā
    for row in rows_produkts:
        tabula_produkts.insert("", "end", values=row)
    
    tabula_produkts.pack(padx=15, pady=10)
    
    ## IZEJVIELU TABULAS IZVEIDOŠANA
    # Iegūst datus no datubāzes
    cursor.execute("SELECT izejvielas_ID, izejviela, daudzums FROM izejvielu_inventerizacija")
    rows_izejvielas = cursor.fetchall()
    
    tabula_izejvielas = ttk.Treeview(scrollable_frame, columns=("izejvielas_ID", "izejviela", "daudzums"), show="headings")
    
    tabula_izejvielas.heading("izejvielas_ID", text="Izejvielas ID")
    tabula_izejvielas.heading("izejviela", text="Izejvielas nosaukums")
    tabula_izejvielas.heading("daudzums", text="Izejvielas daudzums")
  
    # Ievieto datus tabulā
    for row in rows_izejvielas:
        tabula_izejvielas.insert("", "end", values=row)
    
    tabula_izejvielas.pack(padx=15, pady=10)
    
    # TEHNIKAS INVENTERIZĀCIJA
    
    cursor.execute("SELECT tehnikas_ID, tehnikas_nosaukums, iegades_datums, kludas FROM tehnikas_inventerizacija")
    rows_tehnika = cursor.fetchall()
    
    tabula_tehnika = ttk.Treeview(scrollable_frame, columns=("tehnikas_ID", "tehnikas_nosaukums", "iegades_datums", "kludas"), show="headings")
    
    tabula_tehnika.heading("tehnikas_ID", text="Tehnikas ID")
    tabula_tehnika.heading("tehnikas_nosaukums", text="Tehnikas nosaukums")
    tabula_tehnika.heading("iegades_datums", text="Tehnikas iegādes datums")
    tabula_tehnika.heading("kludas", text="Tehnikas iepriekšējās kļūdas")

    # Ievieto datus tabulā
    for row in rows_tehnika:
        tabula_tehnika.insert("", "end", values=row)
    
    tabula_tehnika.pack(padx=15, pady=10)
    
    # BRĪDINĀJUMI
    
    cursor.execute("SELECT bridinajums, nr FROM bridinajumi")
    rows_bridinajumi = cursor.fetchall()
    tabula_bridinajumi = ttk.Treeview(scrollable_frame, columns=("bridinajums", "nr"), show="headings")
    
    tabula_bridinajumi.heading("bridinajums", text="Brīdinājumi")
    tabula_bridinajumi.column("bridinajums", width=800)
    tabula_bridinajumi.heading("nr", text="Brīdinājuma numurs")
    tabula_bridinajumi.column("nr", width=200)
  
    # Ievieto datus tabulā
    for row in rows_bridinajumi:
        tabula_bridinajumi.insert("", "end", values=row)
    
    tabula_bridinajumi.pack(padx=15, pady=10)
    
    tk.Button(scrollable_frame, text="Rediģēt brīdinājumus", command=bridinajumu_ievade).pack(pady=5)
    tk.Button(scrollable_frame, text="Rediģēt lietotāju lomas", command=rediget_lomas_ievade).pack(pady=10)
    tk.Button(scrollable_frame, text="Izrakstīties", command=autorizacijas_ievade).pack(pady=10)
    
screen = tk.Tk()
screen.title("produkta pārvaldības sistēma")
screen.configure(bg='silver')
tk.Label(screen, text="produkta pārvaldes sistēma", font=("Helvetica", 13)).pack(pady=5)

scrollbar = Scrollbar(screen)
autorizacijas_ievade()

screen.mainloop()
conn.close()