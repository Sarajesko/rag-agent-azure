param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl
)

$ErrorActionPreference = "Stop"

Write-Host "Validando despliegue en $BaseUrl"

$root = Invoke-RestMethod -Uri "$BaseUrl/"
Write-Host "GET / -> $($root.message)"

$health = Invoke-RestMethod -Uri "$BaseUrl/health"
Write-Host "GET /health -> database=$($health.database), chunks=$($health.knowledge_chunks)"

$knowledge = Invoke-RestMethod -Uri "$BaseUrl/knowledge"
Write-Host "GET /knowledge -> total=$($knowledge.total)"

$body = @{ question = "Explica que es RAG y que papel cumple Azure SQL" } | ConvertTo-Json
$ask = Invoke-RestMethod -Method Post -Uri "$BaseUrl/ask" -ContentType "application/json" -Body $body
Write-Host "POST /ask -> sources=$($ask.sources.Count)"

Write-Host "Validacion completada correctamente."
