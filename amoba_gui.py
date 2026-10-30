import random  # Beimportálja a véletlenszám-generáló modult (a gép véletlenszerű döntéseihez).
import tkinter as tk  # Beimportálja a Tkinter grafikus könyvtárat, és 'tk'-ként hivatkozik rá.
from tkinter import messagebox  # Beimportálja a felugró üzenetablakokat (pl. győzelem, döntetlen jelzésére).


class Amoba5x5App:  # Létrehozza az Amőba alkalmazás objektumorientált osztályát.
  def __init__(self, root):  # A konstruktor metódus, ami lefut a program indításakor.
    self.root = root  # Eltárolja a főablak objektumot.
    self.root.title("Amőba 5x5 - Gép Ellen")  # Beállítja az ablak címsorát.
    self.root.resizable(False, False)  # Letiltja az ablak átméretezését (fix méretű marad).

    self.meret = 5  # Meghatározza a játéktábla méretét (5x5-ös lesz).
    self.nyero_hossz = (
        4  # Enyéb szabály: 4 azonos jel kell egy sorban a győzelemhez.
    )

    self.ember = "X"  # Az emberi játékos jele (szimbóluma).
    self.gep = "O"  # A gép (AI) jele.
    self.aktualis_jatekos = "X"  # Mindig az ember kezdi a játékot.
    self.tabla = [["" for _ in range(self.meret)] for _ in range(self.meret)]  # Létrehoz egy 5x5-ös üres tömböt a táblának.
    self.gombok = [
        [None for _ in range(self.meret)] for _ in range(self.meret)
    ]  # Létrehozza a gomboknak szánt 5x5-ös mátrixot.

    self.letrehozo_felulet()  # Meghívja a grafikus felépítő függvényt.

  def letrehozo_felulet(self):
    """Létrehozza a grafikus elemeket (címke, rács, gombok)."""
    self.statusz_label = tk.Label(
        self.root,
        text="Te jössz! (X) - Szerezz 4-et egy sorban!",
        font=("Arial", 14, "bold"),
        pady=10,
    )  # Létrehoz egy szöveges sávot a játékállás jelzésére a tetején.
    self.statusz_label.grid(
        row=0, column=0, columnspan=self.meret
    )  # Elhelyezi a státuszcímkét a rács legtetején, kinyújtva az 5 oszlopon.

    # 5x5-ös rács generálása a gomboknak
    for r in range(self.meret):  # Végigmegy a sorokon (0-tól 4-ig).
      for c in range(self.meret):  # Végigmegy az oszlopokon (0-tól 4-ig).
        gomb = tk.Button(
            self.root,
            text="",
            font=("Arial", 18, "bold"),
            width=3,
            height=1,
            command=lambda row=r, col=c: self.ember_kattintas(row, col),
        )  # Létrehoz egy kattintható gombot, és ráköti az ember kattintás eseményét a koordinátákkal.
        gomb.grid(row=r + 1, column=c, padx=3, pady=3)  # Elhelyezi a gombot a rácsban (az 1. sortól kezdve).
        self.gombok[r][c] = gomb  # Eltárolja a gomb hivatkozását a mátrixban.

    # Új játék gomb az alján
    uj_jatek_gomb = tk.Button(
        self.root,
        text="Új Játék",
        font=("Arial", 11),
        command=self.uj_jatek,
        bg="#e0e0e0",
    )  # Létrehoz egy "Új Játék" gombot a tábla alatt.
    uj_jatek_gomb.grid(
        row=self.meret + 1,
        column=0,
        columnspan=self.meret,
        sticky="we",
        padx=4,
        pady=10,
    )  # Elhelyezi és kinyújtja a gombot a tábla alján.

  def ember_kattintas(self, r, c):
    """Kezeli, amikor az emberi játékos rákattint egy mezőre."""
    if (
        self.aktualis_jatekos == self.ember
        and self.tabla[r][c] == ""
        and not self.jatek_vege()
    ):  # Csak akkor léphet, ha az ő köre van, üres a mező, és nincs vége a játéknak.
      self.lepes_vegrehajtasa(r, c, self.ember)  # Végrehajtja és megjeleníti a lépést.

      if self.ellenoriz_gyozelmet(self.tabla, self.ember):  # Ha az ember nyert:
        messagebox.showinfo("Játék vége", "🎉 Gratulálok! Legyőzted a gépet!")  # Győzelmi üzenet.
        self.uj_jatek()  # Új játék indítása.
        return
      elif self.dontetlen():  # Ha döntetlen van:
        messagebox.showinfo("Játék vége", "🤝 Döntetlen!")  # Döntetlen üzenet.
        self.uj_jatek()
        return

      # Gép körének átadása
      self.aktualis_jatekos = self.gep  # Átállítja a játékost a gépre.
      self.statusz_label.config(text="A gép gondolkodik... 🤖")  # Kiírja, hogy a gép gondolkodik.
      self.root.after(400, self.gep_kattintas)  # 0.4 másodperc késleltetés után meghívja a gép lépését.

  def gep_kattintas(self):
    """A gép automatikus lépését vezérli."""
    if self.jatek_vege():  # Ha vége a játéknak, kilép.
      return

    r, c = self.okos_gep_lepes()  # Kéri az AI-tól a legjobb koordinátákat.
    if r is not None and c is not None:  # Ha talált érvényes lépést:
      self.lepes_vegrehajtasa(r, c, self.gep)  # Beírja a gép jelét.

      if self.ellenoriz_gyozelmet(self.tabla, self.gep):  # Ha a gép nyert:
        messagebox.showinfo("Játék vége", "💻 A gép nyert! Próbáld újra később.")  # Vereség üzenet.
        self.uj_jatek()
        return
      elif self.dontetlen():  # Ha döntetlen:
        messagebox.showinfo("Játék vége", "🤝 Döntetlen!")
        self.uj_jatek()
        return

    # Vissza az embernek a kör
    self.aktualis_jatekos = self.ember  # Visszaállítja a játékost az emberre.
    self.statusz_label.config(
        text="Te jössz! (X) - Szerezz 4-et egy sorban!"
    )  # Frissíti a státuszszöveget.

  def lepes_vegrehajtasa(self, r, c, jatekos):
    """Beírja a jelet a memóriába és átszínezi a gombot a felületen."""
    self.tabla[r][c] = jatekos  # Beírja a tábla adatstruktúrájába a jelet ('X' vagy 'O').
    szin = "blue" if jatekos == self.ember else "red"  # Ember kék, gép piros színű lesz.
    self.gombok[r][c].config(
        text=jatekos, fg=szin
    )  # Frissíti a gomb szövegét és szövegszínét a felületen.

  def szabad_mezok(self):
    """Visszaadja egy listában az összes üres cella koordinátáját."""
    return [
        (r, c)
        for r in range(self.meret)
        for c in range(self.meret)
        if self.tabla[r][c] == ""
    ]  # Végigpörgatja a táblát, és kigyűjti a nem üres helyeket.

  # --- Okos 5x5 Heurisztikus AI ---
  def okos_gep_lepes(self):
    """Kiszámolja a gép legokosabb lépését az 5x5-ös táblán."""
    szabad = self.szabad_mezok()  # Lekéri a szabad mezőket.
    if not szabad:
      return None, None

    # 1. Ha a gép nyerhet egy lépésből, azonnal megteszi
    for r, c in szabad:
      self.tabla[r][c] = self.gep  # Kipróbálja a gép helyét.
      if self.ellenoriz_gyozelmet(self.tabla, self.gep):  # Ha ezzel nyer:
        self.tabla[r][c] = ""  # Visszaállítja az ideiglenes értéket.
        return r, c  # Visszaadja a nyerő koordinátát.
      self.tabla[r][c] = ""  # Különben visszaállítja.

    # 2. Ha az ember nyerhetne a következőben, a gép blokkolja azt
    for r, c in szabad:
      self.tabla[r][c] = self.ember  # Kipróbálja, ha az ember lépne ide.
      if self.ellenoriz_gyozelmet(self.tabla, self.ember):  # Ha az ember nyeremne:
        self.tabla[r][c] = ""  # Visszaállítja.
        return r, c  # Visszaadja a blokkolandó koordinátát.
      self.tabla[r][c] = ""  # Különben visszaállítja.

    # 3. Egyébként pontozza a mezőket pozíció és szomszédok alapján
    legjobb_pont = -999  # Kezdeti minimális pontszám.
    legjobb_lepesek = []  # Létrehoz egy listát a legjobb lépéseknek.

    for r, c in szabad:  # Végigmegy az összes szabad mezőn.
      pontszam = 0  # Nullázza a pontszámot.
      pontszam += 4 - abs(r - 2) - abs(c - 2)  # Előnyben részesíti a tábla közepét.

      # Megvizsgálja a környező (szomszédos) mezőket
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if dr == 0 and dc == 0:
            continue
          nr, nc = r + dr, c + dc
          if 0 <= nr < self.meret and 0 <= nc < self.meret:
            if self.tabla[nr][nc] == self.gep:
              pontszam += 3  # Ha ott van a gép saját jele, kap plusz pontot.
            elif self.tabla[nr][nc] == self.ember:
              pontszam += 1  # Ha ott az ember jele, az is értékes.

      if pontszam > legjobb_pont:  # Ha ez a pontszám nagyobb az eddigieknél:
        legjobb_pont = pontszam  # Frissíti a legjobb pontot.
        legjobb_lepesek = [(r, c)]  # Új listát kezd ezzel a lépéssel.
      elif pontszam == legjobb_pont:  # Ha egyenlő a pontszám:
        legjobb_lepesek.append((r, c))  # Hozzáadja a meglévőkhöz.

    return random.choice(legjobb_lepesek)  # Véletlenszerűen választ egyet a legjobb pontszámú lépések közül.

  def ellenoriz_gyozelmet(self, tabla, jatekos):
    """Ellenőrzi, hogy van-e 4 egyforma jel egymás mellett (sorban, oszlopban vagy átlóban)."""
    n = self.meret
    wl = self.nyero_hossz

    # Sorok ellenőrzése
    for r in range(n):
      for c in range(n - wl + 1):
        if all(tabla[r][c + i] == jatekos for i in range(wl)):
          return True

    # Oszlopok ellenőrzése
    for c in range(n):
      for r in range(n - wl + 1):
        if all(tabla[r + i][c] == jatekos for i in range(wl)):
          return True

    # Főátlók ellenőrzése (\)
    for r in range(n - wl + 1):
      for c in range(n - wl + 1):
        if all(tabla[r + i][c + i] == jatekos for i in range(wl)):
          return True

    # Mellékátlók ellenőrzése (/)
    for r in range(n - wl + 1):
      for c in range(wl - 1, n):
        if all(tabla[r + i][c - i] == jatekos for i in range(wl)):
          return True

    return False  # Ha nincs meg a 4-es sorozat, hamisat ad vissza.

  def dontetlen(self):
    """Megvizsgálja, hogy tele van-e a tábla, azaz döntetlen van-e."""
    return all(
        self.tabla[r][c] != ""
        for r in range(self.meret)
        for c in range(self.meret)
    )  # Igazat ad vissza, ha már nincsenek üres mezők.

  def jatek_vege(self):
    """Eldönti, hogy véget ért-e a játék (győzelem vagy döntetlen)."""
    return (
        self.ellenoriz_gyozelmet(self.tabla, self.ember)
        or self.ellenoriz_gyozelmet(self.tabla, self.gep)
        or self.dontetlen()
    )

  def uj_jatek(self):
    """Alaphelyzetbe állítja a táblát és a felületet egy új játékhoz."""
    self.tabla = [["" for _ in range(self.meret)] for _ in range(self.meret)]  # Üresre tiszta mátrix.
    self.aktualis_jatekos = self.ember  # Újra az ember kezdi.
    self.statusz_label.config(
        text="Te jössz! (X) - Szerezz 4-et egy sorban!"
    )  # Visszaállítja a státusz szövegét.
    for r in range(self.meret):
      for c in range(self.meret):
        self.gombok[r][c].config(
            text="", fg="black"
        )  # Kiüríti a gombok feliratát és színét az ablakon.


if __name__ == "__main__":
  root = tk.Tk()  # Létrehozza a Tkinter alapablak példányát.
  app = Amoba5x5App(root)  # Példányosítja az amőba alkalmazásunkat a root ablakkal.
  root.mainloop()  # Elindítja a grafikus eseményhurok futtatását, hogy az ablak életben maradjon.