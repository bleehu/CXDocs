""" we use this when we use player input to check postgres for a search. For instance, we don't want 
           badguys trying to log in with SQL injection - that could lead to damage to login data."""
def sql_escape(dirty):
    #string.replace(new, old)
    sani = dirty.replace('*','')
    sani = sani.replace('=','')
    sani = sani.replace('>','')
    sani = sani.replace('<','')
    sani = sani.replace(';','')
    sani = sani.replace("'","''")
    #sani = sani.replace("\\", "\\") #need a way to sanitize backslashes for escape characters
    return sani