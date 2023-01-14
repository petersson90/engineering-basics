$name = (Get-Item -Path Env:THE_NAME).value
Write-Output "Hello $name"
