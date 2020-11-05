import json
import requests

def index(id: str):
    jsonbody = json.dumps({
        'id': id,
    })
    response = requests.post(url='http://192.168.56.101:30007/function/tot-indexer',auth=('developer', 'developer'),
                             data=jsonbody, headers={'content-type': 'application/json'})
    return response.json()

documents = [
    "f426787d-7ebd-4449-9ff3-d8ba64396051",
    "d0a07016-c5a2-4e25-9e07-9c9b1b86d4e4",
    "eff8b54e-ebc5-4a8a-a115-fee662162a8e",
    "e16f47fb-7831-4d87-b682-cfe104417845",
    "def2b6e5-7123-44ec-b4de-e29fe3808cfe",
    "d93d6909-2a94-4329-80e7-de4d1c7a1d29",
    "c9c2948e-6afb-424c-8f58-e90dc6ff23da",
    "a9f40b37-8f80-4054-8a9b-4bd9ee18e4cb",
    "cecda4cb-dc44-42d7-9a79-290df11a234f",
    "b2a62d28-cbeb-4157-a2e1-37bac434a695",
    "d5aebb04-a341-4ce5-a72a-c4bdb025a6b9",
    "cb83ba9f-fbfc-4ee7-95ef-4104a7246e03",
    "c70db2a1-f98a-4ec9-8af1-6781a67a423f",
    "8935a3ee-315a-498a-bf18-385ec4d09a69",
    "bcc65cba-8327-4e05-896a-20296c5ee747",
    "7032b6dc-6705-4135-95e3-6f888b065e56",
    "05298d72-1b4c-4dfb-ba89-a70dc07f6f50",
    "1294eda7-794a-4679-914f-78b3119fa94d",
    "7a7ef0ff-744f-477b-bced-3bf2871c664f",
    "893d0254-0253-46f5-acfc-f63edc072c5f",
    "8ab8ebb9-0edb-48b1-9531-b513463330cd",
    "620f0455-5fc8-4475-b627-fdaaf24f08ce",
    "1ca7a9ae-cae8-4994-9e2d-264f6b36aea1",
    "61f7521b-abe6-4fb4-9a74-ab42dfa481e8",
    "36fb5cac-b33d-459a-836a-7e8e3cb4ee26",
    "317cb92b-a3cb-436e-8eff-a3fa9cf0a212",
    "53f0a3bc-6013-4e57-aa87-e933faa969cb",
    "8ed959d0-088b-4bbd-8f3c-9f3732acf7e1",
    "28fe3cea-4afe-46d6-b78d-fd97f0a2942b",
    "22df19bb-ac89-4246-9833-9a771a76baac",
    "7d1c9c89-f39f-4fbe-b8ee-abc8142f1c1a",
    "015efcb1-e5bc-4899-b107-7ec8f02d9be3",
    "1e9c2359-634e-45be-bb26-df30632423cd",
    "1fe3e31a-196a-4372-9e36-e5fbe3b6d978",
    "7a6083f6-5051-4797-bf47-c7ca8029e01f",
    "1b85af69-7f0a-4632-b7c3-5eb08d832626",
    "0a7b5db2-a21b-454e-88b6-6cf4e26a87bc", ]

for a in documents:
    print(index(a))