import hashlib

def choisir(ids,job,precedente=None,demande=None):
    if len(ids)!=4 or len(set(ids))!=4 or not job or (precedente is not None and precedente not in ids): raise ValueError('État ou catalogue invalide')
    pool=[i for i in ids if i!=precedente]
    if demande is not None:
        if demande not in pool:raise ValueError('Piste non autorisée ou identique au dernier succès')
        return demande
    return pool[int.from_bytes(hashlib.sha256(job.encode()).digest()[:8],'big')%len(pool)]
