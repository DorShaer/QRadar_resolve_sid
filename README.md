# QRadar_resolve_sid
This code is designed for security integrators working with qradar
## The following code is just a small project I did in order to resolve a username from SID number using 
## LDAP Queries.

This repo contains 2 files, as their names; one is resolving the username from SID and then adding the username to a Doamin Admins reference set.
the second will resolve username from SID and then remove it from the Domain Admins reference set.

ADD_USER:

If the user is in the refernce set the script will just resolve the username and it will not do anything.
If the user is not in the reference set it will resolve the username and then add it to Domain Admins reference set

REMOVE_USER:

If the user is in the refernce set the script will just resolve the username and it will not do anything.
If the user is not in the reference set it will resolve the username and then it will remove the user from the Domain Admins reference set.

Attention to the script comments! If you want the script to work you need to follow those steps:

1. Create Domain Admins reference set (can be any name you want)
2. Generate a SEC key
3. Have a domain user & password

While creating the Custom Action you will have to enter those 5 keys in this order: 

1. Host
2. Key
3. domainUserName
4. domainPassword
5. Reference set 

