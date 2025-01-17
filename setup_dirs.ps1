# Create main directories
New-Item -ItemType Directory -Force -Path "app"
New-Item -ItemType Directory -Force -Path "app\config"
New-Item -ItemType Directory -Force -Path "app\auth"
New-Item -ItemType Directory -Force -Path "app\utils"
New-Item -ItemType Directory -Force -Path "app\monitoring"
New-Item -ItemType Directory -Force -Path "app\ml"
New-Item -ItemType Directory -Force -Path "app\integrations"
New-Item -ItemType Directory -Force -Path "app\static"
New-Item -ItemType Directory -Force -Path "app\static\css"
New-Item -ItemType Directory -Force -Path "app\static\js"
New-Item -ItemType Directory -Force -Path "app\templates"
New-Item -ItemType Directory -Force -Path "reports"
New-Item -ItemType Directory -Force -Path "logs"

# Create __init__.py files
"from pathlib import Path`nAPP_ROOT = Path(__file__).parent`nPROJECT_ROOT = APP_ROOT.parent" | Out-File -FilePath "app\__init__.py" -Encoding utf8
"" | Out-File -FilePath "app\config\__init__.py" -Encoding utf8
"" | Out-File -FilePath "app\auth\__init__.py" -Encoding utf8
"" | Out-File -FilePath "app\utils\__init__.py" -Encoding utf8
"" | Out-File -FilePath "app\monitoring\__init__.py" -Encoding utf8
"" | Out-File -FilePath "app\ml\__init__.py" -Encoding utf8
"" | Out-File -FilePath "app\integrations\__init__.py" -Encoding utf8

Write-Host "Directory structure created successfully!" 