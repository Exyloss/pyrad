#!/usr/bin/env python3

import subprocess
from tabulate import tabulate

from m3u import *
from audio import *
from browser import *

command = "bemenu -l 10"
m3u_file = "/home/antonin/.config/pyrad/radios.m3u"

def prompt_sel(args, items, prompt=""):
    """
    Fonction permettant à l'utilisateur d'interagir avec son menu depuis python
    args: commande sous forme de tableau, chaque élément représente un "mot" de la fonction
    items: liste des valeurs à afficher
    """
    if prompt != "":
        args.append("-p")
        args.append(prompt)
    if items != "":
        try:
            proc = subprocess.Popen(
                args,
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        except OSError as err:
            print("erreur lors du lancement du menu")

        with proc.stdin:
            if isinstance(items, list):
                for item in items:
                    proc.stdin.write(item)
                    proc.stdin.write('\n')
            elif isinstance(items, str):
                proc.stdin.write(items)
    else:
        proc = subprocess.Popen(args)

    if proc.wait() == 0:
        return proc.stdout.read().rstrip('\n')

    stderr = proc.stderr.read()

    if stderr == '':
        return -1

while True:
    items = ["1) Afficher les favoris", "2) Rechercher une radio", "3) Supprimer une radio des favoris", "4) Arrêter le lecteur", "5) Quitter"]
    rep = prompt_sel(command.split(" "), items, "Accueil")
    if rep == -1 or rep.startswith("5)"):
        quit()

    elif rep.startswith("1)"):
        radios = parse_radios(m3u_file)
        favorites = tabulate([[i['name'], i['url']] for i in radios], tablefmt="plain").split("\n")
        while True:
            radio = prompt_sel(command.split(" "), favorites)
            if radio == -1:
                break
            url = radio.split(" ")[-1]
            play(url)

    elif rep.startswith("2)"):
        query = prompt_sel(command.split(" "), [], "Recherche>")
        if query == -1:
            continue
        results = search_radio(query)
        prompt_results = tabulate([[i['name'], f"{i['codec']}:{i['bitrate']}kbps", i["url"], i['stationuuid']] for i in results], tablefmt="plain").split("\n")
        choise = prompt_sel(command.split(" "), prompt_results, "Résultats:")
        if choise == -1:
            continue
        uuid = choise.split(" ")[-1]
        result = []
        for i in results:
            if i["stationuuid"] == uuid:
                result = i
                break
        while True:
            result_tab = [
                ["Ajouter aux favoris", ""      ],
                ["Lire la radio", ""            ],
                ["Nom:",   i['name']            ],
                ["UUID:",  uuid                 ],
                ["URL:",   i['url'],            ],
                ["Codec:", i['codec'],          ],
                ["Débit:", f"{i['bitrate']}kbps"],
            ]
            result_tab = tabulate(result_tab, tablefmt="plain").split("\n")
            choise = prompt_sel(command.split(" "), result_tab)
            if choise == -1:
                break
            elif choise == "Lire la radio":
                play(result["url"])
            elif choise == "Ajouter aux favoris":
                append_radio(m3u_file, i["name"], i["url"], uuid)

    elif rep.startswith("3)"):
        radios = parse_radios(m3u_file)
        favorites = tabulate([[i['name'], i['url'], i['uuid']] for i in radios], tablefmt="plain").split("\n")
        while True:
            radio = prompt_sel(command.split(" "), favorites)
            if radio == -1:
                break
            yes_no = prompt_sel(command.split(" "), ["Oui", "Non"], "Supprimer ?")
            if yes_no == "Oui":
                uuid = radio.split(" ")[-1]
                remove_radio(m3u_file, uuid)

    elif rep.startswith("4)"):
        stop()
