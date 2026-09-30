"""Outils de l'exercice « Charriage sur l'Arbogne » (bedload-exercise.ipynb).

Ce fichier contient tout le code technique de l'exercice : lecture des
résultats HEC-RAS, formule de Meyer-Peter & Müller (1948), contrôle des
réponses et figures. Il n'est pas nécessaire de le lire pour faire
l'exercice ; le notebook l'importe avec ``import charriage as ch``
(ou ``from fun import charriage as ch`` dans jupyter-python-course).

Fichiers nécessaires, dans le même dossier ou selon la structure de
jupyter-python-course (fun/charriage.py et data/hecras-arbogne.csv) :
    charriage.py          ce script
    hecras-arbogne.csv    16 profils HEC-RAS 1D de l'Arbogne, Q = 25 m3/s
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ------------------------------------------------------------- constantes ---
G = 9.81          # accélération de la pesanteur [m/s2]
RHO_S = 2680.0    # masse volumique des grains [kg/m3]
RHO_W = 1000.0    # masse volumique de l'eau [kg/m3]
S = RHO_S / RHO_W # densité relative [-]
NU = 1e-6         # viscosité cinématique de l'eau [m2/s]

DOSSIER = Path(__file__).resolve().parent
# CSV à côté du script, sinon dans ../data/ (structure de jupyter-python-course)
HECRAS = next((p for p in (DOSSIER / "hecras-arbogne.csv",
                           DOSSIER.parent / "data" / "hecras-arbogne.csv")
               if p.exists()), DOSSIER / "hecras-arbogne.csv")

# Palette du cours (hydro-informatics.com) pour axes et textes ; les scénarios
# gardent les couleurs Okabe-Ito de la présentation (lisibles par les daltoniens).
NAVY, BLUE, CYAN, GREEN, WARN, GREY = (
    "#0C0C48", "#00467F", "#00CAEF", "#167D61", "#C74B2A", "#4A4A4C",
)
COULEURS_KST = ["#0072B2", "#D55E00", "#E69F00", "#56B4E9", "#F0E442"]
COULEUR_D84 = "#CC79A7"
SYMBOLE_GRAIN = {"gravier": "o", "sable": "^"}   # diagramme de Shields : symbole = grain
FOND = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9)  # fond des étiquettes

plt.rcParams.update({
    "figure.figsize": (8.4, 4.8),
    "figure.dpi": 110,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.labelcolor": NAVY,
    "axes.edgecolor": NAVY,
    "text.color": NAVY,
    "xtick.color": NAVY,
    "ytick.color": NAVY,
    "font.size": 9,
})


# ---------------------------------------------------------------- données ---
def lire_hecras(fichier=HECRAS):
    """Résultats HEC-RAS des 16 profils (Q = 25 m3/s), de l'amont vers l'aval."""
    return pd.read_csv(fichier).sort_values("profil").reset_index(drop=True)


A_COMPLETER = ">>> COMPLETER"   # texte des endroits à compléter dans le notebook


def _vide(v):
    """True si v est encore à compléter (texte « >>> COMPLETER » ou « ... »)."""
    return v is None or v is Ellipsis or isinstance(v, str)


def _complet(*valeurs):
    """False tant qu'une des valeurs est encore à compléter."""
    return not any(_vide(v) for v in np.ravel(np.array(valeurs, dtype=object)))


def _granulometrie(melanges):
    """{nom: {"d_m": .., "d_84": .., "d_90": ..}} en mètres, à partir de [nom, d_m, d_84, d_90] en mm.

    d_84 et d_90 ne sont nécessaires que pour le lit (le dernier mélange de la liste)."""
    if not all(_complet(*m[1:]) for m in melanges):
        raise ValueError("Tâche 1 : complétez d'abord les diamètres de la liste « melanges ».")
    if len(melanges[-1]) < 4:
        raise ValueError("Tâche 1 : le lit (dernier mélange) demande d_m, d_84 et d_90.")
    return {m[0]: {k: float(v) / 1000.0 for k, v in zip(("d_m", "d_84", "d_90"), m[1:])}
            for m in melanges}


def _verifier_k_st(k_st):
    if not _complet(*k_st):
        raise ValueError("Tâche 1 : complétez d'abord la liste « k_st ».")


def rugosite_grain(melanges):
    """k_r = 26 / d_90^(1/6) avec d_90 [m] du lit, soit le dernier mélange de la liste
    (Meyer-Peter & Müller 1948, éq. 25)."""
    d90_lit = list(_granulometrie(melanges).values())[-1]["d_90"]
    return 26.0 / d90_lit ** (1 / 6)


# -------------------------------------------------------------------- MPM ---
def tau_etoile(Rh, Je, d):
    """Contrainte de cisaillement adimensionnelle tau* = Rh Je / ((s - 1) d)."""
    return Rh * Je / ((S - 1) * d)


def phi_mpm(tau, k_prime, tau_cr):
    """Charriage adimensionnel de Meyer-Peter & Müller (1948)."""
    return 8.0 * np.maximum(k_prime * tau - tau_cr, 0.0) ** 1.5


def nom_rugosite(i, n):
    """Nom du i-ème cas de rugosité sur n. Le premier k_st : écoulement dans le lit
    en gravier, sans végétation ; le dernier : crue débordante dans la plaine
    inondable densément végétalisée ; les éventuels cas intermédiaires : A, B, ..."""
    if i == 0:
        return "sans végétation (écoulement dans le lit)"
    if i == n - 1:
        return "avec végétation (crue débordante)"
    return f"avec végétation {chr(64 + i)}"


def scenarios(melanges, k_st):
    """Liste des scénarios (grain, rugosité, diamètre [m], k_st, symbole, couleur).

    Chaque cas de rugosité (k_st, le premier sans végétation, le dernier avec la
    végétation dense de la plaine inondable) est calculé pour le
    gravier et pour le sable (d_m). Le lit pavé (d_84 du gravier) est ajouté pour
    le cas sans végétation."""
    _verifier_k_st(k_st)
    gr = _granulometrie(melanges)
    sable, lit = list(gr.values())[0], list(gr.values())[-1]
    liste = []
    for grain, d in (("gravier", lit["d_m"]), ("sable", sable["d_m"])):
        for i, k in enumerate(k_st):
            liste.append((f"{grain.capitalize()} d_m", nom_rugosite(i, len(k_st)), d, k,
                          SYMBOLE_GRAIN[grain], COULEURS_KST[i % len(COULEURS_KST)]))
    liste.append(("Gravier d_84 (lit pavé)", nom_rugosite(0, len(k_st)), lit["d_84"], k_st[0],
                  "s", COULEUR_D84))
    return liste


def calculer(melanges, k_st, tau_cr, rapport_rugosite):
    """MPM sur les 16 profils pour chaque scénario et chaque tau*_cr.

    Retourne un tableau (DataFrame) avec une ligne par profil et par calcul."""
    sec = lire_hecras()
    k_r = rugosite_grain(melanges)
    lignes = []
    for tcr in tau_cr:
        for grain, rugosite, d, k, symbole, couleur in scenarios(melanges, k_st):
            kp = rapport_rugosite(k, k_r)
            if _vide(kp):
                raise ValueError("Tâche 2 : complétez d'abord la fonction rapport_rugosite.")
            tau = tau_etoile(sec.Rh_m, sec.Je, d)
            phi = phi_mpm(tau, kp, tcr)
            lignes.append(pd.DataFrame({
                "grain": grain, "rugosite": rugosite, "profil": sec.profil, "d_mm": d * 1000, "k_st": k,
                "k_r": k_r, "k_prime": kp, "tau_cr": tcr, "tau": tau,
                "tau_eff": kp * tau,
                # vitesse de frottement des grains u*' = (k' g Rh Je)^0.5
                "Re": np.sqrt(kp * G * sec.Rh_m * sec.Je) * d / NU,
                "Phi": phi,
                "qb_kg_sm": phi * np.sqrt((S - 1) * G * d ** 3) * RHO_S,
                "symbole": symbole, "couleur": couleur,
            }))
    return pd.concat(lignes, ignore_index=True)


def resume(res):
    """Nombre de profils qui transportent encore (Phi > 0), par scénario."""
    tab = (res.assign(actif=res.Phi > 0)
              .groupby(["tau_cr", "grain", "rugosite"], sort=False)
              .agg(**{"d [mm]": ("d_mm", "first"), "k_st": ("k_st", "first"),
                      "k'": ("k_prime", "first"), "profils actifs": ("actif", "sum"),
                      "Phi max": ("Phi", "max"), "q_b max [kg/(s m)]": ("qb_kg_sm", "max")}))
    tab["profils actifs"] = tab["profils actifs"].astype(str) + " / 16"
    if res.tau_cr.nunique() == 1:
        tab = tab.droplevel("tau_cr")
    return tab.round({"d [mm]": 2, "k'": 3, "Phi max": 4, "q_b max [kg/(s m)]": 4})


# --------------------------------------------------------------- contrôle ---
def verifier(melanges, k_st, rapport_rugosite, k_st_critique, tol=0.02):
    """Compare les réponses aux valeurs de la présentation. [OK] = juste."""
    def ligne(texte, valeur, attendu):
        if _vide(valeur):
            print(f"[  ] {texte:<52} pas encore complété")
            return
        ok = abs(valeur - attendu) <= tol * abs(attendu)
        print(f"[{'OK' if ok else 'XX'}] {texte:<52} {valeur:9.3f}   (attendu {attendu:.3f})")

    try:
        gr = list(_granulometrie(melanges).values())
        ligne("Tâche 1  d_m du sable [mm]", gr[0]["d_m"] * 1000, 0.23)
        ligne("Tâche 1  d_m du gravier [mm]", gr[-1]["d_m"] * 1000, 8.88)
        ligne("Tâche 1  d_84 du gravier [mm]", gr[-1]["d_84"] * 1000, 13.56)
        ligne("Tâche 1  d_90 du gravier [mm]", gr[-1]["d_90"] * 1000, 23.06)
        ligne("         k_r = 26 / d_90^(1/6) [m^(1/3)/s]", rugosite_grain(melanges), 48.7)
    except ValueError:
        ligne("Tâche 1  diamètres caractéristiques", None, 0)
    if _complet(k_st):
        ligne("Tâche 1  k_st sans végétation", k_st[0], 42)
        ligne("Tâche 1  k_st avec végétation", k_st[-1], 8)
    else:
        ligne("Tâche 1  k_st", None, 0)
    ligne("Tâche 2  rapport_rugosite(42, 48.7)", rapport_rugosite(42, 48.7), 0.80090)
    ligne("Tâche 3  k_st_critique(0.05, 48.7, 0.047)", k_st_critique(0.05, 48.7, 0.047), 46.732)


# ---------------------------------------------------------------- figures ---
def _tau_cr_ref(tau_cr):
    """Seuil des marqueurs et des valeurs imprimées : 0.047 (MPM) s'il est dans la liste."""
    return 0.047 if 0.047 in tau_cr else tau_cr[0]


def shields_guo(Re):
    """Courbe de Shields critique, forme de Guo (2002)."""
    return 0.11 / Re + 0.054 * (1 - np.exp(-4 * Re ** 0.52 / 25))


def diagramme_shields(res):
    """Diagramme de Shields : contrainte efficace sur les grains k' tau* en
    fonction de Re*. Taille des marqueurs : une décade de Phi par classe."""
    tau_cr = sorted(res.tau_cr.unique())
    tcr0 = _tau_cr_ref(tau_cr)
    # comparaison rugosité x grain : gravier et sable en d_m (le lit pavé d_84 n'y figure pas)
    sub = res[(res.tau_cr == tcr0) & res.grain.isin(["Gravier d_m", "Sable d_m"])]
    phi_max = sub.Phi.max()
    # classe 0 : Phi = 0 ; classes 1 à 5 : une décade chacune sous Phi_max
    cls = np.where(sub.Phi > 0,
                   np.clip(5 - np.floor(-np.log10(np.maximum(sub.Phi, 1e-30) / phi_max)), 1, 5), 0)
    taille = np.array([12, 22, 40, 70, 110, 160])[cls.astype(int)]

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    Re = np.logspace(0, 4, 300)
    courbe, = ax.plot(Re, shields_guo(Re), "k--", lw=1.6, zorder=2)
    if len(tau_cr) > 1:
        for t in tau_cr:
            ax.axhline(t, color=GREY, lw=0.7, ls=":", zorder=1)
            ax.annotate(rf"$\tau_{{*,cr}}$ = {t:g}", (1.1, t), fontsize=7, color=GREY, va="bottom")
    # du plus lisse au plus rugueux : les points « sans végétation » restent visibles
    for (grain, rugosite), s in sub.groupby(["grain", "rugosite"], sort=False):
        m = ((sub.grain == grain) & (sub.rugosite == rugosite)).to_numpy()
        ax.scatter(s.Re, s.tau_eff, s=taille[m], marker=s.symbole.iloc[0],
                   color=s.couleur.iloc[0], edgecolor="#1A1A1A", linewidths=0.4, zorder=3)
    # étiquette directe à côté du point le plus chargé de chaque grain
    for grain, g in sub.groupby("grain", sort=False):
        p = g.loc[g.tau_eff.idxmax()]
        ax.annotate(f"{grain.split()[0].lower()}, $d_m$ = {p.d_mm:.2f} mm".replace(".", ","),
                    (p.Re, p.tau_eff), xytext=(10, 0), textcoords="offset points",
                    va="center", fontsize=8, fontweight="bold", color=NAVY)
    # deux légendes : couleur = rugosité, symbole = grain
    cas = sub.drop_duplicates("rugosite")
    h_rug = [plt.Line2D([], [], ls="", marker="s", ms=8, color=r.couleur, mec="#1A1A1A", mew=0.4,
                        label=f"{r.rugosite}, $k_{{st}}$ = {r.k_st:g}") for r in cas.itertuples()]
    h_grain = [plt.Line2D([], [], ls="", marker=SYMBOLE_GRAIN[g.split()[0].lower()], ms=8,
                          color="#BFBFBF", mec="#1A1A1A", mew=0.4, label=f"{g}")
               for g in sub.grain.unique()]
    h_grain.append(plt.Line2D([], [], ls="--", color="k", lw=1.6, label=r"$\tau_{*,cr}$, Guo (2002)"))
    leg1 = ax.legend(handles=h_rug, title="couleur : rugosité", fontsize=7.5, title_fontsize=7.5,
                     loc="upper right", framealpha=0.95, alignment="left")
    ax.add_artist(leg1)
    ax.legend(handles=h_grain, title="symbole : grain", fontsize=7.5, title_fontsize=7.5,
              loc="upper center", framealpha=0.95, alignment="left")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1e4)
    ax.set_ylim(1e-3, 1e2)
    ax.set_xlabel(r"Nombre de Reynolds particulaire des grains $Re_*$ [-]")
    ax.set_ylabel(r"Contrainte efficace sur les grains $k'\,\tau_*$ [-]")
    ax.set_title(rf"Arbogne, Q = 25 m$^3$/s : 16 profils (MPM, $\tau_{{*,cr}}$ = {tcr0:g})")
    ax.grid(True, which="major", ls="--", lw=0.5, color="#A6A6A6")
    ax.grid(True, which="minor", ls=":", lw=0.4, color="#D0D0D0")
    ax.annotate("taille du marqueur : une décade de $\\Phi$ par classe\n"
                "sous la courbe : $\\Phi$ = 0", (0.01, 0.01), xycoords="axes fraction",
                fontsize=7.5, color=GREY)
    fig.tight_layout()
    plt.show()


def profils_actifs(melanges, k_st, tau_cr, k_st_critique):
    """Nombre de profils qui transportent encore quand k_st diminue (végétation,
    débordement). Un profil transporte tant que k_st > k_st,cr."""
    _verifier_k_st(k_st)
    sec = lire_hecras()
    k_r = rugosite_grain(melanges)
    gr = _granulometrie(melanges)
    sable, lit = list(gr.values())[0], list(gr.values())[-1]
    k_axe = np.arange(max(60.0, 1.5 * max(k_st)), 0.8 * min(k_st), -0.25)
    tcr0 = _tau_cr_ref(tau_cr)

    fig, ax = plt.subplots(figsize=(8.4 if len(tau_cr) == 1 else 11.0, 4.6))
    styles = ["-", "--", "-.", ":", (0, (5, 1))]
    extinction = {}
    for j, tcr in enumerate(tau_cr):
        for nom, texte, d, col, dy in (
                ("$d_m$ (transit, apport amont)", "d_m  (transit)", lit["d_m"], "#440154", 30),
                ("$d_{84}$ (lit en place, pavage)", "d_84 (pavage)", lit["d_84"], "#21918C", 12)):
            k_cr = np.array([k_st_critique(t, k_r, tcr) for t in tau_etoile(sec.Rh_m, sec.Je, d)])
            if _vide(k_cr[0]):
                raise ValueError("Tâche 3 : complétez d'abord la fonction k_st_critique.")
            n = [(k > k_cr).sum() for k in k_axe]
            lab = nom + (rf", $\tau_{{*,cr}}$ = {tcr:g}" if len(tau_cr) > 1 else "")
            ax.plot(k_axe, n, lw=2.2, color=col, ls=styles[j % len(styles)], label=lab)
            # extinction totale : k_st,cr du profil le plus raide
            ke = float(k_cr.min())
            extinction[(texte, tcr)] = ke
            if tcr == tcr0:
                ax.plot([ke], [0], marker="v", ms=9, color=col, clip_on=False)
                ax.annotate(f"extinction totale, $k_{{st}}$ = {ke:.1f}", (ke, 0),
                            xytext=(-8, dy), textcoords="offset points", ha="right",
                            fontsize=7.5, color=col, fontweight="bold",
                            arrowprops=dict(arrowstyle="-", color=col, lw=0.8))
    for i, k in enumerate(k_st):
        col = COULEURS_KST[i % len(COULEURS_KST)]
        lab = nom_rugosite(i, len(k_st)).replace(" (", "\n(")
        ax.axvline(k, color=col, ls="--", lw=1.4)
        ax.annotate(f"{lab}\n$k_{{st}}$ = {k:g}", (k, 18.8), ha="center", va="top",
                    fontsize=7.5, color=col, fontweight="bold", bbox=FOND)
    e0 = [v for (n, t), v in extinction.items() if t == tcr0]
    ax.axvspan(min(e0), max(e0), color=WARN, alpha=0.10, lw=0)
    ax.annotate("fenêtre critique", (np.mean(e0), 6.6), ha="center", fontsize=8,
                color=WARN, style="italic")
    ax.invert_xaxis()   # la végétation fait baisser k_st : vers la droite
    ax.set_xlabel(r"Rugosité de Strickler $k_{st}$ [m$^{1/3}$/s]   (la végétation augmente vers la droite)")
    ax.set_ylabel("profils qui transportent encore\n(sur 16)")
    ax.set_ylim(-0.8, 19.5)
    ax.set_yticks(range(0, 17, 2))
    ax.grid(True, ls=":", lw=0.5)
    if len(tau_cr) == 1:
        ax.legend(fontsize=8, loc="lower left", title_fontsize=8,
                  title=rf"gravier, $\tau_{{*,cr}}$ = {tcr0:g}")
    else:
        ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.01, 0.5),
                  title="gravier", title_fontsize=8)
    fig.tight_layout()
    plt.show()

    ke_sable = k_st_critique(tau_etoile(sec.Rh_m, sec.Je, sable["d_m"]).max(), k_r, tcr0)
    print(f"Extinction totale (tau*_cr = {tcr0:g}) : plus aucun profil ne transporte si")
    for (nom, t), v in extinction.items():
        if t == tcr0:
            print(f"   gravier {nom:<16} k_st < {v:5.1f}")
    print(f"   sable   {'d_m  (apport)':<16} k_st < {ke_sable:5.1f}")
