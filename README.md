sample project app implementing django custom Authentications Backend

>With this setup, when a user attempts to log in, the custom authentication backend will first try to authenticate them as a student using their provided username (student ID). If that fails, it will then try to authenticate them as a lecturer using the provided username (PF number).