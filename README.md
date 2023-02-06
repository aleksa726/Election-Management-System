# Election-Management-System
System of several Python Flask applications and other services running on Docker Swarm that simulates an electoral system.

The system provides features like registration of election participants (political parties or individuals), creating elections, voting and getting insight of election results. The results of parliamentary elections are formed using D'Hondt method, while the results of presidential elections are formed based on the number of votes that participant received and the total number of votes.

The system consists of 2 main components - one used for authentication and authorization (access control stack) and one for managing the election process (election process management stack). Both of the components consist of network(s) of Docker containers, where each container has a different role in the system. There are two types of users: administrator, whose responsibilities include creating participants, creating elections and getting election results, and election official, whose responsibilities include providing batches of ballots.
