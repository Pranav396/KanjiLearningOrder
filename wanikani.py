import requests
import json

token = ''
headers = {'Authorization': f'Bearer {token}'}

def fetch(url, headers):
    results = []
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        results.extend(data['data'])
        url = data['pages']['next_url']
    return results

# Fetch radicals.
print('Fetching radicals...')
radicals = fetch('https://api.wanikani.com/v2/subjects?types=radical', headers)

radical_lookup = {}
for radical in radicals:
    radical_lookup[radical['id']] = radical['data']['meanings'][0]['meaning']

# Fetch kanji.
print('Fetching kanji...')
kanji_raw = fetch('https://api.wanikani.com/v2/subjects?types=kanji', headers)

kanji_data = []
for kanji in kanji_raw:
    kanji_data.append({
        'character': kanji['data']['characters'],
        'wk_level': kanji['data']['level'],
        'radical_ids': kanji['data']['component_subject_ids'],
        'radical_names': [radical_lookup[id] for id in kanji['data']['component_subject_ids']]
    })

# Save to files.
with open('wk_kanji.json', 'w', encoding='utf-8') as f:
    json.dump(kanji_data, f, ensure_ascii=False, indent=2)

print(f'Done. {len(kanji_data)} kanji saved.')