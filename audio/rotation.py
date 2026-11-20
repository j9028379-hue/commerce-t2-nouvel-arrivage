import hashlib

def choisir(ids,job,precedente=None,demande=None):
 last,requested,job_id=precedente,demande,job
 if not job_id or len(ids)!=4 or len(set(ids))!=4 or (last is not None and last not in ids):raise ValueError('Catalogue ou état de rotation invalide')
 suivant=ids[0] if last is None else ids[(ids.index(last)+1)%4]
 if requested is not None and requested!=suivant:raise ValueError('Seule la prochaine piste du cycle est autorisée')
 return suivant
