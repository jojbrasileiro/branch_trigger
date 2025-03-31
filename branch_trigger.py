import requests
import time

# Configurações
GITHUB_TOKEN = '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'
OWNER = 'jojbrasileiro'
REPO = 'branch_trigger'
BRANCH_ALVO = 'main'

API_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=closed&per_page=100'

print(API_URL)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

vistos = set()

while True:
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        prs = response.json()
        for pr in prs:
            if pr['merged_at'] is not None and pr['base']['ref'] == BRANCH_ALVO:
                pr_id = pr['id']
                if pr_id not in vistos:
                    vistos.add(pr_id)
                    print(f"Merge detectado na branch {BRANCH_ALVO}!")
                    print(f"{pr['head']['ref']} → {pr['base']['ref']}")
                    print(f"Título: {pr['title']}")
                    print(f"Por: {pr['user']['login']}")
                    print("---")
    else:
        print(f"❌ Erro ao consultar API: {response.status_code}")
    
    time.sleep(60)