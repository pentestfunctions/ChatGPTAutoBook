In this chapter, we will discuss the post-exploitation techniques that are used to maintain access to a compromised system, escalate privileges, cover tracks, and pivot to other systems on the network.

Maintaining Access:

Once a system has been compromised, it is important to maintain access to the system in order to continue to gather information and execute commands. One of the most commonly used tools for maintaining access is Netcat. Netcat is a simple yet powerful tool that can be used to establish a connection between two systems. It can be used to create a backdoor that allows an attacker to connect to the compromised system at any time. Another popular tool for maintaining access is Meterpreter, which is a post-exploitation tool that is included in the Metasploit Framework. Meterpreter provides a powerful platform for executing commands, uploading and downloading files, and interacting with the compromised system.

Backdoor Factory is another tool that can be used to create a backdoor on a compromised system. It can be used to modify an existing binary file and inject a backdoor into it. This backdoor can then be used to maintain access to the system.

Privilege Escalation:

Once a system has been compromised, the attacker may need to escalate privileges in order to gain access to sensitive data or perform certain actions. Windows Privilege Escalation techniques include exploiting vulnerabilities in the operating system, exploiting weak passwords, and using tools like Mimikatz to extract passwords from memory. Linux Privilege Escalation techniques include exploiting vulnerabilities in the operating system, exploiting weak file permissions, and using tools like SUID/SGID binaries to gain elevated privileges.

Covering Tracks:

After a system has been compromised, it is important to cover tracks to avoid detection. Clearlogs is a tool that can be used to clear system logs that may contain evidence of the attacker's activities. LogCleaner is another tool that can be used to clean up log files on a compromised system. Logrotate is a tool that can be used to rotate log files on a regular basis, which can help to prevent the accumulation of large amounts of data that could be used to track the attacker's activities.

Pivoting:

Pivoting is the process of using a compromised system to gain access to other systems on the network. SSH Tunneling can be used to create a secure connection between two systems, which can be used to pivot to other systems on the network. Meterpreter Port Forwarding can be used to forward traffic from a compromised system to other systems on the network.

In conclusion, post-exploitation techniques are an important part of penetration testing. Maintaining access, escalating privileges, covering tracks, and pivoting are all essential techniques that can be used to gather information and execute commands on a compromised system. It is important to understand these techniques in order to effectively test the security of a network.