import math  # Beimportálja a matematikai modulokat (pl. végtelen - math.inf használatához a Minimaxhoz).
import random  # Beimportálja a véletlenszám-generáló modult a könnyű nehézségi szintű bot lépéseihez.


def nyomtatas(tabla):
    """Megjeleníti a játéktáblát a konzolon."""
    print("\n  0   1   2")  # Kiírja az oszlopok indexeit a táblázat tetejére.
    for i in range(3):  # Végigmegy a tábla sorain (0, 1, 2).
        print(f"{i} " + " | ".join(tabla[i]))  # Kiírja a sorszámot, majd az adott sor elemeit elválasztva.
        if i < 2:  # Ha még nem az utolsó sorban vagyunk...
            print("  ---------")  # ...akkor kirajzol egy elválasztó vonalat a sorok közé.
    print()  # Egy üres sor a jobb áttekinthetőségért.


def gyozelem_ellenorzes(tabla, jatekos):
    """Ellenőrzi, hogy a megadott játékos (X vagy O) nyert-e."""
    for i in range(3):  # Végigmegy a sorokon és oszlopokon.
        if all(tabla[i][j] == jatekos for j in range(3)):  # Ha az `i`-edik sor összes eleme a játékosé:
            return True  # Akkor a játékos győzelmét jelzi (Igaz).
        if all(tabla[j][i] == jatekos for j in range(3)):  # Ha az `i`-edik oszlop összes eleme a játékosé:
            return True  # Akkor győzelem.

    # Főátló ellenőrzése bal fentről jobb lefelé (0,0 -> 1,1 -> 2,2).
    if (
        tabla[0][0] == jatekos
        and tabla[1][1] == jatekos
        and tabla[2][2] == jatekos
    ):
        return True

    # Mellékátló ellenőrzése jobb fentről bal lefelé (0,2 -> 1,1 -> 2,0).
    if (
        tabla[0][2] == jatekos
        and tabla[1][1] == jatekos
        and tabla[2][0] == jatekos
    ):
        return True

    return False  # Ha egyik feltétel sem teljesült, senki sem nyert még ebben a körben.


def szabad_mezok(tabla):
    """Visszaadja egy listában az összes még üres mező koordinátáját (sor, oszlop)."""
    return [
        (r, c) for r in range(3) for c in range(3) if tabla[r][c] == " "
    ]  # Végigpörgatja a táblát, és gyűjti a " "-hellyel rendelkező cellákat.


def minimax(tabla, depth, is_maximizing):
    """
    Minimax algoritmus a verhetetlen AI-hoz.
    Kiszámolja az összes lehetséges jövőbeli kimenetelt, hogy a legbölcsebb lépést válassza.
    """
    if gyozelem_ellenorzes(tabla, "O"):  # Ha a gép nyerne ebben a szimulációban:
        return 10 - depth  # Pozitív pontszám (minél kevesebb lépésből, annál jobb).
    if gyozelem_ellenorzes(tabla, "X"):  # Ha az ember nyerne:
        return depth - 10  # Negatív pontszám (a gép szempontjából rossz).
    if not szabad_mezok(tabla):  # Ha elfogytak a mezők (döntetlen):
        return 0  # Semleges pontszám.

    if is_maximizing:  # Ha a gép (O) köre van (a maximálásra törekszik):
        best_score = -math.inf  # Kezdetben beállítja a legrosszabb lehetséges pontszámra.
        for r, c in szabad_mezok(tabla):  # Végigmegy az összes szabad mezőn.
            tabla[r][c] = "O"  # Ideiglenesen beírja a gép jelét.
            score = minimax(
                tabla, depth + 1, False
            )  # Rekurzívan hívja az ember körére.
            tabla[r][c] = " "  # Visszaállítja üresre a mezőt (backtracking).
            best_score = max(
                score, best_score
            )  # Kiválasztja a maximális pontszámot.
        return best_score  # Visszaadja a legjobb pontot.
    else:  # Ha az ember (X) köre van (a gép minimalizálni próbálja az ember esélyét):
        best_score = math.inf  # Kezdetben végtelenre állítja.
        for r, c in szabad_mezok(tabla):  # Végigmegy az összes szabad mezőn.
            tabla[r][c] = "X"  # Ideiglenesen beírja az ember jelét.
            score = minimax(tabla, depth + 1, True)  # Rekurzív hívás a gép körére.
            tabla[r][c] = " "  # Visszaállítja üresre a mezőt.
            best_score = min(
                score, best_score
            )  # Kiválasztja a minimális (gépnek rosszabb) pontszámot.
        return best_score  # Visszaadja a legkisebb pontot.


def gep_lepes(tabla, nehezseg):
    """Kiválasztja a gép következő lépését a nehézségi szint alapján."""
    szabad = szabad_mezok(tabla)  # Lekéri az elérhető üres mezőket.

    if nehezseg == "1":  # Ha a könnyű módot választották:
        return random.choice(szabad)  # Véletlenszerűen választ egyet a szabad mezők közül.
    else:  # Ha a nehéz (verhetetlen) módot választották:
        best_score = -math.inf  # Kiinduló pontszám.
        best_move = None  # Kiinduló lépés koordináta.
        for r, c in szabad:  # Végigmegy a szabad mezőkön.
            tabla[r][c] = "O"  # Kipróbálja a lépést.
            score = minimax(tabla, 0, False)  # Kiszámoltatja a Minimax-szal.
            tabla[r][c] = " "  # Visszaállítja az eredeti állapotot.
            if score > best_score:  # Ha ez a lépés jobb az eddigieknél:
                best_score = score  # Elmenti az új legjobb pontot.
                best_move = (r, c)  # Elmenti az új legjobb lépést.
        return best_move  # Visszaadja a legjobb koordinátát.


def amoba_ai():
    """A fő játékhurok (game loop), ami összefogja a játék menetét."""
    tabla = [[" " for _ in range(3)] for _ in range(3)]  # Létrehoz egy üres, 3x3-as mátrixot.

    print("=== AMŐBA JÁTÉK GÉP ELLEN ===")  # Címsor kiírása.
    print("Módok:")
    print("1 - Könnyű (Véletlenszerű lépések)")
    print("2 - Verhetetlen (Minimax AI)")

    nehezseg = ""  # Létrehoz egy üres változót a nehézségnek.
    while nehezseg not in ["1", "2"]:  # Addig kérdez, amíg érvényes választ nem kap.
        nehezseg = input("Válassz nehézséget (1 vagy 2): ").strip()  # Bekéri a nehézséget, levágja a felesleges szóközöket.

    ember = "X"  # Az emberi játékos jele.
    gep = "O"  # A gép jele.
    aktualis_jatekos = "X"  # Mindig az ember kezdi a játékot.

    while True:  # Végtelen ciklus a játék végéig.
        nyomtatas(tabla)  # Kirajzolja a tábla aktuális állását.

        if aktualis_jatekos == ember:  # Ha az ember következik:
            while True:  # Belső ciklus az érvényes emberi lépéshez.
                try:  # Hibakezelés kezdete (ha nem számot ad meg).
                    bejovo = input("Saját lépésed (sor oszlop, pl. 1 1): ")  # Bekéri a koordinátákat.
                    sor, oszlop = map(
                        int, bejovo.split()
                    )  # Szétválasztja a szöveget és egésszé alakítja.

                    if (
                        0 <= sor <= 2 and 0 <= oszlop <= 2
                    ):  # Ha a számok 0 és 2 között vannak:
                        if (
                            tabla[sor][oszlop] == " "
                        ):  # És az a mező még üres:
                            tabla[sor][oszlop] = ember  # Beírja az ember jelét.
                            break  # Kilép a belső bekérő ciklusból.
                        else:
                            print("⚠️ Ez a mező már foglalt!")  # Hibaüzenet, ha foglalt.
                    else:
                        print("⚠️ A számoknak 0 és 2 között kell lenniük!")  # Hibaüzenet, ha túl kicsi/nagy.
                except ValueError:  # Ha betűt vagy rossz formátumot adott meg:
                    print("⚠️ Érvénytelen formátum! Adja meg a sort és oszlopot (pl. 0 2).")
        else:  # Ha a gép következik:
            print("🤖 A gép gondolkodik...")  # Üzenet a gép lépése előtt.
            sor, oszlop = gep_lepes(tabla, nehezseg)  # Meghatározza a gép lépését.
            tabla[sor][oszlop] = gep  # Beírja a gép jelét a táblára.
            print(f"🤖 A gép ide lépett: {sor} {oszlop}")  # Kiírja, hova lépett a gép.

        if gyozelem_ellenorzes(
            tabla, aktualis_jatekos
        ):  # Ha az aktuális játékos nyert ebben a körben:
            nyomtatas(tabla)  # Kirajzolja a végső táblát.
            if aktualis_jatekos == ember:
                print("🎉 Gratulálok! Legyőzted a gépet!")
            else:
                print("💻 A gép nyert! Próbáld újra!")
            break  # Kilép a fő játékciklusból (vége a játéknak).

        if not szabad_mezok(tabla):  # Ha már nincsenek szabad mezők:
            nyomtatas(tabla)  # Kirajzolja a táblát.
            print("🤝 Döntetlen!")  # Kiírja, hogy döntetlen.
            break  # Kilép a játékból.

        aktualis_jatekos = (
            gep if aktualis_jatekos == ember else ember
        )  # Játékosváltás (ha X volt, O lesz; ha O volt, X lesz).


if __name__ == "__main__":
    amoba_ai()  # Csak akkor indítja el a programot, ha közvetlenül ezt a fájlt futtatják.