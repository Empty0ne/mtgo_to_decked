#This is the original script found here:  https://gist.github.com/apetresc/9fcc264886a9e051e695
#Python version 2.7 is needed to run
#just run 'python mtgo_to_decked.py /path/to/MTGOv4.csv' and it will out the Decked Builder .coll file.


from collections import defaultdict
import csv
import os
import sys

set_map = {
	'ARB': 'Alara Reborn',
	'ALL': 'Alliances',
	'AQ': 'Antiquities',
	'AP': 'Apocalypse',
	'AN': 'Arabian Nights',
	'AVR': 'Avacyn Restored',
	'BOK': 'Betrayers of Kamigawa',
	'BNG': 'Born of the Gods',
	'CHK': 'Champions of Kamigawa',
	'6E': 'Classic Sixth Edition',
	'CSP': 'Coldsnap',
	'C13': 'Commander 2013 Edition',
	'CON': 'Conflux',
	'DKA': 'Dark Ascension',
	'DST': 'Darksteel',
	'DIS': 'Dissension',
	'DGM': 'Dragon\'s Maze',
	'DDH': 'Duel Decks: Ajani vs. Nicol Bolas',
	'DDC': 'Duel Decks: Divine vs. Demonic',
	'DDF': 'Duel Decks: Elspeth vs. Tezzeret',
	'EVG': 'Duel Decks: Elves vs. Goblins',
	'DDD': 'Duel Decks: Garruk vs. Liliana',
	'DDL': 'Duel Decks: Heroes vs. Monsters',
	'DDJ': 'Duel Decks: Izzet vs. Golgari',
	'DD2': 'Duel Decks: Jace vs. Chandra',
	'DDM': 'Duel Decks: Jace vs. Vraska',
	'DDG': 'Duel Decks: Knights vs. Dragons',
	'DDE': 'Duel Decks: Phyrexia vs. the Coalition',
	'DDK': 'Duel Decks: Sorin vs. Tibalt',
	'DDI': 'Duel Decks: Venser vs. Koth',
	'8ED': 'Eight Edition',
	'EVE': 'Eventide',
	'EX': 'Exodus',
	'FE': 'Fallen Empires',
	'5DN': 'Fifth Dawn',
	'5E': 'Fifth Edition',
	'4E': 'Fourth Edition',
	'DRB': 'From the Vault: Dragons',
	'V09': 'From the Vault: Exiled',
	'V11': 'From the Vault: Legends',
	'V12': 'From the Vault: Realms',
	'V10': 'From the Vault: Relics',
	'V13': 'From the Vault: Twenty',
	'FUT': 'Future Sight',
	'GTC': 'Gatecrash',
	'GPT': 'Guildpact',
	'HM': 'Homelands',
	'ICE': 'Ice Age',
	'ISD': 'Innistrad',
	'IN': 'Invasion',
	'JOU': 'Journey into Nyx',
	'JUD': 'Judgment',
	'LE': 'Legends',
	'LGN': 'Legions',
	'1E': 'Limited Edition Alpha',
	'2E': 'Limited Edition Beta',
	'LRW': 'Lorwyn',
	'M10': 'Magic 2010',
	'M11': 'Magic 2011',
	'M12': 'Magic 2012',
	'M13': 'Magic 2013',
	'M14': 'Magic 2014 Core Set',
	'M15': 'Magic 2015 Core Set',
	'CMD': 'Magic: The Gathering-Commander',
	'MED': 'Master\'s Edition',
	'ME2': 'Master\'s Edition II',
	'ME3': 'Master\'s Edition III',
	'ME4': 'Master\'s Edition IV',
	'MM': 'Mercadian Masques',
	'MI': 'Mirage',
	'MRD': 'Mirrodin',
	'MBS': 'Mirrodin Besieged',
	'MMA': 'Modern Masters',
	'MOR': 'Morningtide',
	'NE': 'Nemesis',
	'NPH': 'New Phyrexia',
	'9ED': 'Ninth Edition',
	'OD': 'Odyssey',
	'ONS': 'Onslaught',
	'PLC': 'Planar Chaos',
	'PC1': 'Planechase',
	'PC2': 'Planechase 2012 Edition',
	'PS': 'Planeshift',
	'PD2': 'Premium Deck Series: Fire and Lightning',
	'PD3': 'Premium Deck Series: Graveborn',
	'H09': 'Premium Deck Series: Slivers',
	'PR': 'Prophecy',
	'RAV': 'Ravnica: City of Guilds',
	'RTR': 'Return to Ravnica',
	'3E': 'Revised Edition',
	'ROE': 'Rise of the Eldrazi',
	'SOK': 'Saviors of Kamigawa',
	'SOM': 'Scars of Mirrodin',
	'SCG': 'Scourge',
	'7E': 'Seventh Edition',
	'SHM': 'Shadowmoor',
	'ALA': 'Shards of Alara',
	'ST': 'Stronghold',
	'TE': 'Tempest',
	'10E': 'Tenth Edition',
	'DK': 'The Dark',
	'THS': 'Theros',
	'TSP': 'Time Spiral',
	'TSB': 'Time Spiral \"Timeshifted\"',
	'TOR': 'Torment',
	'2U': 'Unlimited Edition',
	'UD': 'Urza\'s Destiny',
	'UL': 'Urza\'s Legacy',
	'UZ': 'Urza\'s Saga',
	'VMA': 'Vintage Masters',
	'VI': 'Visions',
	'WL': 'Weatherlight',
	'WWK': 'Worldwake',
	'ZEN': 'Zendikar'
}

filtered_cards = ['Event Ticket', 'Phantom Point']
filtered_sets = ['PRM', 'DPA']

cards = defaultdict(int)

def filter_card(name, set_name):
    return not (name in filtered_cards or name.startswith('Avatar - ') or
            name.endswith(' Booster') or set_name in filtered_sets)

def escape_name(name):
    return name.replace('\xc3\x86', 'Ae').replace('/', ' // ')

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fin:
        reader = csv.reader(fin)
        next(reader, None)
        for row in reader:
            if filter_card(escape_name(row[0]), row[4]):
                cards[(escape_name(row[0]), set_map[row[4]])] += int(row[1])

    with open('%s.coll' % os.path.splitext(sys.argv[1])[0], 'w') as fout:
        for (card_name, card_set), qty in cards.items():
            fout.write('%s %s [%s]\n' % (qty, card_name, card_set))
